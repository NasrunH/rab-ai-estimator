🏗️ AI RAB Generator (Python Backend)

Proyek ini adalah microservice berbasis Python yang menggunakan Google Gemini AI untuk menganalisis gambar denah bangunan atau dokumen PDF teknik, lalu menghasilkan estimasi RAB (Rencana Anggaran Biaya) secara otomatis dalam format JSON terstruktur.

📋 Prasyarat (Requirements)

Sebelum memulai, pastikan komputer Anda memiliki:

Python 3.10+: Disarankan Python 3.12. (Centang "Add Python to PATH" saat instalasi).

Poppler: Dibutuhkan oleh library pdf2image untuk memproses file PDF.

Windows: Download dari poppler-windows, ekstrak, dan tambahkan folder bin ke Environment Variables PATH.

Linux: sudo apt-get install poppler-utils.

Mac: brew install poppler.

API Key Google Gemini: Dapatkan gratis di Google AI Studio.

🚀 Instalasi & Setup

Buat Virtual Environment

cd C:\path\ke\folder\proyek
python -m venv venv


Aktifkan Environment

Windows (PowerShell): .\venv\Scripts\Activate.ps1

Windows (CMD): venv\Scripts\activate.bat

Install Library

pip install flask flask-cors google-genai python-dotenv pydantic pillow pdf2image


⚙️ Konfigurasi

Setup API Key
Buat file .env di folder root:

GEMINI_API_KEY=KODE_API_KEY_ANDA


Model AI
Script ini menggunakan model gemini-1.5-flash-latest untuk kecepatan dan dukungan multimodal (gambar/PDF) yang stabil.

▶️ Cara Menjalankan

Pastikan terminal dalam mode (venv), lalu jalankan:

python server1.py


Server akan berjalan di http://localhost:5000.

🔗 Endpoint API

Sistem menyediakan endpoint utama untuk integrasi (CodeIgniter, Laravel, React, dll):

URL: http://localhost:5000/generate-rab

Method: POST

Payload (JSON):

{
  "prompt": "Opsional: Instruksi tambahan",
  "file": "Data base64 dari Gambar atau PDF",
  "file_type": "application/pdf atau image/png"
}


🛠️ Troubleshooting

Masalah

Penyebab

Solusi

Unable to get page count

Poppler belum terinstall/PATH salah.

Install Poppler dan pastikan perintah pdftoppm -v jalan di CMD.

Error 404 (Not Found)

Nama model salah atau SDK lama.

Gunakan gemini-1.5-flash-latest dan update library: pip install --upgrade google-genai.

Error 429 (Rate Limit)

Penggunaan gratis terlalu sering.

Tunggu 1-2 menit sebelum mencoba lagi.

Invalid Image Data

Format base64 tidak lengkap.

Pastikan string base64 dikirim dengan benar dari frontend.

Catatan: Gunakan model Flash untuk efisiensi biaya dan kecepatan analisis dokumen.