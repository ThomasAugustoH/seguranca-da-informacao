import bcrypt
from typing import Generator

from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import create_engine, String
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Mapped, mapped_column, Session

URL_BANCO = "sqlite:///./lista09.db"

motor = create_engine(URL_BANCO, connect_args={"check_same_thread": False})
SessaoLocal = sessionmaker(bind=motor, autoflush=False, autocommit=False)


class Base(DeclarativeBase):
    pass


class Usuario(Base):
    __tablename__ = "usuario"

    login: Mapped[str] = mapped_column(String, primary_key=True, index=True)
    senha: Mapped[str] = mapped_column(String, nullable=False)


class UsuarioCreate(BaseModel):
    login: str
    senha: str


class UsuarioResponse(BaseModel):
    login: str

    class Config:
        from_attributes = True


Base.metadata.create_all(bind=motor)


def obter_db() -> Generator[Session, None, None]:
    sessao = SessaoLocal()
    try:
        yield sessao
    finally:
        sessao.close()

app = FastAPI()

@app.post("/usuario", response_model=UsuarioResponse)
def cadastrar_usuario(usuario: UsuarioCreate, db: Session = Depends(obter_db)):
    senha_bytes = usuario.senha.encode('utf-8')
    sal = bcrypt.gensalt()
    senha_hash = bcrypt.hashpw(senha_bytes, sal).decode('utf-8')
    usuario_final = Usuario(login=usuario.login, senha=senha_hash)
    db.add(usuario_final)
    db.commit()
    db.refresh(usuario_final)
    return usuario_final


