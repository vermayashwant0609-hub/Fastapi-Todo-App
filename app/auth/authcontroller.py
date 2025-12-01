from datetime import datetime, timedelta, timezone
from fastapi import HTTPException
import jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from app.auth.dtos import UserLoginSchema
from app.todo.models import User

SECRET_KEY = "TYUIK345678DSVBN56789ODHSFGHJK890OJN"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)



def get_user_by_username(username: str, db: Session):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        return None
    return user



def login(body: UserLoginSchema, db: Session):
    currentUser = get_user_by_username(body.username, db)
    if not currentUser:
        raise HTTPException(status_code=404, detail={"error": "User not found"})
    
    verify_pass = verify_password(body.password, currentUser.hass_password)
    if not verify_pass:
        raise HTTPException(status_code=404, detail={"error": "Password incorrect"})
    
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    token = jwt.encode({"username": currentUser.username, "exp": expire}, SECRET_KEY, algorithm=ALGORITHM)
    
    return {"token": token, "message": "You logged in successfully!"}



def userProfile(db: Session, user: User):
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "mobile": user.mobile,
        "name": user.name
    }
