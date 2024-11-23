from datetime import datetime as dt
from src.database.database import Base
from sqlalchemy import (Integer, String, Date, SmallInteger,
                        LargeBinary)
from sqlalchemy.orm import Mapped, mapped_column


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    logged_at: Mapped[dt] = mapped_column(Date, nullable=True, default=None)
    password: Mapped[bytes] = mapped_column(LargeBinary, nullable=False)


class Event(Base):
    __tablename__ = "event"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(String(500), nullable=True)
    event_start_date: Mapped[dt] = mapped_column(Date, nullable=False, default=dt.now())
    event_end_date: Mapped[dt] = mapped_column(Date, nullable=False, default=dt.now())
    place_count: Mapped[int] = mapped_column(SmallInteger, nullable=False, default=0)
