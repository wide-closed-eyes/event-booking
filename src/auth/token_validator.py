from typing import Union

from fastapi import Depends, HTTPException, Cookie
from jwt import InvalidTokenError
from starlette import status

from src.auth.jwt_core import JWTAuthenticator
from src.auth.token import TokenGenerator
from src.database.main import UserWorker
from src.models.input import UserSchema


class TokenValidator:
    def get_current_token_payload(access: str = Cookie(None)) -> dict:
        token = access
        try:
            payload = JWTAuthenticator.jwt_decode(token=token)
        except InvalidTokenError as e:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"invalid token error: {e}")
        return payload

    async def get_current_auth_user(payload: dict = Depends(get_current_token_payload)) -> UserSchema:
        token_type = payload.get(TokenGenerator.TOKEN_TYPE_FIELD)
        if token_type != TokenGenerator.ACCESS_TOKEN_TYPE:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail=f"invalid token type: {token_type} expected {TokenGenerator.ACCESS_TOKEN_TYPE}")
        user_id: Union[str, None] = payload.get("sub")
        if user := await UserWorker.select_current_user(user_id=user_id):
            return user
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="token invalid (user not found)")

    async def get_current_auth_user_refresh(payload: dict = Depends(get_current_token_payload)) -> UserSchema:
        token_type = payload.get(TokenGenerator.TOKEN_TYPE_FIELD)
        if token_type != TokenGenerator.REFRESH_TOKEN_TYPE:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail=f"invalid token type: {token_type} expected {TokenGenerator.REFRESH_TOKEN_TYPE}")
        user_id = payload.get("sub")
        if user := await UserWorker.select_current_user(user_id=user_id):
            return user
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="token invalid (user not found)")
