from fastapi import FastAPI                 
from app.todo.models import *               
from app.todo.routers import api_router         
from app.auth.routers import api_auth        
from app.utils.db import Base,db_init       

app = FastAPI()                             

app.include_router(api_router)        
app.include_router(api_auth)                

Base.metadata.create_all(bind=db_init)      

@app.get("/test")                           
def home():
    return {"message": "welcome to Todolist"}
