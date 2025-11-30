# Pre-Deployment Checklist

Gunakan checklist ini sebelum deploy ke production untuk memastikan semua sudah siap.

## ✅ Prerequisites

### Server Setup
- [ ] Server/VPS sudah tersedia
- [ ] SSH access ke server sudah dikonfigurasi
- [ ] Docker dan Docker Compose terinstall
- [ ] Port firewall sudah dikonfigurasi (jika perlu)
- [ ] Domain/IP address sudah tersedia (jika perlu)

### Credentials
- [ ] Akun NDE Pos Indonesia sudah aktif
- [ ] Username dan password NDE sudah disiapkan
- [ ] Telegram Bot Token sudah didapat dari @BotFather
- [ ] Telegram Chat ID sudah didapat
- [ ] Test login manual ke NDE berhasil
- [ ] Test bot Telegram dengan kirim pesan berhasil

## ✅ Configuration

### Environment File
- [ ] File `.env` sudah dibuat dari `.env.example`
- [ ] `NDE_USERNAME` sudah diisi dengan benar
- [ ] `NDE_PASSWORD` sudah diisi dengan benar
- [ ] `TELEGRAM_BOT_TOKEN` sudah diisi dengan benar
- [ ] `TELEGRAM_CHAT_ID` sudah diisi dengan benar
- [ ] `CHECK_INTERVAL_MINUTES` sudah disesuaikan (default: 5)
- [ ] `TZ` timezone sudah disesuaikan (default: Asia/Jakarta)

### File Permissions
- [ ] `.env` file permissions set ke 600 (chmod 600 .env)
- [ ] Shell scripts executable (chmod +x *.sh)

## ✅ Testing

### Local Testing (Optional)
- [ ] Docker build berhasil: `docker compose build`
- [ ] Container dapat start: `docker compose up`
- [ ] Logs tidak menunjukkan error critical
- [ ] Bot dapat login ke NDE (check logs)
- [ ] Notifikasi Telegram diterima (startup message)

### Verification
- [ ] Python syntax check passed: `python3 -m py_compile src/*.py`
- [ ] Docker compose config valid: `docker compose config`
- [ ] No sensitive data in git: check `.gitignore`

## ✅ Documentation Review

- [ ] README.md sudah dibaca dan dipahami
- [ ] QUICKSTART.md sudah dibaca
- [ ] DEPLOYMENT.md sudah dibaca untuk production setup
- [ ] TROUBLESHOOTING.md sudah dibookmark untuk reference

## ✅ Backup Plan

- [ ] Backup strategy sudah direncanakan
- [ ] Location backup sudah ditentukan
- [ ] Backup script sudah disiapkan (optional)
- [ ] Recovery plan sudah direncanakan

## ✅ Monitoring Plan

- [ ] Log monitoring strategy sudah direncanakan
- [ ] Notification channel untuk alerts sudah disiapkan
- [ ] Health check monitoring sudah dikonfigurasi (optional)
- [ ] Resource monitoring sudah disetup (optional)

## ✅ Security

- [ ] `.env` file tidak di-commit ke git
- [ ] `.gitignore` sudah mencakup semua sensitive files
- [ ] Server firewall dikonfigurasi dengan benar
- [ ] SSH key-based auth digunakan (bukan password)
- [ ] Regular update schedule sudah direncanakan

## ✅ Production Deployment

### Upload Files
- [ ] Semua file sudah diupload ke server
- [ ] File structure sudah benar
- [ ] `.env` file sudah ada di server

### Docker Setup
- [ ] Docker service running: `sudo systemctl status docker`
- [ ] User dapat run docker tanpa sudo (optional)
- [ ] Docker compose version compatible (2.0+)

### Initial Start
- [ ] Build image: `docker compose build`
- [ ] Start container: `docker compose up -d`
- [ ] Check status: `docker compose ps`
- [ ] Check logs: `docker compose logs -f`
- [ ] Verify startup message received di Telegram

### Verification
- [ ] Container status "Up" dan healthy
- [ ] Logs menunjukkan "Login successful"
- [ ] Startup notification received di Telegram
- [ ] No error messages di logs
- [ ] Resource usage normal: `docker stats`

## ✅ Post-Deployment

### Immediate Check (First 15 minutes)
- [ ] Container masih running setelah 5 menit
- [ ] First check cycle completed successfully
- [ ] Logs tidak menunjukkan error
- [ ] Memory usage stable

### First Hour
- [ ] Container masih healthy
- [ ] Check cycles berjalan sesuai interval
- [ ] Notifications diterima (jika ada update)
- [ ] No crashes atau restarts

### First Day
- [ ] Container running selama 24 jam tanpa issue
- [ ] Multiple check cycles completed successfully
- [ ] State file sudah terbuat dan terupdate
- [ ] Log file size reasonable

### First Week
- [ ] No unexpected errors di logs
- [ ] Memory usage stable
- [ ] Notifications received as expected
- [ ] Performance acceptable

## ✅ Maintenance Setup

- [ ] Log rotation dikonfigurasi
- [ ] Backup automation disetup (jika perlu)
- [ ] Monitoring alerts dikonfigurasi (jika perlu)
- [ ] Update schedule ditentukan
- [ ] Documentation maintenance schedule dibuat

## ✅ Rollback Plan

- [ ] Previous version backup available
- [ ] Rollback procedure documented
- [ ] Rollback tested (optional)
- [ ] Emergency contact list available

## 🎯 Final Check

Sebelum consider deployment "successful":
- [ ] ✅ All items above checked
- [ ] ✅ Container running stable for 24+ hours
- [ ] ✅ Notifications working correctly
- [ ] ✅ No critical errors in logs
- [ ] ✅ Resource usage acceptable
- [ ] ✅ Team informed about deployment
- [ ] ✅ Documentation bookmarked for reference

---

## Notes

Catat hal-hal penting selama deployment:

```
Deployment Date: _______________
Deployed By: _______________
Server IP/Domain: _______________

Issues Encountered:
1. _______________
2. _______________

Solutions Applied:
1. _______________
2. _______________

Additional Notes:
_______________
_______________
```

---

## Quick Commands Reference

```bash
# Build
docker compose build

# Start
docker compose up -d

# Stop
docker compose down

# Logs
docker compose logs -f

# Status
docker compose ps

# Stats
docker stats nde-monitoring-bot

# Restart
docker compose restart

# Update
docker compose pull && docker compose up -d
```

---

**🎉 Deployment Complete!**

Simpan checklist ini untuk reference dan future deployments.
