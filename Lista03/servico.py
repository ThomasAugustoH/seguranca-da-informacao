from datetime import datetime, timedelta
from fastapi import FastAPI, Depends, HTTPException, Request, status
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, create_engine
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
    block_until = Column(DateTime)

class LoginLogs(Base):
    __tablename__ = "login_requests"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, ForeignKey("users.id") , index=True)
    request_date = Column(DateTime, default=datetime.now)
    ip_address = Column(String)
    access_allowed = Column(String)

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

def get_client_ip(request: Request):
    forwarded = request.headers.get("x-forwarded-for")
    
    if forwarded:
        return forwarded.split(",")[0]
    
    return request.client.host

def log_request(db, request, status, ip):
    login_request = LoginLogs(
        username = request.username,
        ip_address = ip,
        access_allowed = status
    )

    db.add(login_request)
    db.commit()
    db.refresh(login_request)

# Rota de login
@app.post("/login/")
def login(request: LoginRequest, db: Session = Depends(get_db), ip: str = Depends(get_client_ip)):

    ip_request_delay = delaySameIpRequisition(db, ip)

    if ip_request_delay > 0:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Muitas requisições feitas por este endereço IP. Aguarde {ip_request_delay} segundos."
        )
    
    user_request = db.query(User).filter(
        User.username == request.username,
    ).first()

    if user_request.block_until and user_request.block_until >= datetime.now():
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Usuário bloqueado"
        )

    user = db.query(User).filter(
        User.username == request.username,
        User.password == request.password
    ).first()

    if not user:
        log_request(db, request, 'N', ip)
        if blockUser(request.username, db):
            user_request.block_until = datetime.now() + timedelta(minutes=5)
            db.commit()
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciais inválidas"
        )

    log_request(db, request, 'Y', ip)

    return {"message": "Login realizado com sucesso!"}

def blockUser(username, db: Session):
    successfulRequest = db.query(LoginLogs).filter(
        LoginLogs.username == username,
        LoginLogs.access_allowed == 'Y'
    ).order_by(
        LoginLogs.request_date.desc()
    ).first()

    print(successfulRequest)

    if successfulRequest:
        failedRequests = db.query(LoginLogs).filter(
            LoginLogs.username == username,
            LoginLogs.access_allowed == 'N',
            LoginLogs.request_date >= successfulRequest.request_date,
        ).count()
    else:
        failedRequests = db.query(LoginLogs).filter(
            LoginLogs.username == username,
            LoginLogs.access_allowed == 'N',
        ).order_by(
            LoginLogs.request_date.desc()
        ).count()

    print(failedRequests)

    if failedRequests >= 3:
        return True
    return False

def delaySameIpRequisition(db: Session, ip):
    successfulRequest = db.query(LoginLogs).filter(
        LoginLogs.ip_address == ip,
        LoginLogs.access_allowed == 'Y'
    ).order_by(
        LoginLogs.request_date
    ).first()

    if successfulRequest:
        failedRequests = db.query(LoginLogs).filter(
            LoginLogs.ip_address == ip,
            LoginLogs.access_allowed == 'N',
            LoginLogs.request_date >= successfulRequest.request_date,
        )
    else:
        failedRequests = db.query(LoginLogs).filter(
            LoginLogs.ip_address == ip,
            LoginLogs.access_allowed == 'N',
        ).order_by(
            LoginLogs.request_date.desc()
        )
    
    lastFail = failedRequests.first()
    failedRequests = failedRequests.count()

    if failedRequests == 0:
        return 0

    if failedRequests > 7:
        failedRequests = 7

    delays = [5, 10, 15, 30, 60, 300, 600, 1800]
    delay = (lastFail.request_date + timedelta(seconds=delays[failedRequests]) - datetime.now())

    return max(0, delay.total_seconds())

# Inicialização direta do servidor
if __name__ == "__main__":
    uvicorn.run(
        "servico:app",
        host="0.0.0.0",
        port=8000,
        reload=False
    )