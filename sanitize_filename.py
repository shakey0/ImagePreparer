import re
import string
import random

def sanitize_filename(filename):

    base_name = filename.rsplit('.', 1)[0] if '.' in filename else filename
    
    sanitized = base_name.lower()
    sanitized = re.sub(r'[\s-]+', '_', sanitized)
    
    sanitized = re.sub(r'[^a-z0-9_]', '', sanitized)
    
    random_chars = ''.join(random.choices(string.ascii_letters + string.digits, k=12))
    
    return f"{sanitized}_{random_chars}.webp"
