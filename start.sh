#!/bin/bash

set -e

echo "=================================="
echo "NDE Monitoring Bot - Startup"
echo "=================================="

if [ ! -f .env ]; then
    echo "❌ File .env tidak ditemukan!"
    echo "📝 Copy .env.example menjadi .env dan isi dengan kredensial Anda:"
    echo "   cp .env.example .env"
    echo "   nano .env"
    exit 1
fi

echo "✅ File .env ditemukan"

echo "🔨 Building Docker image..."
docker-compose build

echo "🚀 Starting bot..."
docker-compose up -d

echo ""
echo "✅ Bot berhasil dijalankan!"
echo ""
echo "📊 Untuk melihat logs:"
echo "   docker-compose logs -f"
echo ""
echo "🔍 Untuk melihat status:"
echo "   docker-compose ps"
echo ""
echo "🛑 Untuk menghentikan bot:"
echo "   docker-compose down"
echo ""
