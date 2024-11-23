from datetime import datetime as dt
from pydantic_core.core_schema import FieldValidationInfo
from pydantic import BaseModel, ConfigDict, Field, EmailStr, field_validator
from typing import Union, Optional
import bcrypt
from src.config import settings

class TokenInfo(BaseModel):
    access_token: str
    refresh_token: Union[str, None] = None
    token_type: str
    

class UserSchema(BaseModel):
    model_config = ConfigDict(strict=True)
    id: int = Field(ge=1)
    logged_at: dt


class UserCreate(BaseModel):
    name: str = Field(min_length=3, max_length=100)
    email: EmailStr
    password: str = Field(min_length=4, max_length=32)

    @field_validator('password')
    @classmethod
    def passwd_hash(cls, v: str) -> bytes:
        return bcrypt.hashpw(v.encode(), salt=settings.SALT)
    

class Event(BaseModel):
    title: str = Field(min_length=3, max_length=100)
    description: str = Field(min_length=5, max_length=500)
    event_start_date: str = Field(min_length=10, max_length=10)
    event_end_date: str = Field(min_length=10, max_length=10)
    place_count: int = Field(ge=0, le=32_767)

    @field_validator('event_start_date')
    @classmethod
    def check_start_date(cls, v):
        try: 
            v = dt.strptime(v, '%d/%m/%Y') 
        except ValueError: 
            raise ValueError("Дата должна быть в формате dd/mm/yyyy")
        if v < dt.now():
            raise ValueError('Event datetime START less than NOW') 
        return v
    
    @field_validator('event_end_date')
    @classmethod
    def check_end_date(cls, v, info: FieldValidationInfo):
        try: 
            v = dt.strptime(v, '%d/%m/%Y') 
        except ValueError: 
            raise ValueError("Дата должна быть в формате dd/mm/yyyy")
        if 'event_start_date' in info.data and v <= info.data['event_start_date']: 
            raise ValueError('Event datetime END must be more than event datetime START') 
        return v
    

class Filter(BaseModel):
    title: Optional[str] = Field(default=None)
    start_date: Optional[str] = Field(default=None)
    end_date: Optional[str] = Field(default=None)

    @field_validator('start_date')
    @classmethod
    def check_start_date(cls, v):
        if not v:
            return v
        try: 
            v = dt.strptime(v, '%d/%m/%Y') 
        except ValueError: 
            raise ValueError("Дата должна быть в формате dd/mm/yyyy")
        return v
    
    @field_validator('end_date')
    @classmethod
    def check_end_date(cls, v, info: FieldValidationInfo):
        if not v:
            return v
        try: 
            v = dt.strptime(v, '%d/%m/%Y') 
        except ValueError: 
            raise ValueError("Дата должна быть в формате dd/mm/yyyy")
        if 'event_start_date' in info.data and v <= info.data['event_start_date']: 
            raise ValueError('Event datetime END must be more than event datetime START') 
        return v

