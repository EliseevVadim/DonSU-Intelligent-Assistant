import uuid
from datetime import datetime, timezone, timedelta

from fastapi import APIRouter, Depends

from app.business_logic.applications.dependencies import get_application
from app.business_logic.chats.dao import ChatsDAO
from app.business_logic.messages.dao import MessagesDAO
from app.business_logic.messages.dependencies import get_chain
from app.business_logic.messages.enums import MessageSender
from app.business_logic.messages.schemas import SendMessageDTO, SendMessageExternallyDTO
from app.business_logic.messages.service import generate_response, build_chat_history, should_clear_context
from app.business_logic.users.dao import UsersDAO
from app.business_logic.users.dependencies import get_user
from app.business_logic.users.models import User
from app.constants import KEEP_MESSAGES_IN_MEMORY, CLEAR_CONTEXT_AFTER_HOURS_OF_NEW_DAY
from app.exceptions import ChatNotFound, NoAccessToChat, ExternalAppUserNotFound

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
async def send_message(message_data: SendMessageDTO,
                       user_data: User = Depends(get_user),
                       rag_chain=Depends(get_chain)):
    chat = await ChatsDAO.find_one(id=message_data.chat_id)
    message_id = uuid.uuid4()
    if not chat:
        raise ChatNotFound
    if not chat.user_id == user_data.id:
        raise NoAccessToChat
    history = await MessagesDAO.load_chat_history(chat_id=message_data.chat_id,
                                                  messages_count=KEEP_MESSAGES_IN_MEMORY)
    chat_history = build_chat_history(history)
    await MessagesDAO.add(**{
        'id': message_id,
        'chat_id': message_data.chat_id,
        'text_content': message_data.text_content,
        'sender': MessageSender.HUMAN
    })
    response = generate_response(query=message_data.text_content,
                                 rag_chain=rag_chain,
                                 chat_history=chat_history)
    response_id = uuid.uuid4()
    await MessagesDAO.add(**{
        'id': response_id,
        'chat_id': message_data.chat_id,
        'text_content': response['answer'],
        'sender': MessageSender.AI
    })
    await ChatsDAO.touch(message_data.chat_id)
    return {'response': response}


@router.post('/send/external')
async def send_message(message_data: SendMessageExternallyDTO,
                       rag_chain=Depends(get_chain)):
    external_app = await get_application(message_data.api_key)
    email = f"{message_data.external_user_id}@{external_app.auth_provider_name}.oauth"
    user = await UsersDAO.find_one(email=email)
    if not user:
        raise ExternalAppUserNotFound
    chat = await ChatsDAO.find_one(user_id=user.id)
    message_id = uuid.uuid4()
    history = await MessagesDAO.load_chat_history(chat_id=chat.id,
                                                  messages_count=KEEP_MESSAGES_IN_MEMORY)
    clear_context = should_clear_context(history, CLEAR_CONTEXT_AFTER_HOURS_OF_NEW_DAY)
    chat_history = [] if clear_context else build_chat_history(history)
    await MessagesDAO.add(**{
        'id': message_id,
        'chat_id': chat.id,
        'text_content': message_data.text_content,
        'sender': MessageSender.HUMAN
    })
    response = generate_response(query=message_data.text_content,
                                 rag_chain=rag_chain,
                                 chat_history=chat_history)
    response_id = uuid.uuid4()
    await MessagesDAO.add(**{
        'id': response_id,
        'chat_id': chat.id,
        'text_content': response['answer'],
        'sender': MessageSender.AI
    })
    return {'response': response}
