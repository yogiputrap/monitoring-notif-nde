import logging
import time
from datetime import datetime
from typing import Dict, List, Optional
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
from src.config import Config

logger = logging.getLogger(__name__)


class NDEScraper:
    def __init__(self):
        self.driver = None
        self.is_logged_in = False
    
    def _setup_driver(self):
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--window-size=1920,1080')
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        try:
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            logger.info("Chrome driver initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize Chrome driver: {e}")
            raise
    
    def login(self) -> bool:
        try:
            if not self.driver:
                self._setup_driver()
            
            logger.info(f"Navigating to {Config.NDE_URL}")
            self.driver.get(Config.NDE_URL)
            
            wait = WebDriverWait(self.driver, 15)
            
            logger.info("Looking for login form...")
            username_field = wait.until(
                EC.presence_of_element_located((By.NAME, "username"))
            )
            password_field = self.driver.find_element(By.NAME, "password")
            
            logger.info("Entering credentials...")
            username_field.clear()
            username_field.send_keys(Config.NDE_USERNAME)
            
            password_field.clear()
            password_field.send_keys(Config.NDE_PASSWORD)
            
            login_button = self.driver.find_element(By.CSS_SELECTOR, "button[type='submit'], input[type='submit']")
            login_button.click()
            
            time.sleep(3)
            
            if "login" not in self.driver.current_url.lower():
                self.is_logged_in = True
                logger.info("Login successful")
                return True
            else:
                logger.error("Login failed - still on login page")
                return False
                
        except TimeoutException:
            logger.error("Timeout waiting for login form")
            return False
        except NoSuchElementException as e:
            logger.error(f"Login element not found: {e}")
            return False
        except Exception as e:
            logger.error(f"Login error: {e}")
            return False
    
    def get_verification_messages(self) -> List[Dict]:
        if not self.is_logged_in:
            logger.warning("Not logged in, attempting login...")
            if not self.login():
                return []
        
        try:
            logger.info("Checking for verification messages...")
            
            wait = WebDriverWait(self.driver, 10)
            
            verifications = []
            
            try:
                verification_elements = self.driver.find_elements(
                    By.XPATH, 
                    "//div[contains(@class, 'verifikasi') or contains(text(), 'Verifikasi') or contains(text(), 'verifikasi')]"
                )
                
                for element in verification_elements:
                    verification_data = {
                        'text': element.text,
                        'timestamp': datetime.now().isoformat(),
                        'type': 'verification'
                    }
                    verifications.append(verification_data)
                    
            except NoSuchElementException:
                logger.info("No verification messages found")
            
            return verifications
            
        except Exception as e:
            logger.error(f"Error getting verification messages: {e}")
            return []
    
    def get_incoming_mails(self) -> List[Dict]:
        if not self.is_logged_in:
            logger.warning("Not logged in, attempting login...")
            if not self.login():
                return []
        
        try:
            logger.info("Checking for incoming mails...")
            
            mails = []
            
            try:
                mail_elements = self.driver.find_elements(
                    By.XPATH,
                    "//div[contains(@class, 'surat-masuk') or contains(@class, 'mail-inbox')]//tr | //table[contains(@class, 'inbox')]//tr"
                )
                
                for element in mail_elements[1:]:
                    try:
                        cells = element.find_elements(By.TAG_NAME, "td")
                        if cells:
                            mail_data = {
                                'content': element.text,
                                'timestamp': datetime.now().isoformat(),
                                'type': 'incoming_mail'
                            }
                            mails.append(mail_data)
                    except:
                        continue
                        
            except NoSuchElementException:
                logger.info("No incoming mails found")
            
            return mails
            
        except Exception as e:
            logger.error(f"Error getting incoming mails: {e}")
            return []
    
    def get_position_updates(self) -> List[Dict]:
        if not self.is_logged_in:
            logger.warning("Not logged in, attempting login...")
            if not self.login():
                return []
        
        try:
            logger.info("Checking for position updates...")
            
            positions = []
            
            try:
                position_elements = self.driver.find_elements(
                    By.XPATH,
                    "//div[contains(@class, 'diposisi') or contains(text(), 'Diposisi')]"
                )
                
                for element in position_elements:
                    position_data = {
                        'content': element.text,
                        'timestamp': datetime.now().isoformat(),
                        'type': 'position_update'
                    }
                    positions.append(position_data)
                    
            except NoSuchElementException:
                logger.info("No position updates found")
            
            return positions
            
        except Exception as e:
            logger.error(f"Error getting position updates: {e}")
            return []
    
    def close(self):
        if self.driver:
            try:
                self.driver.quit()
                logger.info("Browser closed")
            except Exception as e:
                logger.error(f"Error closing browser: {e}")
