import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load API Key
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("API Key kosong! Cek file .env")
else:
    genai.configure(api_key=api_key)
    
    print("=== DAFTAR MODEL YANG BISA KAMU PAKAI ===")
    try:
        for m in genai.list_models():
            # Kita cari model yang support generateContent (bisa chat/gambar)
            if 'generateContent' in m.supported_generation_methods:
                print(f"- {m.name}")
    except Exception as e:
        print(f"Error koneksi: {e}")