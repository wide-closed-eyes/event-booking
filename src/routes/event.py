from fastapi import APIRouter, Depends, HTTPException

from src.database.main import EventWorker
from src.models.input import Event, UserSchema, Filter
from src.auth.tools import check_user_session


router = APIRouter()

@router.post("/create")
async def create_event(event: Event = Depends(Event), user: UserSchema = Depends(check_user_session)):
    return await EventWorker.add_event(event.model_dump())

@router.get("/current/{event_id}")
async def get_event(event_id: int, user: UserSchema = Depends(check_user_session)):
    event = await EventWorker.select_event(event_id)
    if not event:
        raise HTTPException(status_code=404, detail=f"event with id {event_id} does not exist")
    return event

@router.get("/list")
async def get_event_list(filters: Filter = Depends(Filter), user: UserSchema = Depends(check_user_session)):
    return await EventWorker.event_list(filters)

@router.post("/edit/{event_id}")
async def edit_event(event_id: int, event: Event = Depends(Event), user: UserSchema = Depends(check_user_session)):
    if not await EventWorker.edit_event(event_id, event.model_dump()):
        raise HTTPException(status_code=404, detail=f"event with id {event_id} does not exist")
    return "Ok"

@router.delete("/{event_id}")
async def delete_event(event_id: int, user: UserSchema = Depends(check_user_session)):
    if not await EventWorker.delete_event(event_id):
        raise HTTPException(status_code=404, detail=f"event with id {event_id} does not exist")
    return "Ok"