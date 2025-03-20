from datetime import datetime, timezone, timedelta

from jose import jwt
from passlib.context import CryptContext
from pydantic import EmailStr

from app.business_logic.users.dao import UsersDAO
from app.config import get_auth_encoding

password_context = CryptContext(schemes=['sha256_crypt'], deprecated='auto')


def hash_password(password: str) -> str:
    return password_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return password_context.verify(plain_password, hashed_password)


def create_access_token(data: dict) -> str:
    data_to_encode = data.copy()
    auth_encoding = get_auth_encoding()
    token = jwt.encode(data_to_encode, auth_encoding['secret_key'], algorithm=auth_encoding['algorithm'])
    return token


async def authenticate_user(email: EmailStr, password: str):
    user = await UsersDAO.find_one(email=email)
    if not user or verify_password(password, user.password) is False:
        return None
    return user
