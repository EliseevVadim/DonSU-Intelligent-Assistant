import json

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base, int_primary, str_unique


class Application(Base):
    __tablename__ = 'applications'
    id: Mapped[int_primary]
    name: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=True)
    auth_provider_name: Mapped[str_unique]
    app_key: Mapped[str_unique]
    creator_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=False)

    user: Mapped['User'] = relationship('User', back_populates='apps')

    def __str__(self):
        return json.dumps({
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "creator_id": self.creator_id,
            "auth_provider_name": self.auth_provider_name,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }, ensure_ascii=False)

    def __repr__(self):
        return (f"Application(id={self.id}, name='{self.name}', "
                f"description={self.description}, creator_id={self.creator_id})"
                f"auth_provider_name='{self.auth_provider_name}', "
                f"created_at={self.created_at}, updated_at={self.updated_at})")
