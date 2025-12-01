from sqlalchemy import Column, Integer, String, ForeignKey, Date
from app.utils.db import Base

class User(Base):
    __tablename__ = "users"   

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True)
    username = Column(String, unique=True)
    hass_password = Column(String)           
    mobile = Column(Integer, unique=True)


class Todo(Base):
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True)
    title = Column(String)
    description = Column(String)
    priority = Column(String)
    start_date = Column(Date)
    end_date = Column(Date)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

