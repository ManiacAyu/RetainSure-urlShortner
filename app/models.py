from datetime import datetime
from threading import Lock
from typing import Dict, Optional

class URLMapping:
    def __init__(self, original_url: str, short_code: str):
        self.original_url = original_url
        self.short_code = short_code
        self.clicks = 0
        self.created_at = datetime.utcnow()
    
    def increment_clicks(self):
        self.clicks += 1
    
    def to_dict(self):
        return {
            'url': self.original_url,
            'short_code': self.short_code,
            'clicks': self.clicks,
            'created_at': self.created_at.isoformat()
        }

class URLStore:
    def __init__(self):
        self._mappings: Dict[str, URLMapping] = {}
        self._lock = Lock()
    
    def store_mapping(self, short_code: str, mapping: URLMapping) -> None:
        with self._lock:
            self._mappings[short_code] = mapping
    
    def get_mapping(self, short_code: str) -> Optional[URLMapping]:
        with self._lock:
            return self._mappings.get(short_code)
    
    def increment_clicks(self, short_code: str) -> bool:
        with self._lock:
            mapping = self._mappings.get(short_code)
            if mapping:
                mapping.increment_clicks()
                return True
            return False
    
    def code_exists(self, short_code: str) -> bool:
        with self._lock:
            return short_code in self._mappings

url_store = URLStore()
