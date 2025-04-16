from app.base_dao import BaseDAO
from app.business_logic.messages.models import Message


class MessagesDAO(BaseDAO):
    model = Message
