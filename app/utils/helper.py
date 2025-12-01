from fastapi import Request, HTTPException, status, Depends
import jwt
from sqlalchemy.orm import Session
from app.auth.authcontroller import SECRET_KEY, ALGORITHM, get_user_by_username
from app.utils.db import get_db

def is_authenticated(req: Request, db: Session = Depends(get_db)):
    token = req.headers.get("authorization")
    if not token:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail={"error": "You are not authorized"})

    token = token.split(" ")[-1]

    try:
        data = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except jwt.PyJWTError:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail={"error": "Invalid token"})

    if not data.get("username"):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail={"error": "You are not authorized"})

    user = get_user_by_username(data.get("username"), db)
    if not user:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail={"error": "You are not authorized"})

    return user