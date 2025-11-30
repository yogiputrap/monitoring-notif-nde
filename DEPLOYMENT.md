# Production Deployment Guide

Panduan lengkap untuk deploy NDE Monitoring Bot ke production server.

## Prerequisites

### Server Requirements
- **OS**: Ubuntu 20.04+ / Debian 11+ / CentOS 8+
- **RAM**: Minimal 1GB (2GB recommended)
- **CPU**: 1 core minimum (2 cores recommended)
- **Storage**: Minimal 5GB free space
- **Network**: Internet connection dengan akses ke:
  - nde.posindonesia.co.id
  - api.telegram.org

### Software Requirements
- Docker 20.10+
- Docker Compose 2.0+
- Git (optional, untuk clone repository)

## Installation Steps

### 1. Install Docker

#### Ubuntu/Debian
```bash
# Update package index
sudo apt-get update

# Install dependencies
sudo apt-get install -y \
    apt-transport-https \
    ca-certificates \
    curl \
    gnupg \
    lsb-release

# Add Docker's official GPG key
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

# Set up stable repository
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# Install Docker Engine
sudo apt-get update
sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin

# Verify installation
sudo docker --version
sudo docker compose version
```

#### CentOS/RHEL
```bash
# Install required packages
sudo yum install -y yum-utils

# Add Docker repository
sudo yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo

# Install Docker
sudo yum install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin

# Start Docker
sudo systemctl start docker
sudo systemctl enable docker

# Verify installation
sudo docker --version
sudo docker compose version
```

### 2. Setup User Permissions (Optional)

```bash
# Add your user to docker group
sudo usermod -aG docker $USER

# Log out and back in, or run:
newgrp docker

# Verify you can run docker without sudo
docker ps
```

### 3. Deploy Application

#### Option A: Clone from Git
```bash
# Clone repository
git clone <repository-url> monitoring-nde
cd monitoring-nde
```

#### Option B: Upload Files
```bash
# Create directory
mkdir -p ~/monitoring-nde
cd ~/monitoring-nde

# Upload files via SCP
scp -r /local/path/* user@server:~/monitoring-nde/
```

### 4. Configure Environment

```bash
# Copy environment template
cp .env.example .env

# Edit configuration
nano .env
```

Fill in your credentials:
```env
NDE_USERNAME=your_username
NDE_PASSWORD=your_password
TELEGRAM_BOT_TOKEN=your_bot_token
TELEGRAM_CHAT_ID=your_chat_id
CHECK_INTERVAL_MINUTES=5
TZ=Asia/Jakarta
```

### 5. Build and Start

```bash
# Make scripts executable
chmod +x *.sh

# Build Docker image
docker compose build

# Start container in detached mode
docker compose up -d

# Check status
docker compose ps

# View logs
docker compose logs -f
```

## System Service (systemd)

For automatic startup on boot, create a systemd service:

### Create Service File

```bash
sudo nano /etc/systemd/system/nde-monitor.service
```

Add content:
```ini
[Unit]
Description=NDE Pos Indonesia Monitoring Bot
Requires=docker.service
After=docker.service

[Service]
Type=oneshot
RemainAfterExit=yes
WorkingDirectory=/home/your_user/monitoring-nde
ExecStart=/usr/bin/docker compose up -d
ExecStop=/usr/bin/docker compose down
TimeoutStartSec=0

[Install]
WantedBy=multi-user.target
```

### Enable and Start Service

```bash
# Reload systemd
sudo systemctl daemon-reload

# Enable service on boot
sudo systemctl enable nde-monitor

# Start service
sudo systemctl start nde-monitor

# Check status
sudo systemctl status nde-monitor
```

## Monitoring

### Health Checks

```bash
# Check container health
docker inspect --format='{{json .State.Health}}' nde-monitoring-bot | jq

# Check container status
docker compose ps

# View resource usage
docker stats nde-monitoring-bot
```

### Log Monitoring

```bash
# Real-time logs
docker compose logs -f

# Last 100 lines
docker compose logs --tail=100

# Search for errors
docker compose logs | grep ERROR

# Check log file directly
tail -f monitor.log
```

### Setup Log Rotation

Create logrotate config:
```bash
sudo nano /etc/logrotate.d/nde-monitor
```

Add:
```
/home/your_user/monitoring-nde/monitor.log {
    daily
    rotate 14
    compress
    delaycompress
    notifempty
    create 0644 your_user your_user
    postrotate
        docker compose -f /home/your_user/monitoring-nde/docker-compose.yml restart
    endscript
}
```

## Backup Strategy

### Automated Backup Script

Create backup script:
```bash
nano ~/backup-nde.sh
```

