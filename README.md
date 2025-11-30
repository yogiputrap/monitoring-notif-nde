# NDE Pos Indonesia Monitoring Bot

Bot monitoring otomatis untuk website NDE Pos Indonesia (https://nde.posindonesia.co.id/) yang mengirimkan notifikasi ke Telegram ketika ada:
- 🔔 Pesan Verifikasi Baru
- 📬 Surat Masuk
- 📍 Update Diposisi

## Fitur

✅ **Monitoring Otomatis** - Cek setiap 5 menit (dapat dikonfigurasi)  
✅ **Notifikasi Telegram** - Instant notification untuk setiap update  
✅ **Login Authentication** - Login otomatis dengan credentials yang aman  
✅ **State Management** - Tracking untuk menghindari notifikasi duplikat  
✅ **Docker Ready** - Containerized untuk deployment yang mudah  
✅ **Production Ready** - Logging, error handling, dan auto-recovery  
✅ **Resource Efficient** - Headless browser dengan memory limit  

## 📖 Documentation

- **[Quick Start Guide](QUICKSTART.md)** - Setup dalam 5 menit
- **[Deployment Guide](DEPLOYMENT.md)** - Production deployment lengkap
- **[Troubleshooting](TROUBLESHOOTING.md)** - Solusi masalah umum
- **[Pre-Deployment Checklist](PRE-DEPLOYMENT-CHECKLIST.md)** - Checklist sebelum deploy
- **[Contributing](CONTRIBUTING.md)** - Panduan kontribusi
- **[Changelog](CHANGELOG.md)** - Version history

## Prerequisites

- Docker dan Docker Compose
- Telegram Bot Token (dari [@BotFather](https://t.me/botfather))
- Telegram Chat ID
- Akun NDE Pos Indonesia (username & password)

## Cara Mendapatkan Telegram Bot Token & Chat ID

### 1. Membuat Bot Telegram

1. Buka Telegram dan cari [@BotFather](https://t.me/botfather)
2. Kirim command `/newbot`
3. Ikuti instruksi untuk memberi nama dan username bot
4. Simpan **Bot Token** yang diberikan (format: `123456789:ABCdefGHIjklMNOpqrsTUVwxyz`)

### 2. Mendapatkan Chat ID

**Cara 1: Menggunakan Bot**
1. Cari bot Anda di Telegram dan klik "Start"
2. Kirim pesan apa saja ke bot
3. Buka browser dan akses: `https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getUpdates`
4. Cari `"chat":{"id":` - angka setelah `id` adalah Chat ID Anda

**Cara 2: Menggunakan @userinfobot**
1. Cari [@userinfobot](https://t.me/userinfobot) di Telegram
2. Klik "Start"
3. Bot akan mengirim Chat ID Anda

## Instalasi

### 1. Clone Repository

```bash
git clone <repository-url>
cd monitoring-notif-nde
```

### 2. Konfigurasi Environment

Copy file `.env.example` menjadi `.env`:

```bash
cp .env.example .env
```

Edit file `.env` dan isi dengan kredensial Anda:

```env
# NDE Pos Indonesia Credentials
NDE_USERNAME=username_anda
NDE_PASSWORD=password_anda

# Telegram Bot Configuration
TELEGRAM_BOT_TOKEN=123456789:ABCdefGHIjklMNOpqrsTUVwxyz
TELEGRAM_CHAT_ID=987654321

# Monitoring Configuration
CHECK_INTERVAL_MINUTES=5

# Optional: Timezone (default: Asia/Jakarta)
TZ=Asia/Jakarta
```

### 3. Build dan Jalankan dengan Docker

```bash
# Build image
docker-compose build

# Jalankan bot
docker-compose up -d

# Lihat logs
docker-compose logs -f
```

## Penggunaan

### Menjalankan Bot

```bash
# Start bot (background)
docker-compose up -d

# Start bot (foreground dengan logs)
docker-compose up
```

### Monitoring Logs

```bash
# Real-time logs
docker-compose logs -f

# Logs dari file
tail -f monitor.log
```

### Melihat Status

```bash
# Status container
docker-compose ps

# Health check
docker inspect --format='{{json .State.Health}}' nde-monitoring-bot
```

### Menghentikan Bot

```bash
# Stop bot
docker-compose down

# Stop dan hapus volumes
docker-compose down -v
```

## Struktur Project

```
monitoring-notif-nde/
├── src/
│   ├── __init__.py
│   ├── main.py                 # Entry point aplikasi
│   ├── config.py               # Konfigurasi dan environment variables
│   ├── scraper.py              # Web scraping logic untuk NDE
│   ├── telegram_notifier.py    # Telegram notification handler
│   ├── state_manager.py        # State management untuk tracking updates
│   └── monitor.py              # Main monitoring logic
├── .env                        # Environment variables (JANGAN di-commit!)
├── .env.example                # Template environment variables
├── .gitignore                  # Git ignore rules
├── .dockerignore               # Docker ignore rules
├── requirements.txt            # Python dependencies
├── Dockerfile                  # Docker image definition
├── docker-compose.yml          # Docker Compose configuration
└── README.md                   # Dokumentasi ini
```

## Teknologi yang Digunakan

- **Python 3.11** - Runtime
- **Selenium** - Web automation dan scraping
- **python-telegram-bot** - Telegram API integration
- **APScheduler** - Job scheduling
- **Docker** - Containerization
- **Chrome Headless** - Browser automation

## Konfigurasi Lanjutan

### Mengubah Interval Check

Edit file `.env`:

```env
CHECK_INTERVAL_MINUTES=10  # Check setiap 10 menit
```

### Resource Limits

Edit `docker-compose.yml` untuk menyesuaikan resource limits:

```yaml
mem_limit: 1g           # Maximum memory
mem_reservation: 512m   # Reserved memory
cpus: 1.0              # CPU limit
```

## Troubleshooting

### Bot Tidak Mengirim Notifikasi

1. Pastikan bot sudah di-start di Telegram (kirim `/start`)
2. Periksa Chat ID sudah benar
3. Periksa Bot Token valid
4. Lihat logs untuk error: `docker-compose logs -f`

### Login Gagal

1. Periksa username dan password sudah benar
2. Akses manual ke https://nde.posindonesia.co.id/ untuk memastikan akun aktif
3. Periksa logs untuk detail error

### Container Restart Terus

```bash
# Lihat logs
docker-compose logs

# Periksa health check
docker inspect --format='{{json .State.Health}}' nde-monitoring-bot
```

### Memory Issues

Kurangi resource limit di `docker-compose.yml` atau tambah memory di host.

## Maintenance

### Update Dependencies

```bash
# Update image
docker-compose pull

# Rebuild
docker-compose build --no-cache

# Restart
docker-compose up -d
```

### Backup State

```bash
# Backup state file
cp state.json state.json.backup

# Backup logs
cp monitor.log monitor.log.backup
```

### Clear Old State

```bash
# Stop bot
docker-compose down

# Remove state
rm state.json

# Start bot
docker-compose up -d
```

## Security Notes

⚠️ **PENTING:**

- Jangan commit file `.env` ke repository
- Jangan share Bot Token atau credentials
- Gunakan environment variables untuk sensitive data
- Backup state.json secara berkala
- Monitor logs untuk aktivitas mencurigakan

## Production Deployment

### Recommended Setup

1. **Server**: VPS dengan minimal 1GB RAM
2. **OS**: Ubuntu 20.04+ atau Debian 11+
3. **Docker**: Latest stable version
4. **Monitoring**: Setup alerts untuk container health
5. **Backup**: Automated backup untuk state.json

### Auto-restart on Boot

Docker Compose sudah dikonfigurasi dengan `restart: unless-stopped`, jadi container akan otomatis restart setelah server reboot.

### Monitoring Production

```bash
# Check container health
docker ps

# Monitor resource usage
docker stats nde-monitoring-bot

# Check logs for errors
docker-compose logs --tail=100 | grep ERROR
```

## License

Lihat file LICENSE untuk detail.

## Support

Jika mengalami masalah atau ada pertanyaan, silakan buat issue di repository ini.

---

**Dibuat dengan ❤️ untuk otomasi monitoring NDE Pos Indonesia**
