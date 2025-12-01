from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.utils.db import get_db
from app.todo.controller import *
from app.todo.dtos import UserSchema, TodoSchema
from app.utils.helper import is_authenticated
from datetime import date

api_router = APIRouter(prefix="/api")



@api_router.get("/todos-date-filter")
def api_get_todos_by_date( start_date:date=None, end_date: date=None, db: Session = Depends(get_db),user:User=Depends(is_authenticated)):
    return get_todos_by_date(user, db, start_date, end_date)


# def api_get_todos_by_date(
#     user_id: int,
#     start_date: str = None,
#     end_date: str = None,
#     db: Session = Depends(get_db)
# ):
#     return get_todos_by_date(user_id, db, start_date, end_date)


@api_router.get("/todos/alphabetical")
def api_get_todos_alphabetically(user_id: int, db: Session = Depends(get_db)):
    return get_todos_alphabetically(user_id, db)


# -------- User Endpoints --------

@api_router.post("/users")
def api_create_user(body: UserSchema, db: Session = Depends(get_db)):
    return create_user(body, db)

@api_router.get("/users")
def api_get_users(db: Session = Depends(get_db),user:User=Depends(is_authenticated)):
    return get_user(db,user)


@api_router.put("/users")
def api_update_user(body:UserSchema,db:Session=Depends(get_db),user:User=Depends(is_authenticated)):
    return update_user(user, body, db)

@api_router.delete("/users")
def api_delete_user(db:Session=Depends(get_db),user:User=Depends(is_authenticated)):
    return delete_user(user, db)

# -------- Todo Endpoints --------

@api_router.post("/todos")
def api_create_todo(body: TodoSchema, db: Session = Depends(get_db),user:User=Depends(is_authenticated)):
    return create_todo(body, db,user)

@api_router.get("/todos")
def api_get_todos(user:User=Depends(is_authenticated),db: Session = Depends(get_db)):
    return get_todo(db, user)


@api_router.put("/todos/{id}")
def api_update_todo(todo_id: int, body: TodoSchema, db: Session = Depends(get_db),user:User=Depends(is_authenticated)):
    return update_todo(db, todo_id, body,user)

@api_router.delete("/todos/{id}")
def api_delete_todo(todo_id: int, db: Session = Depends(get_db),user:User=Depends(is_authenticated)):
    return delete_todo(db, user, todo_id)