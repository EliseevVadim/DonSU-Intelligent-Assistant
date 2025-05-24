import secrets
import uuid

from fastapi import APIRouter, Depends, Response, Request
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from datetime import datetime, timedelta, timezone

from authlib.integrations.starlette_client import OAuth
from starlette.responses import RedirectResponse

from app.business_logic.applications.dependencies import get_application
from app.business_logic.chats.dao import ChatsDAO
from app.business_logic.users.auth import hash_password, authenticate_user, create_access_token
from app.business_logic.users.dao import UsersDAO
from app.business_logic.users.dependencies import get_user
from app.business_logic.users.models import User
from app.business_logic.users.schemas import UserRegistrationDTO, UserPublicDTO, ResetPasswordRequestDTO, \
    ResetPasswordDTO, ExternalUserRegistrationDTO, GetExternalUsersDTO, GetExternalUserRegisteredDTO
from app.business_logic.users.service import send_password_reset_email
from app.config import get_google_client_id, get_google_client_secret, get_client_url
from app.exceptions import UserAlreadyExistsException, IncorrectEmailOrPasswordException, NoUserIdException, \
    CantResetPasswordException, PasswordResetLinkInvalid, PasswordsMismatch

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

PASSWORD_RESET_TOKEN_EXPIRE_MINUTES = 15


@router.post('/register')
async def register_user(user_data: UserRegistrationDTO):
    user = await UsersDAO.find_one(email=user_data.email)
    if user:
        raise UserAlreadyExistsException
    user_info = user_data.model_dump()
    user_info['password'] = hash_password(user_data.password)
    await UsersDAO.add(**user_info)
    return {'message': 'Пользователь успешно зарегистрирован'}


@router.post('/register/external')
async def register_external_user(user_data: ExternalUserRegistrationDTO):
    external_app = await get_application(user_data.api_key)
    email = f"{user_data.external_user_id}@{external_app.auth_provider_name}.oauth"
    user = await UsersDAO.find_one(email=email)
    if user:
        raise UserAlreadyExistsException
    user_info = {
        'first_name': user_data.first_name,
        'last_name': user_data.last_name,
        'email': email,
        'auth_provider': external_app.auth_provider_name,
        'password': hash_password(secrets.token_urlsafe(32))
    }
    await UsersDAO.add(**user_info)
    user = await UsersDAO.find_one(email=email)
    chat_info = {
        'id': uuid.uuid4(),
        'user_id': user.id,
        'name': f"Чат с пользователем {user.id} в {external_app.auth_provider_name}"
    }
    await ChatsDAO.add(**chat_info)
    return {'message': 'Пользователь успешно зарегистрирован'}


@router.post('/externally-added')
async def get_external_users(search_data: GetExternalUsersDTO):
    external_app = await get_application(search_data.api_key)
    users = await UsersDAO.find_all(auth_provider=external_app.auth_provider_name)
    return {'users': users}


@router.post('/external-user-registered')
async def external_user_already_registered(search_data: GetExternalUserRegisteredDTO):
    external_app = await get_application(search_data.api_key)
    email = f"{search_data.external_user_id}@{external_app.auth_provider_name}.oauth"
    user = await UsersDAO.find_one(email=email)
    user_found = user is not None
    return {'registered': user_found}


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
    return RedirectResponse(f"{get_client_url()}/external_auth?access_token={access_token}")


@router.post('/password/reset')
async def request_password_reset(request_data: ResetPasswordRequestDTO):
    user = await UsersDAO.find_one(email=request_data.email)
    if not user:
        raise NoUserIdException
    reset_token = secrets.token_urlsafe(64)
    token_expires_at = datetime.now() + timedelta(minutes=PASSWORD_RESET_TOKEN_EXPIRE_MINUTES)
    rows = await UsersDAO.update(filter_by={'id': user.id}, reset_token=reset_token,
                                 reset_token_expires_at=token_expires_at)
    if rows == 0:
        raise CantResetPasswordException
    reset_link = f"{get_client_url()}/auth/password/reset/confirm?token={reset_token}"
    await send_password_reset_email(user.email, reset_link)
    return {'message': 'На ваш адрес электронной почты отправлена ссылка для сброса пароля.', 'link': reset_link}


@router.post('/password/reset/confirm')
async def reset_password(request_data: ResetPasswordDTO):
    user = await UsersDAO.find_one(reset_token=request_data.token)
    if not user or user.reset_token_expires_at < datetime.now():
        raise PasswordResetLinkInvalid
    if request_data.new_password != request_data.confirm_new_password:
        raise PasswordsMismatch
    rows = await UsersDAO.update(filter_by={'id': user.id}, password=hash_password(request_data.new_password),
                                 reset_token=None, reset_token_expires_at=None)
    if rows == 0:
        raise CantResetPasswordException
    return {'message': 'Пароль успешно сброшен. Теперь вы можете войти в систему с новым паролем.'}


@router.get('/me')
async def get_me(user_data: User = Depends(get_user)):
    return UserPublicDTO(**user_data.__dict__)


@router.post('/logout')
async def logout(response: Response):
    response.delete_cookie('access_token')
    return {'message': 'Пользователь успешно вышел из системы'}
