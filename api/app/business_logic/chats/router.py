import uuid
from datetime import datetime, timezone

from fastapi import APIRouter, Depends

from app.business_logic.applications.dependencies import get_application
from app.business_logic.chats.dao import ChatsDAO
from app.business_logic.chats.schemas import RenameChatDTO, ResetChatContextDTO
from app.business_logic.users.dao import UsersDAO
from app.business_logic.users.dependencies import get_user
from app.business_logic.users.models import User
from app.exceptions import ChatNotFound, NoAccessToChat, ExternalAppUserNotFound

router = APIRouter(prefix='/chats', tags=['Управление чатами'])


@router.get('/')
async def get_all_chats_for_user(user_data: User = Depends(get_user)):
    chats = await ChatsDAO.find_all(user_id=user_data.id)
    return {'chats': chats}


@router.post('/create')
async def create_chat(user_data: User = Depends(get_user)):
    chat_id = uuid.uuid4()
    user_id = user_data.id
    chat_name = f"Чат #{chat_id}"
    await ChatsDAO.add(**{'id': chat_id, 'user_id': user_id, 'name': chat_name})
    return {'ok': True, 'chat_id': chat_id}


@router.put('/rename')
async def rename_chat(rename_data: RenameChatDTO, user_data: User = Depends(get_user)):
    renaming_chat = await ChatsDAO.find_one(id=rename_data.chat_id)
    if not renaming_chat:
        raise ChatNotFound
    if not renaming_chat.user_id == user_data.id:
        raise NoAccessToChat
    await ChatsDAO.update(filter_by={'id': renaming_chat.id}, name=rename_data.new_name)
    return {'ok': True, 'new_name': rename_data.new_name}


@router.delete('/delete/{chat_id}')
async def delete_chat(chat_id: str, user_data: User = Depends(get_user)):
    deleting_chat = await ChatsDAO.find_one(id=chat_id)
    if not deleting_chat:
        raise ChatNotFound
    if not deleting_chat.user_id == user_data.id:
        raise NoAccessToChat
    await ChatsDAO.delete(id=chat_id)
    return {'ok': True, 'message': 'Чат был успешно удален'}


@router.post('/reset-context')
async def reset_chat_context(reset_data: ResetChatContextDTO):
    external_app = await get_application(reset_data.api_key)
    email = f"{reset_data.external_user_id}@{external_app.auth_provider_name}.oauth"
    user = await UsersDAO.find_one(email=email)
    if not user:
        raise ExternalAppUserNotFound
    chat = await ChatsDAO.find_one(user_id=user.id)
    await ChatsDAO.update(filter_by={'id': chat.id}, last_context_reset_at=datetime.now(timezone.utc))
    return {'ok': True, 'message': 'Контекст чата был успешно сброшен'}
