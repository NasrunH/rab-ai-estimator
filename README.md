🏗️ AI RAB Generator (Python Backend)

Proyek ini adalah microservice berbasis Python yang menggunakan Google Gemini AI untuk menganalisis gambar denah bangunan dan menghasilkan estimasi RAB (Rencana Anggaran Biaya) kasar dalam format JSON.

Sistem ini dirancang untuk diintegrasikan dengan aplikasi utama (misalnya CodeIgniter 4 atau Laravel).

📋 Prasyarat (Requirements)

Sebelum memulai, pastikan komputer Anda memiliki:

Python 3.10 atau lebih baru (Disarankan Python 3.12).

Download: python.org

⚠️ PENTING: Saat instalasi, pastikan mencentang opsi "Add Python to PATH".

API Key Google Gemini (Gratis via Google AI Studio).

🚀 Instalasi & Setup

Ikuti langkah-langkah ini secara berurutan di terminal (PowerShell atau CMD).

1. Buat Virtual Environment

Agar library tidak bentrok dengan sistem Windows, kita wajib menggunakan Virtual Environment.

# Masuk ke folder proyek
cd C:\path\ke\folder\estimator

# Buat environment baru bernama 'venv'
python -m venv venv


2. Aktifkan Environment

Setiap kali ingin menjalankan aplikasi, langkah ini wajib dilakukan.

Untuk Windows (PowerShell):

.\venv\Scripts\Activate.ps1


Untuk Windows (CMD):

venv\Scripts\activate.bat


✅ Indikator Sukses: Akan muncul tulisan (venv) di sebelah kiri baris perintah terminal Anda.

3. Install Library

Install semua paket yang dibutuhkan (Flask, Google AI, Dotenv).

pip install flask google-generativeai python-dotenv


⚙️ Konfigurasi

1. Setup API Key

Buat file baru bernama .env (tanpa nama depan) di dalam folder root proyek. Isi file tersebut dengan baris berikut:

GEMINI_API_KEY=KODE_API_KEY_ANDA_DISINI


Jangan bagikan file .env ini ke orang lain atau upload ke GitHub publik.

2. Cek Model AI (ai_server.py)

Pastikan script ai_server.py menggunakan model yang Gratis & Stabil untuk menghindari error limit kuota.

# Pastikan baris ini menggunakan 1.5-flash
model = genai.GenerativeModel('gemini-1.5-flash')


▶️ Cara Menjalankan

Pastikan terminal masih dalam mode (venv).

Jalankan server:

python ai_server.py


Jika berhasil, akan muncul pesan:

Server berjalan di [http://0.0.0.0:5000](http://0.0.0.0:5000)


(Jangan tutup terminal ini selama aplikasi digunakan)

🧪 Cara Testing (Tanpa Frontend)

Kami telah menyediakan file UI sederhana untuk memastikan AI bekerja sebelum diintegrasikan ke CodeIgniter.

Pastikan ai_server.py sedang berjalan.

Buka file test_upload.html (Double click atau drag ke Browser).

Upload gambar denah (JPG/PNG).

Klik Analisis.

Tunggu 5-10 detik hingga JSON muncul.

🛠️ Troubleshooting (Masalah Umum)

Error

Penyebab

Solusi

ModuleNotFoundError

Python tidak membaca library yang diinstall.

Pastikan (venv) aktif. Jalankan pakai .\venv\Scripts\python ai_server.py.

Error 404 (Model not found)

Nama model salah atau tidak tersedia.

Ganti nama model di ai_server.py menjadi gemini-1.5-flash atau gemini-flash-latest.

Error 429 (Quota Exceeded)

Limit penggunaan habis atau pakai model berbayar.

Jangan pakai gemini-2.0. Gunakan gemini-1.5-flash.

pip command not found

Python belum masuk PATH Windows.

Install ulang Python dan centang "Add Python to PATH".

🔗 Endpoint API

Jika ingin dihubungkan ke CodeIgniter/Postman:

URL: http://localhost:5000/analyze

Method: POST

Body (Form-Data):

Key: image (Type: File)