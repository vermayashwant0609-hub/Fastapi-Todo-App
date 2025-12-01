from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.utils.db import get_db
from app.auth.dtos import UserLoginSchema
from app.auth.authcontroller import login, userProfile
from app.todo.models import User
from app.utils.helper import is_authenticated

api_auth = APIRouter(prefix="/auth")

@api_auth.get("/login")
def loginUser(body: UserLoginSchema, db: Session = Depends(get_db)):
    return login(body, db)

@api_auth.get("/user")
def getUserProfile(db: Session = Depends(get_db), user: User = Depends(is_authenticated)):
    return userProfile(db, user)
