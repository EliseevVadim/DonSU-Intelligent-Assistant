from datetime import datetime
from typing import Annotated

from sqlalchemy import func
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, declared_attr, Mapped, mapped_column
from app.config import get_assistant_db_connection_string, get_knowledge_base_connection_string

ASSISTANT_CONNECTION_STRING = get_assistant_db_connection_string()
engine = create_async_engine(ASSISTANT_CONNECTION_STRING)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)

KNOWLEDGE_BASE_CONNECTION_STRING = get_knowledge_base_connection_string()
knowledge_engine = create_async_engine(KNOWLEDGE_BASE_CONNECTION_STRING)
knowledge_session = async_sessionmaker(knowledge_engine, expire_on_commit=False)

int_primary = Annotated[int, mapped_column(primary_key=True, autoincrement=True)]
created_at = Annotated[datetime, mapped_column(server_default=func.now())]
updated_at = Annotated[datetime, mapped_column(server_default=func.now(), onupdate=datetime.now)]
str_unique = Annotated[str, mapped_column(unique=True, nullable=False)]
str_nullable = Annotated[str, mapped_column(nullable=True)]


class Base(AsyncAttrs, DeclarativeBase):
    __abstract__ = True

    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]

    @declared_attr.directive
    def __tablename__(self) -> str:
        return f"{self.__name__.lower()}s"


class EmbeddingBase(DeclarativeBase):
    pass
