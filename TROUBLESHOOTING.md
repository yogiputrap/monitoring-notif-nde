# Troubleshooting Guide

## Masalah Umum dan Solusi

### 🔴 Container tidak mau start

#### Gejala
```bash
$ docker-compose up -d
Error: ...
```

#### Solusi
1. **Periksa Docker running:**
   ```bash
   sudo systemctl status docker
   sudo systemctl start docker
   ```

2. **Periksa file .env ada dan terisi:**
   ```bash
   cat .env
   ```

3. **Periksa syntax docker-compose.yml:**
   ```bash
   docker-compose config
   ```

4. **Lihat logs detail:**
   ```bash
   docker-compose up
   ```

---

### 🔴 Login ke NDE gagal

#### Gejala
```
ERROR - Login failed - still on login page
```

#### Solusi
1. **Test login manual** ke https://nde.posindonesia.co.id/
   - Pastikan username dan password benar
   - Pastikan tidak ada perubahan form login

2. **Periksa credentials di .env:**
   ```bash
   grep "NDE_" .env
   ```

3. **Periksa koneksi internet:**
   ```bash
   docker exec nde-monitoring-bot ping -c 4 google.com
   ```

4. **Periksa selector login berubah:**
   - Website mungkin update UI
   - Perlu update selector di `src/scraper.py`

---

### 🔴 Tidak menerima notifikasi Telegram

#### Gejala
Bot running tapi tidak ada notifikasi

#### Solusi
1. **Pastikan bot sudah di-start:**
   - Buka bot di Telegram
   - Klik tombol "Start" atau kirim `/start`
   - Kirim pesan apa saja

2. **Test bot token:**
   ```bash
   curl https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getMe
   ```
   Harus return info bot

3. **Test chat ID:**
   ```bash
   # Kirim test message
   curl -X POST "https://api.telegram.org/bot<YOUR_BOT_TOKEN>/sendMessage" \
     -d "chat_id=<YOUR_CHAT_ID>" \
     -d "text=Test message"
   ```

4. **Periksa logs untuk error Telegram:**
   ```bash
   docker-compose logs | grep -i telegram
   ```

---

### 🔴 Bot crash atau restart terus

#### Gejala
```bash
$ docker-compose ps
Container terus restart
```

#### Solusi
1. **Lihat logs untuk error:**
   ```bash
   docker-compose logs --tail=50
   ```

2. **Periksa memory:**
   ```bash
   docker stats nde-monitoring-bot
   ```
   Jika memory usage 100%, tambah limit di docker-compose.yml

3. **Periksa Chrome driver:**
   ```bash
   docker exec nde-monitoring-bot which google-chrome
   ```

4. **Rebuild container:**
   ```bash
   docker-compose down
   docker-compose build --no-cache
   docker-compose up -d
   ```

---

### 🔴 Notifikasi duplikat

#### Gejala
Menerima notifikasi yang sama berkali-kali

#### Solusi
1. **Reset state:**
   ```bash
   docker-compose down
   rm state.json
   docker-compose up -d
   ```

2. **Periksa state file:**
   ```bash
   cat state.json
   ```

---

### 🔴 Memory usage tinggi

#### Gejala
Container menggunakan memory banyak

#### Solusi
1. **Kurangi memory limit:**
   Edit `docker-compose.yml`:
   ```yaml
   mem_limit: 512m
   mem_reservation: 256m
   ```

2. **Restart container:**
   ```bash
   docker-compose restart
   ```

3. **Monitor memory:**
   ```bash
   docker stats nde-monitoring-bot
   ```

---

### 🔴 Website NDE berubah struktur

#### Gejala
```
ERROR - Element not found
```

#### Solusi
1. **Inspect website manual:**
   - Buka https://nde.posindonesia.co.id/
   - Inspect element (F12)
   - Cari selector yang berubah

2. **Update selector di `src/scraper.py`:**
   ```python
   # Contoh update selector
   username_field = wait.until(
       EC.presence_of_element_located((By.NAME, "new_username_name"))
   )
   ```

3. **Test perubahan:**
   ```bash
   docker-compose restart
   docker-compose logs -f
   ```

---

### 🔴 Timezone salah

#### Gejala
Timestamp notifikasi tidak sesuai waktu lokal

#### Solusi
1. **Set timezone di .env:**
   ```env
   TZ=Asia/Jakarta
   ```

2. **Restart container:**
   ```bash
   docker-compose restart
   ```

3. **Verify timezone:**
   ```bash
   docker exec nde-monitoring-bot date
   ```

---

## Debug Mode

### Enable verbose logging

1. Edit `src/main.py`, ubah level logging:
   ```python
   logging.basicConfig(
       level=logging.DEBUG,  # Ubah dari INFO ke DEBUG
       ...
   )
   ```

2. Rebuild dan restart:
   ```bash
   docker-compose down
   docker-compose build
   docker-compose up -d
   ```

3. Lihat logs detail:
   ```bash
   docker-compose logs -f
   ```

---

## Perintah Debug Berguna

```bash
# Masuk ke container
docker exec -it nde-monitoring-bot bash

# Check Python version
docker exec nde-monitoring-bot python --version

# Check installed packages
docker exec nde-monitoring-bot pip list

# Check environment variables
docker exec nde-monitoring-bot env | grep NDE

# Check Chrome version
docker exec nde-monitoring-bot google-chrome --version

# Check network connectivity
docker exec nde-monitoring-bot curl -I https://nde.posindonesia.co.id/

# Check disk space
docker exec nde-monitoring-bot df -h

# Check running processes
docker exec nde-monitoring-bot ps aux
```

---

## Masih Bermasalah?

1. **Backup current setup:**
   ```bash
   cp .env .env.backup
   cp state.json state.json.backup
   cp monitor.log monitor.log.backup
   ```

2. **Clean reinstall:**
   ```bash
   docker-compose down -v
   docker system prune -a
   git pull
   docker-compose build --no-cache
   cp .env.backup .env
   docker-compose up -d
   ```

3. **Collect debug info:**
   ```bash
   echo "=== System Info ===" > debug.log
   uname -a >> debug.log
   echo -e "\n=== Docker Version ===" >> debug.log
   docker --version >> debug.log
   echo -e "\n=== Container Logs ===" >> debug.log
   docker-compose logs --tail=100 >> debug.log
   echo -e "\n=== Container Stats ===" >> debug.log
   docker stats nde-monitoring-bot --no-stream >> debug.log
   ```

4. **Share debug.log** untuk mendapat bantuan

---

## Kontak

Jika masih mengalami masalah setelah mencoba troubleshooting di atas, buat issue di repository dengan:
- Output dari `debug.log`
- Versi Docker dan OS
- Deskripsi masalah detail
- Steps yang sudah dicoba
