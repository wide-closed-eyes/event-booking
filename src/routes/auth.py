from datetime import datetime as dt, timedelta, timezone

from fastapi import APIRouter, Depends, Response, Request, HTTPException
from fastapi.security import HTTPBearer

from src.auth.token import TokenGenerator
from src.models.input import UserSchema, UserCreate
from src.auth.tools import check_user_session, validate_auth_user
from src.database.main import UserWorker
from src.config import settings


http_bearer = HTTPBearer(auto_error=False)

router = APIRouter(dependencies=[Depends(http_bearer)])


@router.post("/reg")
async def reg_user(user_data: UserCreate):
    return await UserWorker.add_user(user_data.model_dump())


@router.post("/login")
async def auth_login(response: Response, request: Request, user: UserSchema = Depends(validate_auth_user)):
    access_token = TokenGenerator().create_access_token(user)
    refresh_token = TokenGenerator().create_refresh_token(user)
    
    response.set_cookie(
        key="access",
        value=access_token,
        httponly=True,
        secure=False,
        path="/api",
        samesite="strict", 
        expires=dt.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
    )
    response.set_cookie(
        key="refresh",
        value=refresh_token,
        httponly=True,
        secure=False,
        path="/api",
        samesite="strict", 
        expires=dt.now(timezone.utc) + timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES),
    )
    return "Ok"


@router.get("/me")
async def auth_user_check_self_info(
        user: UserSchema = Depends(check_user_session)
):
    return await UserWorker.select_current_user(user["id"])