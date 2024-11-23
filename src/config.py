from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict


BASE_DIR = Path(__file__).parent.parent


class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str

    PRIVATE_KEY_PATH: Path = BASE_DIR / "private.pem"
    PUBLIC_KEY_PATH: Path = BASE_DIR / "public.pem"
    ALG: str = "RS256"
    SALT: bytes = b'$2b$12$t8K.nEVBN9M.ewAhYQ1f8u'
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 10_080

    @property
    def DATABASE_URL_asyncpg(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    model_config = SettingsConfigDict(env_file=".env", extra='ignore')


settings = Settings()