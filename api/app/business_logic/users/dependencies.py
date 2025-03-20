from fastapi import Request, Depends
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError

from app.business_logic.users.dao import UsersDAO
from app.config import get_auth_encoding
from app.exceptions import TokenNoFound, NoJwtException, NoUserIdException

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='auth/login')


def get_token(request: Request, token: str = Depends(oauth2_scheme)):
    if token:
        return token
    token = request.cookies.get('Authorization')
    if not token:
        raise TokenNoFound
    return token


async def get_user(token: str = Depends(get_token)):
    try:
        auth_data = get_auth_encoding()
        payload = jwt.decode(token, auth_data['secret_key'], algorithms=auth_data['algorithm'])
    except JWTError:
        raise NoJwtException
    user_id = payload.get('sub')
    if not user_id:
        raise NoUserIdException
    user = await UsersDAO.find_by_id(int(user_id))
    if not user:
        raise NoUserIdException
    return user
