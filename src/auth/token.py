from src.auth.jwt_core import JWTAuthenticator
from src.config import settings
from src.models.input import UserSchema


class TokenGenerator:
    TOKEN_TYPE_FIELD = "type"
    ACCESS_TOKEN_TYPE = "access"
    REFRESH_TOKEN_TYPE = "refresh"

    def create_jwt(
            self,
            token_type: str,
            token_data: dict,
            expire_minutes: int = settings.ACCESS_TOKEN_EXPIRE_MINUTES
    ) -> str:
        jwt_payload = {self.TOKEN_TYPE_FIELD: token_type}
        jwt_payload.update(token_data)
        return JWTAuthenticator.jwt_encode(payload=jwt_payload, expire_minutes=expire_minutes)

    def create_access_token(self, user: UserSchema) -> str:
        jwt_payload = {
            "sub": str(user["id"]),
            "la": user["logged_at"]
        }
        return self.create_jwt(
            token_type=self.ACCESS_TOKEN_TYPE,
            token_data=jwt_payload,
            expire_minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )

    def create_refresh_token(self, user: UserSchema) -> str:
        jwt_payload = {
            "sub": str(user["id"]),
            "la": user["logged_at"]
        }
        return self.create_jwt(
            token_type=self.REFRESH_TOKEN_TYPE,
            token_data=jwt_payload,
            expire_minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES
        )
