from fastapi import APIRouter, Depends, Response
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from app.business_logic.users.auth import hash_password, authenticate_user, create_access_token
from app.business_logic.users.dao import UsersDAO
from app.business_logic.users.dependencies import get_user
from app.business_logic.users.models import User
from app.business_logic.users.schemas import UserRegistrationDTO, UserPublicDTO
from app.exceptions import UserAlreadyExistsException, IncorrectEmailOrPasswordException

router = APIRouter(prefix='/auth', tags=['Авторизация и регистрация пользователей'])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")


@router.post('/register')
async def register_user(user_data: UserRegistrationDTO):
    user = await UsersDAO.find_one(email=user_data.email)
    if user:
        raise UserAlreadyExistsException
    user_info = user_data.model_dump()
    user_info['password'] = hash_password(user_data.password)
    del user_info['registration_secret']
    await UsersDAO.add(**user_info)
    return {'message': 'Пользователь успешно зарегистрирован'}


@router.post('/auth/token')
async def login(response: Response, form_data: OAuth2PasswordRequestForm = Depends()):
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise IncorrectEmailOrPasswordException
    access_token = create_access_token({'sub': str(user.id)})
    response.set_cookie(key='access_token', value=access_token, httponly=True)
    return {'ok': True, 'access_token': access_token,
            'message': 'Авторизация прошла успешно'}


@router.get('/me')
async def get_me(user_data: User = Depends(get_user)):
    return UserPublicDTO(**user_data.__dict__)
