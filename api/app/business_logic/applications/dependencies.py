from jose import jwt, JWTError

from app.business_logic.applications.auth import app_key_is_correct
from app.business_logic.applications.dao import ApplicationsDAO
from app.config import get_auth_encoding
from app.exceptions import NoJwtException, AppNotFound, NoAccessToApp


async def get_application(api_key):
    try:
        auth_data = get_auth_encoding()
        payload = jwt.decode(api_key, auth_data['secret_key'], algorithms=auth_data['algorithm'])
    except JWTError:
        raise NoJwtException
    app_id = payload.get('sub')
    app_key = payload.get('key')
    if not app_id or not app_key:
        raise NoJwtException
    application = await ApplicationsDAO.find_one(id=int(app_id))
    if not application:
        raise AppNotFound
    if not app_key_is_correct(app_key, application.app_key):
        raise NoAccessToApp
    return application
