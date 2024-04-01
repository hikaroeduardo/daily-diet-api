from typing import List
from database import db
from sqlalchemy import Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from flask_login import UserMixin
import datetime

class User(db.Model, UserMixin):
    __tablename__ = "user"

    id = mapped_column(Integer, primary_key=True)
    name = mapped_column(String(80), nullable=False)
    email = mapped_column(String(80), nullable=False, unique=True)
    password = mapped_column(String(80), nullable=False)

    foods: Mapped[List["Food"]] = relationship(back_populates="user", cascade="all, delete-orphan")

class Food(db.Model, UserMixin):
    __tablename__ = "food"

    id = mapped_column(Integer, primary_key=True)
    name = mapped_column(String(20), nullable=False)
    description = mapped_column(String(100))
    date = mapped_column(DateTime, default=datetime.datetime.now)
    user_id = mapped_column(Integer, ForeignKey("user.id"))

    user: Mapped["User"] = relationship(back_populates="foods")