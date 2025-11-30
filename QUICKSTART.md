# Quick Start Guide

## Setup dalam 5 Menit! ⚡

### 1️⃣ Buat Telegram Bot (2 menit)

1. Buka Telegram, cari **@BotFather**
2. Kirim: `/newbot`
3. Ikuti instruksi, simpan **Bot Token** yang diberikan
4. Cari bot Anda, klik **Start**, kirim pesan "Hello"

### 2️⃣ Dapatkan Chat ID (1 menit)

1. Buka browser, akses:
   ```
   https://api.telegram.org/bot<MASUKKAN_BOT_TOKEN_ANDA>/getUpdates
   ```
2. Cari angka di `"chat":{"id": ANGKA_INI}`
3. Catat **Chat ID** tersebut

### 3️⃣ Setup Bot (2 menit)

```bash
# 1. Copy template config
cp .env.example .env

# 2. Edit file .env
nano .env
# atau
vim .env
# atau gunakan text editor favorit Anda

# 3. Isi kredensial:
#    - NDE_USERNAME: username NDE Anda
#    - NDE_PASSWORD: password NDE Anda
#    - TELEGRAM_BOT_TOKEN: token dari BotFather
#    - TELEGRAM_CHAT_ID: chat ID dari step 2

# 4. Jalankan bot
chmod +x start.sh
./start.sh
```

## Selesai! ✅

Bot Anda sekarang berjalan dan akan:
- ✅ Login ke NDE Pos Indonesia otomatis
- ✅ Cek setiap 5 menit untuk update baru
- ✅ Kirim notifikasi ke Telegram Anda

## Lihat Logs

```bash
# Real-time logs
./logs.sh

# atau
docker-compose logs -f
```

## Stop Bot

```bash
./stop.sh

# atau
docker-compose down
```

## Troubleshooting Cepat

### ❌ Login gagal?
- Cek username/password di .env
- Pastikan akun NDE aktif
- Lihat logs: `./logs.sh`

### ❌ Tidak dapat notifikasi?
- Pastikan sudah kirim pesan ke bot Telegram Anda
- Cek Bot Token dan Chat ID benar
- Lihat logs untuk error

### ❌ Container terus restart?
- Periksa semua env variables sudah diisi
- Lihat logs: `docker-compose logs`

## Perintah Berguna

```bash
# Status container
docker-compose ps

# Restart bot
docker-compose restart

# Lihat resource usage
docker stats nde-monitoring-bot

# Backup state
cp state.json state.backup.json

# Update & restart
docker-compose down
docker-compose pull
docker-compose build --no-cache
docker-compose up -d
```

## Butuh Bantuan?

Lihat **README.md** untuk dokumentasi lengkap!
