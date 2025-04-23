from sqlalchemy import select, desc

from app.base_dao import BaseDAO
from app.business_logic.messages.models import Message
from app.database import async_session_maker


class MessagesDAO(BaseDAO):
    model = Message

    @classmethod
    async def load_chat_history(cls, chat_id: str, messages_count: int):
        async with async_session_maker() as session:
            query = (
                select(cls.model)
                .where(cls.model.chat_id == chat_id)
                .order_by(desc(cls.model.created_at))
                .limit(messages_count)
            )
            result = await session.execute(query)
            messages = result.scalars().all()
            return list(reversed(messages))
