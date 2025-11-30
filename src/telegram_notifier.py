import logging
from telegram import Bot
from telegram.error import TelegramError
from src.config import Config

logger = logging.getLogger(__name__)


class TelegramNotifier:
    def __init__(self):
        self.bot = Bot(token=Config.TELEGRAM_BOT_TOKEN)
        self.chat_id = Config.TELEGRAM_CHAT_ID
    
    async def send_message(self, message: str):
        try:
            await self.bot.send_message(
                chat_id=self.chat_id,
                text=message,
                parse_mode='HTML'
            )
            logger.info(f"Notification sent successfully")
            return True
        except TelegramError as e:
            logger.error(f"Failed to send Telegram message: {e}")
            return False
    
    async def send_verification_alert(self, verification_data: dict):
        message = (
            "🔔 <b>PESAN VERIFIKASI BARU</b>\n\n"
            f"📋 <b>Detail:</b>\n"
        )
        
        for key, value in verification_data.items():
            message += f"• {key}: {value}\n"
        
        message += f"\n⏰ Timestamp: {verification_data.get('timestamp', 'N/A')}"
        
        await self.send_message(message)
    
    async def send_incoming_mail_alert(self, mail_data: dict):
        message = (
            "📬 <b>SURAT MASUK BARU</b>\n\n"
            f"📋 <b>Detail:</b>\n"
        )
        
        for key, value in mail_data.items():
            message += f"• {key}: {value}\n"
        
        message += f"\n⏰ Timestamp: {mail_data.get('timestamp', 'N/A')}"
        
        await self.send_message(message)
    
    async def send_position_update_alert(self, position_data: dict):
        message = (
            "📍 <b>UPDATE DIPOSISI</b>\n\n"
            f"📋 <b>Detail:</b>\n"
        )
        
        for key, value in position_data.items():
            message += f"• {key}: {value}\n"
        
        message += f"\n⏰ Timestamp: {position_data.get('timestamp', 'N/A')}"
        
        await self.send_message(message)
    
    async def send_error_alert(self, error_message: str):
        message = (
            "❌ <b>ERROR</b>\n\n"
            f"Terjadi kesalahan pada monitoring bot:\n\n"
            f"<code>{error_message}</code>"
        )
        
        await self.send_message(message)
    
    async def send_startup_message(self):
        message = (
            "✅ <b>Bot Monitoring Started</b>\n\n"
            f"Monitoring NDE Pos Indonesia setiap {Config.CHECK_INTERVAL_MINUTES} menit.\n"
            f"URL: {Config.NDE_URL}"
        )
        
        await self.send_message(message)
