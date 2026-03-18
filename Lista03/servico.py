from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import sessionmaker, Session, declarative_base
from pydantic import BaseModel
import uvicorn

DATABASE_URL = "sqlite:///./users.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
MIN_PASSWORD_LEN = 6
MAX_PASSWORD_LEN = 30

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)
    email = Column(String)

Base.metadata.create_all(bind=engine)

app = FastAPI()

class RegisterRequest(BaseModel):
    username: str
    email: str
    password: str

class LoginRequest(BaseModel):
    username: str
    password: str

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Rota para registrar usuário
@app.post("/register/")
def register_user(request: RegisterRequest, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.username == request.username).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Usuário já existe"
        )
    
    validatePassword(request.password)

    user = User(
        username=request.username,
        email=request.email,
        password=request.password
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    return {"message": "Usuário registrado com sucesso!"}

def validatePassword(password):
    if len(password) < MIN_PASSWORD_LEN or len(password) > MAX_PASSWORD_LEN:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail=f"Senha deve ter entre {MIN_PASSWORD_LEN} e {MAX_PASSWORD_LEN} caracteres!"
        )

    if (password.isupper() or password.islower()):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail=f"Senha deve ter letras maiúsculas e minúsculas!"
        )

    if (not(any(char.isdigit() for char in password))):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail=f"Senha deve ter pelo menos um número!"
        )
    
    if (not(any(not char.isalnum() for char in password))):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail=f"Senha deve conter caracteres especiais!"
        )
    
    invalid_symbols = ['\'', '\"']
    
    for char in invalid_symbols:
        if char in password:
            raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail=f"Senha não pode conter o caractere [{char}]!"
        )
        break

# Rota de login
@app.post("/login/")
def login(request: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(
        User.username == request.username,
        User.password == request.password
    ).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciais inválidas"
        )

    return {"message": "Login realizado com sucesso!"}


# Inicialização direta do servidor
if __name__ == "__main__":
    uvicorn.run(
        "servico:app",
        host="0.0.0.0",
        port=8000,
        reload=False
    )