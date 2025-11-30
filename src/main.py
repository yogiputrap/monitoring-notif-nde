import asyncio
import logging
import signal
import sys
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from src.config import Config
from src.monitor import NDEMonitor

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('monitor.log')
    ]
)

logger = logging.getLogger(__name__)


class MonitoringBot:
    def __init__(self):
        self.monitor = NDEMonitor()
        self.scheduler = AsyncIOScheduler()
        self.is_running = False
    
    async def start(self):
        try:
            logger.info("=" * 60)
            logger.info("NDE Pos Indonesia Monitoring Bot")
            logger.info("=" * 60)
            
            Config.validate()
            logger.info("Configuration validated successfully")
            
            await self.monitor.notifier.send_startup_message()
            
            logger.info(f"Scheduling checks every {Config.CHECK_INTERVAL_MINUTES} minutes")
            
            self.scheduler.add_job(
                self.monitor.check_updates,
                trigger=IntervalTrigger(minutes=Config.CHECK_INTERVAL_MINUTES),
                id='nde_monitor',
                name='NDE Monitor Check',
                replace_existing=True
            )
            
            self.scheduler.start()
            self.is_running = True
            
            logger.info("Performing initial check...")
            await self.monitor.check_updates()
            
            logger.info("Bot is now running. Press Ctrl+C to stop.")
            
            while self.is_running:
                await asyncio.sleep(1)
                
        except KeyboardInterrupt:
            logger.info("Received keyboard interrupt")
            await self.stop()
        except Exception as e:
            logger.error(f"Fatal error: {e}", exc_info=True)
            await self.stop()
            sys.exit(1)
    
    async def stop(self):
        logger.info("Shutting down bot...")
        self.is_running = False
        
        if self.scheduler.running:
            self.scheduler.shutdown(wait=False)
        
        self.monitor.cleanup()
        
        logger.info("Bot stopped successfully")
    
    def setup_signal_handlers(self):
        def signal_handler(sig, frame):
            logger.info(f"Received signal {sig}")
            self.is_running = False
        
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)


async def main():
    bot = MonitoringBot()
    bot.setup_signal_handlers()
    await bot.start()


if __name__ == "__main__":
    asyncio.run(main())
