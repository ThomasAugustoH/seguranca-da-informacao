import base64
import hashlib
import hmac
import time
from typing import Generator

from fastapi import FastAPI, Depends, HTTPException, Request, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from sqlalchemy import create_engine, String, Integer, Float
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Mapped, mapped_column, Session

URL_BANCO = "sqlite:///./app.db"
JANELA_SEGUNDOS = 300 

CLIENTES = {
    "ClienteA": "Chave123",
    "ClienteB": "Chave789",
}

motor = create_engine(URL_BANCO, connect_args={"check_same_thread": False})
SessaoLocal = sessionmaker(bind=motor, autoflush=False, autocommit=False)

class Base(DeclarativeBase):
    pass

class Produto(Base):
    __tablename__ = "produtos"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    nome: Mapped[str] = mapped_column(String, nullable=False)
    preco: Mapped[float] = mapped_column(Float, nullable=False)

Base.metadata.create_all(bind=motor)

def obter_db() -> Generator[Session, None, None]:
    sessao = SessaoLocal()
    try:
        yield sessao
    finally:
        sessao.close()


class ProdutoEntrada(BaseModel):
    nome: str
    preco: float

class ProdutoSaida(BaseModel):
    id: int
    nome: str
    preco: float

    class Config:
        from_attributes = True


def gerar_assinatura(secreto: str, string_para_assinar: str) -> str:
    mac = hmac.new(
        secreto.encode("utf-8"),
        string_para_assinar.encode("utf-8"),
        hashlib.sha256
    ).digest()
    return base64.b64encode(mac).decode("utf-8")

async def verificar_hmac(requisicao: Request):
    id_consumidor = requisicao.headers.get("X-Consumer-Id")
    timestamp = requisicao.headers.get("X-Timestamp")
    assinatura = requisicao.headers.get("X-Signature")

    if not id_consumidor or not timestamp or not assinatura:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Headers obrigatorios ausentes"
        )

    segredo = CLIENTES.get(id_consumidor)
    if not segredo:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Consumidor invalido"
        )

    try:
        ts = int(timestamp)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Timestamp invalido"
        )

    agora_ms = int(time.time() * 1000)
    if abs(agora_ms - ts) > JANELA_SEGUNDOS * 1000:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Request expirado"
        )

    corpo = await requisicao.body()
    hash_corpo = hashlib.sha256(corpo).hexdigest()

    string_para_assinar = (
        f"{id_consumidor}\n"
        f"{timestamp}\n"
        f"{requisicao.method}\n"
        f"{requisicao.url.path}\n"
        f"{hash_corpo}"
    )

    assinatura_esperada = gerar_assinatura(segredo, string_para_assinar)

    if not hmac.compare_digest(assinatura_esperada, assinatura):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="MAC invalido"
        )

app = FastAPI()

@app.post("/produtos", response_model=ProdutoSaida, dependencies=[Depends(verificar_hmac)])
def criar_produto(produto_entrada: ProdutoEntrada, db: Session = Depends(obter_db)):
    produto = Produto(nome=produto_entrada.nome, preco=produto_entrada.preco)
    db.add(produto)
    db.commit()
    db.refresh(produto)
    return produto

@app.get("/produtos", response_model=list[ProdutoSaida], dependencies=[Depends(verificar_hmac)])
def listar_produtos(db: Session = Depends(obter_db)):
    return db.query(Produto).all()

@app.get("/produtos/{produto_id}", response_model=ProdutoSaida, dependencies=[Depends(verificar_hmac)])
def buscar_produto(produto_id: int, db: Session = Depends(obter_db)):
    produto = db.get(Produto, produto_id)
    if not produto:
        raise HTTPException(status_code=404, detail="Produto nao encontrado")
    return produto

@app.put("/produtos/{produto_id}", response_model=ProdutoSaida, dependencies=[Depends(verificar_hmac)])
def atualizar_produto(produto_id: int, produto_entrada: ProdutoEntrada, db: Session = Depends(obter_db)):
    produto = db.get(Produto, produto_id)
    if not produto:
        raise HTTPException(status_code=404, detail="Produto nao encontrado")

    produto.nome = produto_entrada.nome
    produto.preco = produto_entrada.preco
    db.commit()
    db.refresh(produto)
    return produto

@app.delete("/produtos/{produto_id}", dependencies=[Depends(verificar_hmac)])
def remover_produto(produto_id: int, db: Session = Depends(obter_db)):
    produto = db.get(Produto, produto_id)
    if not produto:
        raise HTTPException(status_code=404, detail="Produto nao encontrado")

    db.delete(produto)
    db.commit()
    return JSONResponse({"mensagem": "Removido com sucesso"})