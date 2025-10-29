# Telegram Auto-Translate Bot (Indonesia <-> Thailand)

Bot Telegram sederhana yang otomatis menerjemahkan pesan antara Bahasa Indonesia dan Bahasa Thai.

Fitur:
- Mendeteksi bahasa pesan.
- Jika terdeteksi `id` → terjemahkan ke `th`.
- Jika terdeteksi `th` → terjemahkan ke `id`.
- Per-chat auto-translate (default: ON). Gunakan `/auto_off` dan `/auto_on`.
- Perintah: `/start`, `/status`, `/auto_on`, `/auto_off`.

Persyaratan:
- Python 3.8+
- Token bot Telegram

Instalasi & Jalankan:
1. Clone repo ini.
2. Buat virtualenv dan install dependencies:
   ```
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```
3. Buat file `.env` berdasarkan `.env.example` dan isi TELEGRAM_TOKEN:
   ```
   TELEGRAM_TOKEN=123456:ABC-DEF...
   ```
4. Jalankan:
   ```
   python bot.py
   ```

Catatan:
- Saya menggunakan library `googletrans` (4.0.0-rc1). Ini adalah library tidak-resmi dan kadang perubahan di pihak Google dapat mempengaruhi fungsionalitas. Jika kamu ingin solusi lebih stabil/produk, gunakan Google Cloud Translate API (berbayar) atau layanan translate lain dengan API resmi.
- Bot ini diset untuk auto-translate semua pesan yang terdeteksi `id` atau `th`. Di grup besar ini bisa mengganggu — gunakan `/auto_off` untuk mematikannya, atau sesuaikan logika (mis. hanya terjemahkan pesan yang reply ke bot atau yang diawali dengan prefix tertentu).

Deploy:
- Untuk hosting, bisa gunakan VPS, Heroku, Railway, atau layanan lain. Untuk Heroku, tambahkan `Procfile` dan set TELEGRAM_TOKEN sebagai config var.

Lisensi: bebas dipakai dan dimodifikasi.
