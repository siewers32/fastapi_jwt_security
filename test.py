from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base
from pwdlib import PasswordHash, exceptions


#Passwords
password_hash = PasswordHash.recommended()
# password_hash.hash("password")
# password_hash.verify("password", "hash")


# Database configuratie
DB_USERNAME = 'web'  # Pas dit aan naar je database gebruiker
DB_PASSWORD = '230mod'  # Pas dit aan naar je wachtwoord
DB_HOST = 'localhost'  # Of een andere host als nodig
DB_NAME = 'chatusers'

DATABASE_URL = f"mysql+pymysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

# Gebruiker Model
def create_db():
    Base.metadata.create_all(engine)

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    email = Column(String(50), unique=False, nullable=False)

    def set_password(self, password):
        self.hashed_password = password_hash.hash(password)

    def check_password(self, password):
        print(f"hashed password: {self.hashed_password}")
        print(f"password: {password}")
        return password_hash.verify(password, self.hashed_password)
    
    def set_email(self, email):
        self.email = email

# Functie om een gebruiker toe te voegen
def add_user(username, password, email):
    session = SessionLocal()
    user = User(username=username)
    user.set_password(password)
    user.set_email(email)
    session.add(user)
    session.commit()
    session.close()

# Functie om een gebruiker te verifiëren
def verify_user(username, password):
    session = SessionLocal()
    user = session.query(User).filter_by(username=username).first()
    session.close()
    
    if user and user.check_password(password):
        return "Login succesvol"
    else:
        return "Ongeldige gebruikersnaam of wachtwoord"

if __name__ == "__main__":
    create_db()
    add_user("johndoe", "secret", "johnny@doe.nl")  # Voeg een testgebruiker toe
    print(verify_user("johndoe", "secret"))  # Controleer de login
    
