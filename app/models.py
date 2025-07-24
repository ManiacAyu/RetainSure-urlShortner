from datetime import datetime
from threading import Lock
from typing import Dict, Optional

class URLMapping:
    """Represents a URL mapping with analytics"""
    def __init__(self, original_url: str, short_code: str):
        self.original_url = original_url
        self.short_code = short_code
        self.clicks = 0
        self.created_at = datetime.utcnow()
    
    def increment_clicks(self):
        """Thread-safe click increment"""
        self.clicks += 1
    
    def to_dict(self):
        """Convert to dictionary for JSON serialization"""
        return {
            'url': self.original_url,
            'short_code': self.short_code,
            'clicks': self.clicks,
            'created_at': self.created_at.isoformat()
        }

class URLStore:
    """Thread-safe in-memory storage for URL mappings"""
    def __init__(self):
        self._mappings: Dict[str, URLMapping] = {}
        self._lock = Lock()
    
    def store_mapping(self, short_code: str, mapping: URLMapping) -> None:
        """Store a URL mapping"""
        with self._lock:
            self._mappings[short_code] = mapping
    
    def get_mapping(self, short_code: str) -> Optional[URLMapping]:
        """Get a URL mapping by short code"""
        with self._lock:
            return self._mappings.get(short_code)
    
    def increment_clicks(self, short_code: str) -> bool:
        """Increment click count for a short code"""
        with self._lock:
            mapping = self._mappings.get(short_code)
            if mapping:
                mapping.increment_clicks()
                return True
            return False
    
    def code_exists(self, short_code: str) -> bool:
        """Check if a short code already exists"""
        with self._lock:
            return short_code in self._mappings

# Global store instance
url_store = URLStore()
