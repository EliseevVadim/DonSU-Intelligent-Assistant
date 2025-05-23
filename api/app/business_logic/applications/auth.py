import hashlib


def hash_app_key(app_key: str) -> str:
    return hashlib.sha256(app_key.encode('utf-8')).hexdigest()


def app_key_is_correct(app_key: str, hashed_key: str) -> bool:
    return hash_app_key(app_key) == hashed_key
