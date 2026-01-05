import os
import json
from flask import Flask, request, jsonify
import google.generativeai as genai
from dotenv import load_dotenv

# 1. Load API Key
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    print("Error: API Key belum diisi di file .env!")
    exit()

# 2. Setup Gemini
genai.configure(api_key=API_KEY)

# KITA GUNAKAN MODEL TERBARU YANG TERSEDIA DI AKUNMU
# Dari list kamu: 'models/gemini-2.0-flash'
model = genai.GenerativeModel('gemini-flash-latest')

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return "Server AI Estimator (Gemini 2.0 Flash) Aktif!"

@app.route('/analyze', methods=['POST'])
def analyze_rab():
    # Cek file upload
    if 'image' not in request.files:
        return jsonify({"error": "Tidak ada file gambar yang dikirim"}), 400
    
    file = request.files['image']
    if file.filename == '':
        return jsonify({"error": "Nama file kosong"}), 400

    try:
        # Baca gambar ke memori
        image_bytes = file.read()
        
        # 3. PROMPT KHUSUS RAB
        prompt = """
        Bertindaklah sebagai Professional Quantity Surveyor (Estimator Bangunan).
        Tugasmu adalah menganalisis gambar denah/konstruksi ini untuk membuat RAB (Rencana Anggaran Biaya) kasar.
        
        Lakukan langkah berikut:
        1. Identifikasi elemen konstruksi visual (Dinding, Lantai, Pintu, Jendela, Atap, Pondasi, dll).
        2. Perkirakan Volume-nya. Jika tidak ada skala dimensi, gunakan asumsi standar rumah tinggal (misal: tinggi dinding 3.5m).
        3. Kelompokkan item pekerjaan dengan rapi.

        OUTPUT HARUS BERUPA JSON VALID (Tanpa Markdown).
        Format JSON:
        {
            "proyek": "Estimasi Visual Bangunan",
            "kategori_pekerjaan": [
                {
                    "nama_kategori": "Pekerjaan Dinding & Plesteran",
                    "items": [
                        {
                            "pekerjaan": "Pasangan Dinding Bata Merah",
                            "volume": 120.5,
                            "satuan": "m2",
                            "estimasi_keterangan": "Asumsi keliling dinding terlihat x tinggi 3.5m"
                        }
                    ]
                },
                {
                    "nama_kategori": "Pekerjaan Lantai",
                    "items": [
                        {
                            "pekerjaan": "Pasang Keramik 60x60",
                            "volume": 45.0,
                            "satuan": "m2",
                            "estimasi_keterangan": "Luas area dalam ruangan"
                        }
                    ]
                }
            ]
        }
        """

        print("Mengirim data ke Gemini 2.0 Flash...")
        
        # Kirim ke AI
        response = model.generate_content([
            {'mime_type': 'image/jpeg', 'data': image_bytes},
            prompt
        ])
        
        # Bersihkan response (kadang AI membungkus dengan ```json ... ```)
        clean_text = response.text
        if "```json" in clean_text:
            clean_text = clean_text.split("```json")[1].split("```")[0]
        elif "```" in clean_text:
            clean_text = clean_text.replace("```", "")
            
        # Validasi JSON
        data_rab = json.loads(clean_text.strip())
        
        return jsonify({
            "status": "success",
            "model_used": "gemini-2.0-flash",
            "data": data_rab
        })

    except Exception as e:
        print(f"Error Server: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    print("Starting AI Server on port 5000...")
    app.run(host='0.0.0.0', port=5000, debug=True)