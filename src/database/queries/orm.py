from datetime import datetime as dt, date
from sqlalchemy import select, update, text, and_

from src.database.database import async_session_fabric, async_engine
from src.database.models import Base, User, Event
from src.models.input import Filter


class ASyncORM:
    @staticmethod
    async def is_table_empty(id: any, table):
        """
        Метод определяет наличие строки с заданным uid в заданной таблице table 
        """
        async with async_session_fabric() as session:
            res = await session.execute(select(table).filter(table.id == id))
            return res.scalars().first()
    

    @staticmethod
    async def create_tables():
       async with async_engine.begin() as conn: 
           await conn.run_sync(Base.metadata.create_all)
            
    
    @staticmethod
    async def insert_user(user: dict):
        async with async_session_fabric() as session:
            session.add(User(**user))
            await session.commit()
            return "Ok"
        
    @staticmethod
    async def login_user(user_id: int):
        async with async_session_fabric() as session:
            now = dt.now()
            query = (
                update(User)
                .filter(User.id == user_id)
                .values(
                    logged_at=now
                )
            )
            await session.execute(query)
            await session.commit()
        return now

    @staticmethod
    async def select_user(login: str):
        async with async_session_fabric() as session:
            result = await session.execute(select(User).where(User.email == login))
            user = result.scalars().first()
            if user: 
                return { 
                    "id": user.id, 
                    "name": user.name, 
                    "login": user.email,
                    "password": user.password
                }
            return user

    @staticmethod
    async def select_current_user(user_id):
        async with async_session_fabric() as session:
            result = await session.execute(select(User).where(User.id == int(user_id)))
            user = result.scalars().first()
            if user: 
                return { 
                    "id": user.id, 
                    "name": user.name, 
                    "login": user.email
                }
            return user
    
    @staticmethod
    async def insert_event(event: dict):
        async with async_session_fabric() as session:
            session.add(Event(**event))
            await session.commit()

    @staticmethod
    async def select_event(event_id):
        async with async_session_fabric() as session:
            res = await session.execute(select(Event).filter(Event.id == event_id))
            event = res.scalars().first()
            if not event:
                return None
            
            event.event_start_date = date.strftime(event.event_start_date, "%d/%m/%Y")
            event.event_end_date = date.strftime(event.event_end_date, "%d/%m/%Y")
            return event
        
    @staticmethod
    async def event_list(filters: Filter):
        async with async_session_fabric() as session:
            query = (
                select(Event)
                .filter(
                    and_(
                        Event.title.op('~*')(filters.title) if filters.title else text(""),
                        Event.event_start_date >= filters.start_date if filters.start_date else text(""),
                        Event.event_start_date <= filters.end_date if filters.end_date else text(""),
                    )
                )
            )
            res = await session.execute(query)
            if not res:
                return []
            events = res.scalars().all()
            for event in events:
                event.event_start_date = date.strftime(event.event_start_date, "%d/%m/%Y")
                event.event_end_date = date.strftime(event.event_end_date, "%d/%m/%Y")
            return events
        
    @staticmethod
    async def edit_event(event_id: int, event: dict):
        if not await ASyncORM.is_table_empty(event_id, Event):
            return None
        print(await ASyncORM.is_table_empty(event_id, Event))
        async with async_session_fabric() as session:
            query =(
                update(Event)
                .filter(Event.id == event_id)
                .values(**event)
            )
            await session.execute(query)
            await session.commit()
            return 1
        
    @staticmethod
    async def delete_event(event_id: int):
        async with async_session_fabric() as session:
            res = await session.execute(select(Event).filter(Event.id == event_id))
            event = res.scalars().first()
            if not event:
                return None
            await session.delete(event)
            await session.commit()
            return 1