Add:
```bash
#!/bin/bash
BACKUP_DIR="/backup/nde-monitor"
DATE=$(date +%Y%m%d_%H%M%S)

mkdir -p $BACKUP_DIR

# Backup state file
cp ~/monitoring-nde/state.json $BACKUP_DIR/state_$DATE.json

# Backup logs
cp ~/monitoring-nde/monitor.log $BACKUP_DIR/monitor_$DATE.log

# Keep only last 30 days
find $BACKUP_DIR -name "state_*.json" -mtime +30 -delete
find $BACKUP_DIR -name "monitor_*.log" -mtime +30 -delete

echo "Backup completed: $DATE"
```

Make executable:
```bash
chmod +x ~/backup-nde.sh
```

### Setup Cron for Daily Backup

```bash
crontab -e
```

Add:
```
# Backup NDE monitor every day at 2 AM
0 2 * * * /home/your_user/backup-nde.sh >> /var/log/nde-backup.log 2>&1
```

## Monitoring Alerts

### Setup with Healthchecks.io (Optional)

```bash
# Install curl if not available
sudo apt-get install -y curl

# Add healthcheck script
nano ~/healthcheck-nde.sh
```

Add:
```bash
#!/bin/bash
HEALTHCHECK_URL="https://hc-ping.com/your-uuid-here"

if docker ps | grep -q nde-monitoring-bot; then
    curl -fsS --retry 3 $HEALTHCHECK_URL > /dev/null
fi
```

Add to cron:
```
*/5 * * * * /home/your_user/healthcheck-nde.sh
```

## Updates

### Update Container

```bash
# Pull latest changes
cd ~/monitoring-nde
git pull

# Rebuild container
docker compose down
docker compose build --no-cache
docker compose up -d

# Verify
docker compose logs -f
```

### Rollback

```bash
# Stop current version
docker compose down

# Restore from backup
cp /backup/nde-monitor/state_YYYYMMDD_HHMMSS.json state.json

# Checkout previous version
git checkout previous-commit-hash

# Rebuild and start
docker compose build
docker compose up -d
```

## Security Hardening

### 1. Firewall Configuration

```bash
# Allow only necessary ports
sudo ufw allow 22/tcp  # SSH
sudo ufw enable

# Docker doesn't need exposed ports for this application
```

### 2. Secure .env File

```bash
# Set proper permissions
chmod 600 .env
chown your_user:your_user .env
```

### 3. Regular Updates

```bash
# Update system packages monthly
sudo apt-get update && sudo apt-get upgrade -y

# Update Docker images
docker compose pull
docker compose up -d
```

## Performance Optimization

### 1. Adjust Resource Limits

Edit `docker-compose.yml`:
```yaml
services:
  nde-monitor:
    mem_limit: 512m      # Reduce if server has limited RAM
    mem_reservation: 256m
    cpus: 0.5           # Reduce CPU allocation
```

### 2. Adjust Check Interval

Edit `.env`:
```env
CHECK_INTERVAL_MINUTES=10  # Increase to reduce resource usage
```

## Troubleshooting Production

### Container Won't Start

```bash
# Check Docker service
sudo systemctl status docker

# Check logs
docker compose logs

# Check disk space
df -h

# Check memory
free -h
```

### High Memory Usage

```bash
# Monitor resources
docker stats

# Restart container
docker compose restart

# If persistent, reduce memory limit in docker-compose.yml
```

### Network Issues

```bash
# Test connectivity
docker exec nde-monitoring-bot ping -c 4 8.8.8.8
docker exec nde-monitoring-bot curl -I https://nde.posindonesia.co.id/

# Check DNS
docker exec nde-monitoring-bot nslookup nde.posindonesia.co.id
```

## Maintenance Schedule

### Daily
- ✅ Check logs for errors: `./logs.sh | grep ERROR`
- ✅ Verify notifications received

### Weekly
- ✅ Review resource usage: `docker stats`
- ✅ Check disk space: `df -h`
- ✅ Verify backups created

### Monthly
- ✅ Update system packages
- ✅ Update Docker images
- ✅ Review and cleanup old logs
- ✅ Test backup restoration

### Quarterly
- ✅ Security audit
- ✅ Performance review
- ✅ Update documentation

## Support

For production support:
1. Check [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
2. Review logs: `docker compose logs --tail=100`
3. Create issue with debug info

## Scaling (Future)

For monitoring multiple accounts:
1. Run multiple containers with different .env files
2. Use Docker networks for isolation
3. Setup reverse proxy if needed
4. Use container orchestration (Kubernetes) for large scale

---

**Remember**: Always test changes in staging environment before applying to production!
