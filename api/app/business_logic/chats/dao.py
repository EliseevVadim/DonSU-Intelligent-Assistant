from datetime import datetime, timezone

from sqlalchemy import update

from app.base_dao import BaseDAO
from app.business_logic.chats.models import Chat
from app.database import async_session_maker


class ChatsDAO(BaseDAO):
    model = Chat

    @classmethod
    async def touch(cls, chat_id: str):
        async with async_session_maker() as session:
            await session.execute(
                update(cls.model)
                .where(cls.model.id == chat_id)
                .values(updated_at=datetime.now(timezone.utc))
            )
            await session.commit()
