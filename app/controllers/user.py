from sqlalchemy.orm import Session
from app.models import user as user_model
from app.schemas import user as user_schema
from app.database.conf import Base

def get_user(db: Session, user_id: int):
    db_user = db.query(user_model.User).filter(user_model.User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

def get_user_by_username(db: Session, username: str):
    user =  db.query(user_model.User).filter(user_model.User.username == username).first()
    if user:
        return user
    else:
        return None

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(user_model.User).offset(skip).limit(limit).all()

def create_user(db: Session, user: user_schema.UserCreate):
    # bytes = user.password.encode('utf-8')   
    # # generating the salt 
    # salt = bcrypt.gensalt()   
    # # Hashing the password 
    hashed_password = get_password_hash(user.password)  
    db_user = user_model.User(username=user.username, email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user