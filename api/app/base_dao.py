from sqlalchemy import select, update, delete, func
from sqlalchemy.exc import SQLAlchemyError

from app.database import async_session_maker


class BaseDAO:
    model = None

    @classmethod
    async def find_by_id(cls, data_id: int):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(id=data_id)
            result = await session.execute(query)
            return result.scalar_one_or_none()

    @classmethod
    async def find_one(cls, **fileter_by):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(**fileter_by)
            result = await session.execute(query)
            return result.scalar_one_or_none()

    @classmethod
    async def find_all(cls, **fileter_by):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(**fileter_by)
            result = await session.execute(query)
            return result.scalars().all()

    @classmethod
    async def find_all_paginated(cls, limit: int = 10, offset: int = 0, search_query: str = None, **filter_by):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(**filter_by).limit(limit).offset(offset)
            if search_query:
                query = query.filter(func.lower(cls.model).ilike(search_query))
            result = await session.execute(query)
            items = result.scalars().all()

            count_query = select(func.count()).select_from(cls.model).filter_by(**filter_by)
            if search_query:
                count_query = count_query.filter(func.lower(cls.model).ilike(search_query))
            total_result = await session.execute(count_query)
            total = total_result.scalar()
        return items, total

    @classmethod
    async def add(cls, **data):
        async with async_session_maker() as session:
            async with session.begin():
                new_record = cls.model(**data)
                session.add(new_record)
                try:
                    await session.commit()
                except SQLAlchemyError as e:
                    await session.rollback()
                    raise e
                return new_record

    @classmethod
    async def add_many(cls, instances: list[dict]):
        async with async_session_maker() as session:
            async with session.begin():
                new_records = [cls.model(**instance) for instance in instances]
                session.add_all(new_records)
                try:
                    await session.commit()
                except SQLAlchemyError as e:
                    await session.rollback()
                    raise e
                return new_records

    @classmethod
    async def update(cls, filter_by, **data):
        async with async_session_maker() as session:
            async with session.begin():
                query = (
                    update(cls.model)
                    .where(*[getattr(cls.model, k) == v for k, v in filter_by.items()])
                    .values(**data)
                    .execution_options(synchronize_session='fetch')
                )
                result = await session.execute(query)
                try:
                    await session.commit()
                except SQLAlchemyError as e:
                    await session.rollback()
                    raise e
                return result.rowcount

    @classmethod
    async def delete(cls, delete_all: bool = False, **filter_by):
        if delete_all is False:
            if not filter_by:
                raise ValueError("Не указаны параметры для удаления")
        async with async_session_maker() as session:
            async with session.begin():
                query = delete(cls.model).filter_by(**filter_by)
                result = await session.execute(query)
                try:
                    await session.commit()
                except SQLAlchemyError as e:
                    await session.rollback()
                    raise e
                return result.rowcount
