import secrets

from fastapi import APIRouter, Depends, Response, Request
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from authlib.integrations.starlette_client import OAuth

from app.business_logic.users.auth import hash_password, authenticate_user, create_access_token
from app.business_logic.users.dao import UsersDAO
from app.business_logic.users.dependencies import get_user
from app.business_logic.users.models import User
from app.business_logic.users.schemas import UserRegistrationDTO, UserPublicDTO
from app.config import get_google_client_id, get_google_client_secret
from app.exceptions import UserAlreadyExistsException, IncorrectEmailOrPasswordException

router = APIRouter(prefix='/auth', tags=['Авторизация и регистрация пользователей'])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login/token")
oauth = OAuth()
oauth.register(
    name='google',
    client_id=get_google_client_id(),
    client_secret=get_google_client_secret(),
    authorize_url="https://accounts.google.com/o/oauth2/auth",
    access_token_url="https://oauth2.googleapis.com/token",
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
    client_kwargs={"scope": "openid email profile"},
)


@router.post('/register')
async def register_user(user_data: UserRegistrationDTO):
    user = await UsersDAO.find_one(email=user_data.email)
    if user:
        raise UserAlreadyExistsException
    user_info = user_data.model_dump()
    user_info['password'] = hash_password(user_data.password)
    await UsersDAO.add(**user_info)
    return {'message': 'Пользователь успешно зарегистрирован'}


@router.post('/login')
async def login(response: Response, form_data: OAuth2PasswordRequestForm = Depends()):
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise IncorrectEmailOrPasswordException
    access_token = create_access_token({'sub': str(user.id)})
    response.set_cookie(key='access_token', value=access_token, httponly=True)
    return {'ok': True, 'access_token': access_token,
            'message': 'Авторизация прошла успешно'}


@router.get('/google')
async def auth_google(request: Request):
    nonce = secrets.token_urlsafe(16)
    request.session['nonce'] = nonce
    return await oauth.google.authorize_redirect(request, request.url_for('auth_google_callback'), nonce=nonce)


@router.get('/google/callback')
async def auth_google_callback(request: Request):
    token = await oauth.google.authorize_access_token(request)
    nonce = request.session.pop('nonce', None)
    user_info = await oauth.google.parse_id_token(token, nonce=nonce)
    user = await UsersDAO.find_one(email=user_info['email'])
    if not user:
        user_data = {
            'first_name': user_info['given_name'],
            'last_name': user_info['family_name'],
            'email': user_info['email'],
            'password': hash_password(secrets.token_urlsafe(32)),
            'auth_provider': 'google'
        }
        user = await UsersDAO.add(**user_data)
    access_token = create_access_token({'sub': str(user.id)})
    return {'ok': True, 'access_token': access_token,
            'message': 'Авторизация прошла успешно'}



@router.get('/me')
async def get_me(user_data: User = Depends(get_user)):
    return UserPublicDTO(**user_data.__dict__)
