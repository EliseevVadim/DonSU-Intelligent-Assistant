import uuid

from fastapi import APIRouter, Depends

from app.business_logic.chats.dao import ChatsDAO
from app.business_logic.messages.dao import MessagesDAO
from app.business_logic.messages.enums import MessageSender
from app.business_logic.messages.schemas import SendMessageDTO
from app.business_logic.messages.service import generate_response
from app.business_logic.users.dependencies import get_user
from app.business_logic.users.models import User
from app.exceptions import ChatNotFound, NoAccessToChat

router = APIRouter(prefix="/messages", tags=["Управление сообщениями"])


@router.get('/{chat_id}')
async def get_messages_by_chat(chat_id: str, user_data: User = Depends(get_user)):
    chat = await ChatsDAO.find_one(id=chat_id)
    if not chat:
        raise ChatNotFound
    if not chat.user_id == user_data.id:
        raise NoAccessToChat
    messages = await MessagesDAO.find_all(chat_id=chat_id)
    return {'messages': messages}


@router.post('/send')
async def send_message(message_data: SendMessageDTO, user_data: User = Depends(get_user)):
    chat = await ChatsDAO.find_one(id=message_data.chat_id)
    message_id = uuid.uuid4()
    if not chat:
        raise ChatNotFound
    if not chat.user_id == user_data.id:
        raise NoAccessToChat
    await MessagesDAO.add(**{
        'id': message_id,
        'chat_id': message_data.chat_id,
        'text_content': message_data.text_content,
        'sender': MessageSender.HUMAN
    })
    response = generate_response()
    response_id = uuid.uuid4()
    await MessagesDAO.add(**{
        'id': response_id,
        'chat_id': message_data.chat_id,
        'text_content': response,
        'sender': MessageSender.AI
    })
    await ChatsDAO.touch(message_data.chat_id)
    return {'response': response}


