from sqlmodel import Field, Session, SQLModel, create_engine, select
from sqlalchemy import Column, Integer, String, Boolean
# from app.database.conf import Base
from pwdlib import PasswordHash, exceptions

password_hash = PasswordHash.recommended()


class UserBase(SQLModel):
    username: str = Field(sa_column=Column(String(50), unique=True, index=True))
    email: str | None = Field(sa_column=Column(String(50), unique=True, index=True))   
    # password: str | None = Field(sa_column=Column(String(50), unique=True, index=True))   

class User(UserBase, table=True):
    __tablename__ = "users"
    id: int | None = Field(default=None, primary_key=True)
    hashed_password: str = Field(sa_column=Column(String(50), unique=True, index=True))  
    disabled: bool = Field(default=0)
    
    def set_password(self, password):
        self.hashed_password = password_hash.hash(password)

    def check_password(self, password):
        # print(f"hashed password: {self.hashed_password}")
        # print(f"password: {password}")
        return password_hash.verify(password, self.hashed_password)
    
    def set_email(self, email):
        self.email = email

class UserPublic(UserBase):
    id: int
    
class UserUpdate(UserBase):
    name: str | None = None
    age: int | None = None
    hashed_password: str | None = None
    

    # id = Column(Integer, primary_key=True, index=True)
    # username = Column(String(50), unique=True, index=True)
    # email = Column(String(100), unique=True, index=True)
    # hashed_password = Column(String(255))
    # disabled = Column(bool)