import hashlib


def hash_app_key(app_key: str) -> str:
    return hashlib.sha256(app_key.encode('utf-8')).hexdigest()
