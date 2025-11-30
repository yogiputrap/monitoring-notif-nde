import json
import logging
import os
from typing import Dict, List, Set
from src.config import Config

logger = logging.getLogger(__name__)


class StateManager:
    def __init__(self):
        self.state_file = Config.STATE_FILE
        self.state = self._load_state()
    
    def _load_state(self) -> Dict:
        if os.path.exists(self.state_file):
            try:
                with open(self.state_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                logger.error(f"Error loading state file: {e}")
                return self._get_default_state()
        return self._get_default_state()
    
    def _get_default_state(self) -> Dict:
        return {
            'verification_ids': [],
            'incoming_mail_ids': [],
            'position_update_ids': [],
            'last_check': None
        }
    
    def _save_state(self):
        try:
            with open(self.state_file, 'w') as f:
                json.dump(self.state, f, indent=2)
            logger.debug("State saved successfully")
        except Exception as e:
            logger.error(f"Error saving state: {e}")
    
    def _generate_id(self, data: Dict) -> str:
        return f"{data.get('type', 'unknown')}_{data.get('timestamp', '')}_{hash(str(data.get('content', data.get('text', ''))))}"
    
    def is_new_verification(self, verification_data: Dict) -> bool:
        item_id = self._generate_id(verification_data)
        if item_id not in self.state['verification_ids']:
            self.state['verification_ids'].append(item_id)
            self._save_state()
            return True
        return False
    
    def is_new_incoming_mail(self, mail_data: Dict) -> bool:
        item_id = self._generate_id(mail_data)
        if item_id not in self.state['incoming_mail_ids']:
            self.state['incoming_mail_ids'].append(item_id)
            self._save_state()
            return True
        return False
    
    def is_new_position_update(self, position_data: Dict) -> bool:
        item_id = self._generate_id(position_data)
        if item_id not in self.state['position_update_ids']:
            self.state['position_update_ids'].append(item_id)
            self._save_state()
            return True
        return False
    
    def update_last_check(self, timestamp: str):
        self.state['last_check'] = timestamp
        self._save_state()
    
    def cleanup_old_ids(self, max_items: int = 1000):
        if len(self.state['verification_ids']) > max_items:
            self.state['verification_ids'] = self.state['verification_ids'][-max_items:]
        
        if len(self.state['incoming_mail_ids']) > max_items:
            self.state['incoming_mail_ids'] = self.state['incoming_mail_ids'][-max_items:]
        
        if len(self.state['position_update_ids']) > max_items:
            self.state['position_update_ids'] = self.state['position_update_ids'][-max_items:]
        
        self._save_state()
