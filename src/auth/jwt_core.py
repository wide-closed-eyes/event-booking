from datetime import timedelta
from typing import Union

import jwt
import bcrypt
from src.config import settings


class JWTAuthenticator:
    @staticmethod
    def jwt_encode(
            payload: dict,
            private_key: str = settings.PRIVATE_KEY_PATH.read_text(),
            algorithm: str = settings.ALG,
            expire_minutes: int = settings.ACCESS_TOKEN_EXPIRE_MINUTES
    ) -> str:
        now = payload["la"]
        to_encode = payload.copy()
        to_encode.update(
            exp=(now + timedelta(minutes=expire_minutes)).timestamp(),
            iat=now.timestamp()
        )
        to_encode.pop("la")
        encoded = jwt.encode(to_encode, private_key, algorithm=algorithm)
        return encoded

    @staticmethod
    def jwt_decode(
            token: Union[str, bytes],
            public_key: str = settings.PUBLIC_KEY_PATH.read_text(),
            algorithm: str = settings.ALG
    ) -> dict:
        decoded = jwt.decode(token, public_key, algorithms=[algorithm])
        return decoded

    @staticmethod
    def hash_password(password: str) -> bytes:
        hashed_password = bcrypt.hashpw(password.encode(), settings.SALT)
        return hashed_password

    @staticmethod
    def verify_password(password: str, hashed_password: bytes) -> bool:
        return bcrypt.checkpw(password.encode(), hashed_password)
