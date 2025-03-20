from app.base_dao import BaseDAO
from app.business_logic.users.models import User


class UsersDAO(BaseDAO):
    model = User
