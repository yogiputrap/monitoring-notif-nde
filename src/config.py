import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    NDE_URL = "https://nde.posindonesia.co.id/"
    NDE_USERNAME = os.getenv("NDE_USERNAME")
    NDE_PASSWORD = os.getenv("NDE_PASSWORD")
    
    TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
    TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
    
    CHECK_INTERVAL_MINUTES = int(os.getenv("CHECK_INTERVAL_MINUTES", "5"))
    
    STATE_FILE = "state.json"
    
    @classmethod
    def validate(cls):
        missing = []
        if not cls.NDE_USERNAME:
            missing.append("NDE_USERNAME")
        if not cls.NDE_PASSWORD:
            missing.append("NDE_PASSWORD")
        if not cls.TELEGRAM_BOT_TOKEN:
            missing.append("TELEGRAM_BOT_TOKEN")
        if not cls.TELEGRAM_CHAT_ID:
            missing.append("TELEGRAM_CHAT_ID")
        
        if missing:
            raise ValueError(f"Missing required environment variables: {', '.join(missing)}")
        
        return True
