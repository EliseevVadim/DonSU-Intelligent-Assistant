from app.base_dao import BaseDAO
from app.business_logic.chats.models import Chat


class ChatsDAO(BaseDAO):
    model = Chat
