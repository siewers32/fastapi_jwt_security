import os
from typing import Annotated
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from sqlmodel import Field, Session, SQLModel, create_engine, select
import jwt
from jwt.exceptions import InvalidTokenError
from app.models.user import User, UserBase
from app.models.token import Token, TokenData
from app.database.conf import SessionDep, create_db_and_tables

from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv

load_dotenv()

ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_current_user(session: SessionDep, token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except InvalidTokenError:
        raise credentials_exception
    user =  session.query(User).filter(User.username == username).first()
    if user is None:
        raise credentials_exception
    return user
    
@app.on_event("startup")
def on_startup():
    create_db_and_tables()
    
@app.post("/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: SessionDep
) -> Token:
    user =  authenticate_user(session, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")


# @app.get("/users/me/", response_model=User)
# async def read_users_me(
#     current_user: Annotated[User, Depends(get_current_active_user)],
# ):
#     return current_user



# @app.get("/users/me/items/")
# async def read_own_items(
#     current_user: Annotated[User, Depends(get_current_active_user)],
# ):
#     return [{"item_id": "Foo", "owner": current_user.username}]

@app.post("/users/")
def create_user(user: User, session: SessionDep) -> User:
    new_user = User(username=user.username, email=user.email, disabled=0)
    new_user.set_password(user.hashed_password)
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    return new_user

@app.get("/users/")
def read_users(session: SessionDep) -> list[User]:
    users = session.exec(select(User)).all()
    return users

@app.get("/users/{user_id}")
def read_user(user_id: int, session: SessionDep) -> User:
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.get("/users/byname/{username}")
def read_user_by_username(username: str, session: SessionDep) -> UserBase:
    user =  session.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.get("/geheim")
def geheim(token: str = Depends(get_current_user)):
    return "Dit is geheim!"
    
# def get_user_by_username(session: SessionDep, username: str):
#     user =  session.query(User).filter(User.username == username).first()
#     if user:
#         return user
#     else:
#         return None
    
def authenticate_user(session: SessionDep, username: str, password: str):
    user =  session.query(User).filter(User.username == username).first()
    if not user:
        return False
    if not user.check_password(password):
        return False
    return user

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

