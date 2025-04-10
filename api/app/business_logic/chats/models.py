import json
import uuid

from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Chat(Base):
    __tablename__ = 'chats'
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=False)

    user: Mapped['User'] = relationship('User', back_populates='chats')

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
