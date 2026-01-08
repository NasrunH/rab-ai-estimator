import os
from dotenv import load_dotenv
from google import genai

# Load env variables
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("Error: GEMINI_API_KEY tidak ditemukan di .env")
    exit(1)

print("Sedang menghubungi Google AI untuk mengambil daftar model...")

try:
    client = genai.Client(api_key=api_key)
    # Mengambil list model
    # Perhatikan: struktur response list() mungkin berbeda tergantung versi SDK
    # Kita iterasi standard
    
    print("\n=== Model yang Tersedia untuk API Key Anda ===")
    count = 0
    for model in client.models.list():
        # Filter hanya model yang bisa generateContent (bukan embedding only)
        if "generateContent" in model.supported_generation_methods:
            print(f"- {model.name}")
            count += 1
            
    if count == 0:
        print("Tidak ada model generateContent yang ditemukan. Cek permission API Key.")
    else:
        print(f"\nTotal: {count} model ditemukan.")

except Exception as e:
    print(f"\nTerjadi kesalahan saat mengecek model: {e}")
    print("Pastikan library google-genai sudah terupdate: pip install --upgrade google-genai")