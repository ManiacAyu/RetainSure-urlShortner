import re
import random
import string
from urllib.parse import urlparse

def validate_url(url: str) -> bool:
    if not url or not isinstance(url, str):
        return False
    
    url_pattern = re.compile(
        r'^https?://'
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'
        r'localhost|'
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'
        r'(?::\d+)?'
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    
    if not url_pattern.match(url):
        return False
    
    try:
        parsed = urlparse(url)
        return bool(parsed.netloc and parsed.scheme in ['http', 'https'])
    except Exception:
        return False

def generate_short_code(length: int = 6, max_attempts: int = 100) -> str:
    from .models import url_store
    characters = string.ascii_letters + string.digits
    
    for _ in range(max_attempts):
        short_code = ''.join(random.choices(characters, k=length))
        if not url_store.code_exists(short_code):
            return short_code
    
    raise RuntimeError("Unable to generate unique short code")

def normalize_url(url: str) -> str:
    url = url.strip()
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url
    return url
