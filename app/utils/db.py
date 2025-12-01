from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import create_engine


Base = declarative_base()

db_url = "sqlite:///Todo.db"
db_init = create_engine(db_url)

LocalSession = sessionmaker(bind=db_init)

def get_db():
    db = LocalSession()
    try:
        yield db
    finally:
        db.close()
