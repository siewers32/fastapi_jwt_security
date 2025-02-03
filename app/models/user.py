from sqlmodel import Field, Session, SQLModel, create_engine, select
from app.database.conf import Base

class User(SQLModel, table=True):
    __tablename__ = "users"
    id: int | None = Field(default=None, primary_key=True)
    username: str = Field(index=True)
    email: str | None = Field(default=None, index=True)
    hashed_password: str 
    disabled: bool = Field(default=0)


    # id = Column(Integer, primary_key=True, index=True)
    # username = Column(String(50), unique=True, index=True)
    # email = Column(String(100), unique=True, index=True)
    # hashed_password = Column(String(255))
    # disabled = Column(bool)