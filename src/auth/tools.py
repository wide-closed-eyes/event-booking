from fastapi import Form, HTTPException, status, Response, Request

from src.auth.token_validator import TokenValidator
from src.auth.jwt_core import JWTAuthenticator
from src.auth.token import TokenGenerator
from src.models.input import UserSchema
from src.database.main import UserWorker
from src.config import settings

from datetime import datetime as dt, timezone, timedelta


async def validate_auth_user(login: str = Form(), password: str = Form()):
    unauthorized_exc = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid username or password")
    if not (user := await UserWorker.select_user(login)):
        raise unauthorized_exc
    if not JWTAuthenticator.verify_password(password=password, hashed_password=user["password"]):
        raise unauthorized_exc
    user["logged_at"] = await UserWorker.login_user(user["id"])
    return user


async def check_user_session(response: Response, request: Request) -> UserSchema:
    if "access" not in request.cookies.keys():
        if "refresh" not in request.cookies.keys():
            raise HTTPException(status_code=401, detail="Not Authenticated")
        payload = TokenValidator.get_current_token_payload(request.cookies["refresh"])
        user = await TokenValidator.get_current_auth_user_refresh(payload)
        user["logged_at"] = dt.now()
        response.set_cookie(
                key="access",
                value=TokenGenerator().create_access_token(user),
                expires=dt.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
                path="/api",
                secure=False,
                httponly=True,
                samesite='strict'  
            )
        return user
    payload = TokenValidator.get_current_token_payload(request.cookies["access"])
    return await TokenValidator.get_current_auth_user(payload=payload)
