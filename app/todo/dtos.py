from pydantic import BaseModel
from datetime import date
from typing import Literal

class UserSchema(BaseModel):
    name: str
    email: str
    username: str
    mobile: int
    password: str

class TodoSchema(BaseModel):
    title:str
    description: str
    priority: Literal["Low", "Medium", "High"]  
    start_date: date
    end_date: date
