import uuid

from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import Enum as SQLEnum

from app.business_logic.messages.enums import MessageSender
from app.database import Base


class Message(Base):
    __tablename__ = 'messages'
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    text_content: Mapped[str] = mapped_column(nullable=False)
    sender: Mapped[MessageSender] = mapped_column(SQLEnum(MessageSender, name='message_sender'),
                                                  nullable=False)
    chat_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('chats.id'), nullable=False)

    chat: Mapped['Chat'] = relationship('Chat', back_populates='messages')
