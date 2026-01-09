from flask import Flask, request, jsonify
from flask_cors import CORS
from google import genai
from pydantic import BaseModel, Field
import os
from dotenv import load_dotenv
import base64
import io
import time
from PIL import Image
from pdf2image import convert_from_bytes # Import tambahan untuk PDF

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Configure Gemini API
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    print("Warning: GEMINI_API_KEY environment variable not set.")

# Initialize client
try:
    client = genai.Client(api_key=api_key or "")
except Exception as e:
    print(f"Failed to initialize Gemini client: {e}")
    client = None

class RABItem(BaseModel):
    uraian_pekerjaan: str = Field(description="Uraian detail pekerjaan")
    volume: float = Field(description="Volume pekerjaan")
    satuan: str = Field(description="Satuan pengukuran (m2, m3, bh, ls, dll)")
    harga_satuan: float = Field(description="Harga satuan standar per unit")
    total_harga: float = Field(description="Total harga (volume * harga_satuan)")
    kategori: str = Field(description="Kategori pekerjaan (Persiapan, Struktur, Arsitektur, MEP, dll)")

def attempt_generate(model_name, contents, config):
    """
    Fungsi bantu untuk mencoba generate content dengan satu model tertentu.
    Melakukan retry jika terkena Rate Limit (429) atau Server Error (500+).
    """
    max_retries = 3
    base_delay = 5  # Detik

    for attempt in range(max_retries):
        try:
            print(f"Mencoba generate dengan model: {model_name} (Percobaan {attempt+1}/{max_retries})")
            response = client.models.generate_content(
                model=model_name,
                contents=contents,
                config=config,
            )
            return response
        except Exception as e:
            error_str = str(e)
            print(f"  -> Error pada {model_name}: {error_str}")
            
            # Cek error quota (429) atau server overload (503/500)
            if any(x in error_str for x in ["429", "RESOURCE_EXHAUSTED", "500", "503"]):
                if attempt < max_retries - 1:
                    sleep_time = (attempt + 1) * base_delay
                    print(f"  -> Quota penuh atau server sibuk. Menunggu {sleep_time} detik sebelum retry...")
                    time.sleep(sleep_time)
                    continue
                else:
                    print(f"  -> Gagal setelah {max_retries} kali percobaan pada model {model_name}.")
                    raise e
            else:
                raise e

@app.route('/generate-rab', methods=['POST'])
def generate_rab():
    if not client:
        return jsonify({"error": "Server configuration error: Gemini Client not initialized"}), 500
        
    try:
        data = request.json
        if not data:
            return jsonify({"error": "No data provided"}), 400

        # Mendukung field 'image' (bisa berisi PDF base64) atau 'file'
        image_data = data.get('image') or data.get('file')
        file_type = data.get('file_type', '') # Opsional, untuk deteksi lebih akurat
        user_prompt = data.get('prompt')

        if not image_data and not user_prompt:
            return jsonify({"error": "Harap sertakan gambar/PDF ATAU deskripsi teks."}), 400

        contents = []

        # Context prompt instructions
        base_instruction = """
        Anda adalah seorang ahli estimator biaya konstruksi (Quantity Surveyor) profesional di Indonesia.
        Tugas anda adalah membuat Rencana Anggaran Biaya (RAB) yang detail, akurat, dan realistis.

        Instruksi Teknis:
        1. Output HARUS berupa JSON array berisi objek RABItem sesuai schema. 
        2. Jangan tambahkan markdown block ```json atau teks lain diluar JSON raw.
        3. Gunakan standar harga konstruksi Indonesia terbaru (Rupiah).
        4. Kelompokkan pekerjaan secara sistematis (Persiapan, Tanah & Pondasi, Struktur, Dinding, Lantai, Plafond, Atap, Pintu Jendela, Finishing/Pengecatan, MEP).
        """

        if user_prompt:
            final_prompt = f"{base_instruction}\n\nPermintaan Spesifik User: {user_prompt}"
            if image_data:
                final_prompt += "\n\nAnalisis file (gambar/PDF) yang disertakan untuk melengkapi detail RAB sesuai permintaan user."
        else:
            final_prompt = base_instruction + """
            \n\nAnalisis file arsitektur/teknik yang diberikan dengan sangat teliti:
            1. Identifikasi jenis bangunan dan fungsi.
            2. Perkirakan dimensi dan luas berdasarkan proporsi visual.
            3. Tentukan spesifikasi material yang standar digunakan untuk tipe bangunan tersebut.
            4. Buatkan RAB lengkap dari tahap persiapan hingga finishing berdasarkan visual tersebut.
            """

        contents.append(final_prompt)

        # Logika Pengolahan File (Gambar atau PDF)
        if image_data:
            try:
                # Bersihkan prefix base64
                if "base64," in image_data:
                    image_data = image_data.split("base64,")[1]
                
                file_bytes = base64.b64decode(image_data)

                # Cek apakah file adalah PDF (berdasarkan file_type atau magic bytes PDF '%PDF-')
                if file_type == 'application/pdf' or image_data.startswith('JVBERi0'):
                    print("File terdeteksi sebagai PDF. Mengonversi ke gambar...")
                    # Konversi PDF ke gambar (setiap halaman menjadi satu gambar)
                    pages = convert_from_bytes(file_bytes)
                    for page in pages:
                        contents.append(page)
                    print(f"Berhasil memproses {len(pages)} halaman PDF.")
                else:
                    # Proses sebagai gambar biasa
                    image = Image.open(io.BytesIO(file_bytes))
                    contents.append(image)
                    
            except Exception as img_err:
                print(f"Error processing file: {img_err}")
                return jsonify({"error": f"Invalid file data: {str(img_err)}"}), 400

        # --- LOGIC PEMILIHAN MODEL (FALLBACK CHAIN) ---
        # Menggunakan gemini-1.5-flash-latest untuk menghindari error 404 model lama
        candidate_models = [
            "gemini-flash-latest"
        ]
        
        last_error = None
        
        generate_config = {
            "response_mime_type": "application/json",
            "response_schema": list[RABItem],
        }

        for model in candidate_models:
            try:
                response = attempt_generate(model, contents, generate_config)
                print(f"Sukses generate menggunakan model: {model}")
                return response.text, 200, {'Content-Type': 'application/json'}
            except Exception as e:
                print(f"Gagal total menggunakan model {model}. Pindah ke model berikutnya.")
                last_error = e
                continue

        error_msg = str(last_error)
        friendly_error = "Maaf, server AI sedang sangat sibuk (Rate Limit). Silakan coba lagi dalam 1-2 menit." if "429" in error_msg else f"Terjadi kesalahan teknis: {error_msg}"
        
        return jsonify({"error": friendly_error}), 500

    except Exception as e:
        print(f"Unexpected Error: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/', methods=['GET'])
def health_check():
    return jsonify({"status": "active", "service": "RAB AI Estimator"}), 200

if __name__ == '__main__':
    port = int(os.getenv("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)