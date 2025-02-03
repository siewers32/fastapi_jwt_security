import os

# Definitie van de mappenstructuur
folders = [
    "fastapi_app/app",
    "fastapi_app/app/api/v1/endpoints",
    "fastapi_app/app/core",
    "fastapi_app/app/models",
    "fastapi_app/app/schemas",
    "fastapi_app/app/crud",
    "fastapi_app/app/services",
    "fastapi_app/app/tests",
    "fastapi_app/alembic",
]

# Bestanden die we willen aanmaken
files = {
    "fastapi_app/.env": "DATABASE_URL=mysql+pymysql://user:password@localhost/dbname\nSECRET_KEY=your_secret_key",
    "fastapi_app/.gitignore": "__pycache__/\n.env",
    "fastapi_app/requirements.txt": "fastapi\nuvicorn\nsqlalchemy\npydantic\nalembic\npasslib[bcrypt]\npython-jose[cryptography]\nPyMySQL\npython-dotenv",
    "fastapi_app/README.md": "# FastAPI Project\n\nThis is a FastAPI project setup.",
    "fastapi_app/app/main.py": "from fastapi import FastAPI\n\napp = FastAPI()\n\n@app.get('/')\ndef home():\n    return {'message': 'Hello FastAPI!'}",
    "fastapi_app/app/core/config.py": "import os\nfrom dotenv import load_dotenv\n\nload_dotenv()\nDATABASE_URL = os.getenv('DATABASE_URL')\nSECRET_KEY = os.getenv('SECRET_KEY')",
    "fastapi_app/app/core/database.py": """from sqlalchemy import create_engine\nfrom sqlalchemy.orm import sessionmaker, declarative_base\nimport os\n\nDATABASE_URL = os.getenv('DATABASE_URL')\n\nengine = create_engine(DATABASE_URL, pool_pre_ping=True)\nSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)\nBase = declarative_base()\n\ndef get_db():\n    db = SessionLocal()\n    try:\n        yield db\n    finally:\n        db.close()""",
    "fastapi_app/app/models/user.py": """from sqlalchemy import Column, Integer, String\nfrom app.core.database import Base\n\nclass User(Base):\n    __tablename__ = 'users'\n    id = Column(Integer, primary_key=True, index=True)\n    username = Column(String(50), unique=True, index=True)\n    email = Column(String(100), unique=True, index=True)\n    hashed_password = Column(String(255))""",
    "fastapi_app/app/schemas/user.py": """from pydantic import BaseModel, EmailStr\nfrom typing import Optional\n\nclass UserCreate(BaseModel):\n    username: str\n    email: EmailStr\n    password: str\n\nclass UserResponse(BaseModel):\n    id: int\n    username: str\n    email: EmailStr\n\n    class Config:\n        orm_mode = True\n\nclass UserLogin(BaseModel):\n    email: EmailStr\n    password: str\n\nclass UserUpdate(BaseModel):\n    username: Optional[str] = None\n    email: Optional[EmailStr] = None\n    password: Optional[str] = None""",
    "fastapi_app/app/api/v1/endpoints/users.py": """from fastapi import APIRouter, Depends, HTTPException\nfrom sqlalchemy.orm import Session\nfrom typing import List\nfrom app.schemas.user import UserCreate, UserResponse, UserUpdate\nfrom app.crud.user import create_user, get_user_by_id, get_users, update_user\nfrom app.core.database import get_db\n\nrouter = APIRouter()\n\n@router.post('/', response_model=UserResponse)\ndef register_user(user: UserCreate, db: Session = Depends(get_db)):\n    return create_user(db, user)\n\n@router.get('/{user_id}', response_model=UserResponse)\ndef get_user(user_id: int, db: Session = Depends(get_db)):\n    user = get_user_by_id(db, user_id)\n    if not user:\n        raise HTTPException(status_code=404, detail='User not found')\n    return user""",
    "fastapi_app/app/api/v1/endpoints/auth.py": """from fastapi import APIRouter, Depends, HTTPException\nfrom sqlalchemy.orm import Session\nfrom fastapi.security import OAuth2PasswordRequestForm\nfrom datetime import timedelta\nfrom app.core.security import create_access_token, verify_password\nfrom app.core.config import ACCESS_TOKEN_EXPIRE_MINUTES\nfrom app.schemas.user import UserLogin\nfrom app.models.user import User\nfrom app.crud.user import get_user_by_email\nfrom app.core.database import get_db\n\nrouter = APIRouter()\n\n@router.post('/login')\ndef login_user(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):\n    user = get_user_by_email(db, form_data.username)\n    if not user or not verify_password(form_data.password, user.hashed_password):\n        raise HTTPException(status_code=401, detail='Incorrect email or password')\n    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)\n    access_token = create_access_token(data={'sub': user.email}, expires_delta=access_token_expires)\n    return {'access_token': access_token, 'token_type': 'bearer'}"""
}

# Folders aanmaken
for folder in folders:
    os.makedirs(folder, exist_ok=True)

# Bestanden aanmaken met inhoud
for file, content in files.items():
    with open(file, "w", encoding="utf-8") as f:
        f.write(content)

print("✅ FastAPI folderstructuur en basisbestanden aangemaakt!")
