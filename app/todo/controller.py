from sqlalchemy.orm import Session
from app.todo.models import Todo, User
from app.todo.dtos import TodoSchema, UserSchema
from fastapi import HTTPException, status
from datetime import datetime
from passlib.context import CryptContext
from datetime import date



# Get todos filtered by date range (start_date and end_date are strings "YYYY-MM-DD")
def get_todos_by_date(user:User, db:Session, start_date:date=None, end_date:date=None):
    todos = db.query(Todo).filter(Todo.user_id == user.id).all()

    # Date conversion & error check
    # start, end = None, None
    # try:
    #     if start_date:
    #         start = datetime.strptime(start_date, "%Y-%m-%d").date()
    #     if end_date:
    #         end = datetime.strptime(end_date, "%Y-%m-%d").date()
    # except ValueError:
    #     raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD.")

    # Filter todos on all 3 conditions
    
    if start_date and end_date:
        filtered_todos = [todo for todo in todos if todo.start_date >= start_date and todo.end_date <= end_date]
    elif start_date:
        filtered_todos = [todo for todo in todos if todo.start_date >= start_date]
    elif end_date:
        filtered_todos = [todo for todo in todos if todo.end_date <= end_date]

    return {"status": "OK", "todos": filtered_todos}
         


# Get todos sorted alphabetically by title
def get_todos_alphabetically(user:User, db: Session):
    todos = db.query(Todo).filter(Todo.user_id == user.id).all()
    if not todos:
             raise HTTPException ( status_code=status.HTTP_404_NOT_FOUND,
            detail="No todos found for this user")
    
    sorted_todos = sorted(todos, key=lambda t: t.title.lower())
    return {"status": "OK", "todos": sorted_todos}


#-----------------User-------------------

pwd_context=CryptContext(schemes=["bcrypt"],deprecated="auto")

def get_password_hash(password):
    return pwd_context.hash(password)



def create_user(body: UserSchema, db: Session):
    existing_user = db.query(User).filter(User.username == body.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")
    
    hp = get_password_hash(body.password)

    new_user=User(username=body.username,
                 hass_password=hp,
                 email=body.email,
                 mobile=body.mobile,
                 name=body.name)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"status": "OK", "user": new_user}



def get_user(db: Session, user:User):
        
        todos = db.query(Todo).filter(Todo.user_id ==user.id).all()

        return {
            "user": {
                "id": user.id,
                "name": user.name,
                "email": user.email,
                "username": user.username,
                "mobile": user.mobile,
            },
            "todos": todos
        }


def update_user(user:User, body: UserSchema, db: Session):
    user = db.query(User).filter(User.id == user.id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.name = body.name
    user.email = body.email
    user.username = body.username
    user.mobile = body.mobile
    user.password=pwd_context.hash(body.password)
    db.commit()
    db.refresh(user)
    return {"status": "OK", "user": user}


def delete_user(user: User, db: Session):
    db.delete(user)
    db.commit()
    return {"status": "OK","message": "User deleted successfully"}


#-----------------Todo-------------------

def create_todo(body: TodoSchema, db: Session,user:User):
    new_todo = Todo(
         description=body.description,
         priority=body.priority,
         start_date=body.start_date,
         end_date=body.end_date,
         user_id=user.id
    )
    db.add(new_todo)
    db.commit()
    db.refresh(new_todo)
    return {"status": "OK", "todo": new_todo}



def get_todo(db: Session, user:User):
        todo = db.query(Todo).filter(Todo.id == user.id).first()
        if not todo:
            raise HTTPException(status_code=404, detail="Todo not found")
        return {"status": "OK", "todo": todo}
    

    
def update_todo(todo_id:int,body:TodoSchema,db:Session,user:User):
    todo=db.query(Todo).filter(Todo.id==todo_id,Todo.user_id==user.id).first()
    if not todo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")

    todo.description = body.description
    todo.priority = body.priority
    todo.start_date = body.start_date
    todo.end_date = body.end_date

    db.commit()
    db.refresh(todo)
    return {"status": "OK", "todo": todo}



def delete_todo(db: Session, todo_id: int,user:User):
    todo = db.query(Todo).filter(Todo.id == todo_id, Todo.user_id == user.id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    db.delete(todo)
    db.commit()
    return {"status": "OK", "message": "Todo deleted successfully"}
