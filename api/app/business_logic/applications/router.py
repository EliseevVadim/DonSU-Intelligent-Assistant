import uuid

from fastapi import APIRouter, Depends

from app.business_logic.applications.auth import hash_app_key
from app.business_logic.applications.dao import ApplicationsDAO
from app.business_logic.applications.schemas import CreateApplicationDTO, UpdateApplicationDTO
from app.business_logic.users.auth import create_access_token
from app.business_logic.users.dependencies import get_user
from app.business_logic.users.models import User
from app.exceptions import AppNotFound, NoAccessToApp

router = APIRouter(prefix="/apps", tags=["Управление приложениями"])


@router.get('/')
async def get_all_apps_made_by_user(user_data: User = Depends(get_user)):
    apps = await ApplicationsDAO.find_all(creator_id=user_data.id)
    return {'apps': apps}


@router.post('/create')
async def create_app(app_data: CreateApplicationDTO,
                     user_data: User = Depends(get_user)):
    app_info = app_data.model_dump()
    app_key = uuid.uuid4().hex
    hashed_key = hash_app_key(app_key)
    app_info['app_key'] = hashed_key
    app_info['creator_id'] = user_data.id
    await ApplicationsDAO.add(**app_info)
    application = await ApplicationsDAO.find_one(app_key=hashed_key)
    api_key = create_access_token({'sub': str(application.id), 'key': app_key})
    return {
        'ok': True,
        'app_key': app_key,
        'api_key': api_key,
        'message': f'Приложение успешно создано. Используйте '
                   f'ключ приложения для модификации информации о нем и токен для '
                   f'авторизации запросов к API. ВАЖНО! Храните их в защищенном месте! Передача ключа и токена третьим '
                   f'лицам может повлечь к несанкционированному доступу, их утеря - к потере доступа к приложению.'
    }


@router.put('/update')
async def update_app(app_data: UpdateApplicationDTO,
                     user_data: User = Depends(get_user)):
    hashed_key = hash_app_key(app_data.app_key)
    renaming_app = await ApplicationsDAO.find_one(app_key=hashed_key)
    if not renaming_app:
        raise AppNotFound
    if renaming_app.creator_id != user_data.id:
        raise NoAccessToApp
    app_info = app_data.model_dump()
    del app_info['app_key']
    await ApplicationsDAO.update(filter_by={'app_key': hashed_key}, **app_info)
    return {
        'ok': True,
        'message': 'Данные приложения успешно изменены'
    }
