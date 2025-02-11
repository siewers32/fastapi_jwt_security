import os
from dotenv import load_dotenv
import pymysql
from typing import Annotated
from sqlmodel import Field, Session, SQLModel, create_engine, select
from fastapi import Depends, FastAPI, HTTPException, Query


load_dotenv()

DATABASE_URL = f"mariadb+pymysql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_DATABASE')}"
# connect_args = {"check_same_thread": False}
engine = create_engine(DATABASE_URL)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session    

SessionDep = Annotated[Session, Depends(get_session)]

# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()
