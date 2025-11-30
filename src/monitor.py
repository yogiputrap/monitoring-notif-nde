import logging
import asyncio
from datetime import datetime
from src.scraper import NDEScraper
from src.telegram_notifier import TelegramNotifier
from src.state_manager import StateManager

logger = logging.getLogger(__name__)


class NDEMonitor:
    def __init__(self):
        self.scraper = NDEScraper()
        self.notifier = TelegramNotifier()
        self.state_manager = StateManager()
        self.retry_count = 0
        self.max_retries = 3
    
    async def check_updates(self):
        try:
            logger.info("=== Starting check cycle ===")
            
            if not self.scraper.is_logged_in:
                logger.info("Logging in to NDE...")
                if not self.scraper.login():
                    logger.error("Login failed")
                    if self.retry_count < self.max_retries:
                        self.retry_count += 1
                        logger.info(f"Retry attempt {self.retry_count}/{self.max_retries}")
                        await asyncio.sleep(5)
                        return await self.check_updates()
                    else:
                        await self.notifier.send_error_alert("Login gagal setelah beberapa kali percobaan")
                        self.retry_count = 0
                        return
            
            self.retry_count = 0
            
            await self._check_verifications()
            await self._check_incoming_mails()
            await self._check_position_updates()
            
            self.state_manager.update_last_check(datetime.now().isoformat())
            self.state_manager.cleanup_old_ids()
            
            logger.info("=== Check cycle completed ===")
            
        except Exception as e:
            logger.error(f"Error during check cycle: {e}")
            await self.notifier.send_error_alert(str(e))
    
    async def _check_verifications(self):
        try:
            verifications = self.scraper.get_verification_messages()
            
            for verification in verifications:
                if self.state_manager.is_new_verification(verification):
                    logger.info(f"New verification found: {verification}")
                    await self.notifier.send_verification_alert(verification)
                    await asyncio.sleep(1)
            
            if verifications:
                logger.info(f"Checked {len(verifications)} verification messages")
                
        except Exception as e:
            logger.error(f"Error checking verifications: {e}")
    
    async def _check_incoming_mails(self):
        try:
            mails = self.scraper.get_incoming_mails()
            
            for mail in mails:
                if self.state_manager.is_new_incoming_mail(mail):
                    logger.info(f"New incoming mail found: {mail}")
                    await self.notifier.send_incoming_mail_alert(mail)
                    await asyncio.sleep(1)
            
            if mails:
                logger.info(f"Checked {len(mails)} incoming mails")
                
        except Exception as e:
            logger.error(f"Error checking incoming mails: {e}")
    
    async def _check_position_updates(self):
        try:
            positions = self.scraper.get_position_updates()
            
            for position in positions:
                if self.state_manager.is_new_position_update(position):
                    logger.info(f"New position update found: {position}")
                    await self.notifier.send_position_update_alert(position)
                    await asyncio.sleep(1)
            
            if positions:
                logger.info(f"Checked {len(positions)} position updates")
                
        except Exception as e:
            logger.error(f"Error checking position updates: {e}")
    
    def cleanup(self):
        logger.info("Cleaning up resources...")
        self.scraper.close()
