import json
import uuid
from datetime import datetime

from sqlalchemy import ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.business_logic.messages.models import Message
from app.database import Base


class Chat(Base):
    __tablename__ = 'chats'
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=False)
    last_context_reset_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    user: Mapped['User'] = relationship('User', back_populates='chats')
    messages: Mapped[list['Message']] = relationship('Message', back_populates='chat',
                                                     cascade='all, delete')

    def __str__(self):
        return json.dumps({
            "id": self.id,
            "name": self.name,
            "user_id": self.user_id,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }, ensure_ascii=False)

    def __repr__(self):
        return (f"Chat(id={self.id}, name='{self.name}', "
                f"user_id='{self.user_id}', "
                f"created_at={self.created_at}, updated_at={self.updated_at})")
