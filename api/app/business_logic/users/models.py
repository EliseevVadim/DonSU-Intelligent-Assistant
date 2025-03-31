import json
from typing import Optional

from sqlalchemy import CheckConstraint, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base, str_unique, int_primary


class User(Base):
    __tablename__ = 'users'
    id: Mapped[int_primary]
    first_name: Mapped[str] = mapped_column(nullable=False)
    last_name: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str_unique]
    password: Mapped[str] = mapped_column(nullable=False)
    auth_provider: Mapped[str] = mapped_column(nullable=True)
    reset_token: Mapped[str] = mapped_column(nullable=True)
    reset_token_expires_at: Mapped[Optional[DateTime]] = mapped_column(DateTime, nullable=True)
    __table_args__ = (
        CheckConstraint("LENGTH(password) >= 8", name="password_min_length"),
    )

    def __str__(self):
        return json.dumps({
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "auth_provider": self.auth_provider,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }, ensure_ascii=False)

    def __repr__(self):
        return (f"User(id={self.id}, first_name='{self.first_name}', "
                f"last_name='{self.last_name}', email='{self.email}', "
                f"auth_provider='{self.auth_provider}', "
                f"created_at={self.created_at}, updated_at={self.updated_at})")
