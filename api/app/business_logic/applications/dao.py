from sqlalchemy import select, func, desc

from app.base_dao import BaseDAO
from app.business_logic.applications.models import Application
from app.business_logic.users.models import User
from app.database import async_session_maker


class ApplicationsDAO(BaseDAO):
    model = Application

    @classmethod
    async def find_all(cls, creator_id: int):
        async with async_session_maker() as session:
            stmt = (
                select(
                    cls.model,
                    func.count(User.id).label("users_count")
                )
                .outerjoin(User, User.auth_provider == cls.model.auth_provider_name)
                .where(cls.model.creator_id == creator_id)
                .group_by(cls.model.id)
                .order_by(desc(cls.model.updated_at))
            )
            result = await session.execute(stmt)
            return [
                {
                    **{
                        k: v for k, v in app.__dict__.items()
                        if not k.startswith('_')
                    },
                    "users_count": users_count
                }
                for app, users_count in result.all()
            ]
