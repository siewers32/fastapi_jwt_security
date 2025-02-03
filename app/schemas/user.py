from pydantic import BaseModel


class User(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None

    class Config:
        orm_mode = True  # Belangrijk voor SQLAlchemy conversie
        
class UserCreate(User):
    hashed_password: str