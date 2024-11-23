from src.database.queries.orm import ASyncORM
from fastapi import HTTPException

async def create_tables():
    return await ASyncORM.create_tables()

class UserWorker:
    @staticmethod
    async def add_user(user: dict):
        if await ASyncORM.select_user(user["email"]):
            raise HTTPException(status_code=404, detail=f"User with email {user["email"]} already exist")
        return await ASyncORM.insert_user(user)
    
    @staticmethod
    async def login_user(user_id: int):
        return await ASyncORM.login_user(user_id)
    
    @staticmethod
    async def select_user(login: str):
        return await ASyncORM.select_user(login)
    
    @staticmethod
    async def select_current_user(user_id: int):
        return await ASyncORM.select_current_user(user_id)
    

class EventWorker:
    @staticmethod
    async def add_event(event: dict):
        return await ASyncORM.insert_event(event)
    
    @staticmethod
    async def select_event(event_id: int):
        return await ASyncORM.select_event(event_id)
    
    @staticmethod
    async def event_list(filters):
        return await ASyncORM.event_list(filters)
    
    @staticmethod
    async def edit_event(event_id: int, event: dict):
        return await ASyncORM.edit_event(event_id, event)
    
    @staticmethod
    async def delete_event(event_id: int):
        return await ASyncORM.delete_event(event_id)