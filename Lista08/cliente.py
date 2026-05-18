import base64
import hashlib
import hmac
import json
import time
import requests

URL_BASE = "http://127.0.0.1:8000"
id_cliente = input("Forneça o id do cliente: ")
chave = input("Forneça a chave: ")

def gerar_hash_corpo(corpo: str) -> str:
    return hashlib.sha256(corpo.encode("utf-8")).hexdigest()

def gerar_assinatura(chave: str, string_para_assinar: str) -> str:
    mac = hmac.new(
        chave.encode("utf-8"),
        string_para_assinar.encode("utf-8"),
        hashlib.sha256
    ).digest()
    return base64.b64encode(mac).decode("utf-8")

def montar_cabecalhos(id_cliente: str, chave: str, metodo: str, rota: str, corpo: str, timestamp: str):
    hash_corpo = gerar_hash_corpo(corpo)

    string_para_assinar = (
        f"{id_cliente}\n"
        f"{timestamp}\n"
        f"{metodo}\n"
        f"{rota}\n"
        f"{hash_corpo}"
    )

    assinatura = gerar_assinatura(chave, string_para_assinar)

    return {
        "X-Consumer-Id": id_cliente,
        "X-Timestamp": timestamp,
        "X-Signature": assinatura,
        "Content-Type": "application/json",
    }

def enviar_post_produto(corpo: str, timestamp: str = None, chave: str = chave):
    if timestamp is None:
        timestamp = str(int(time.time() * 1000))

    cabecalhos = montar_cabecalhos(
        id_cliente,
        chave,
        "POST",
        "/produtos",
        corpo,
        timestamp
    )

    resposta = requests.post(
        f"{URL_BASE}/produtos",
        data=corpo,
        headers=cabecalhos
    )

    print("Status:", resposta.status_code)
    print("Resposta:", resposta.text)
    print("-" * 40)

def caso_1_sucesso():
    print("CASO 1 - requisição válida")
    corpo = '{"nome":"Teclado","preco":150}'
    enviar_post_produto(corpo)

def caso_2_mac_invalido():
    print("CASO 2 - mensagem alterada depois da assinatura")
    corpo_original = '{"nome":"Teclado","preco":150}'
    timestamp = str(int(time.time() * 1000))

    cabecalhos = montar_cabecalhos(
        id_cliente,
        chave,
        "POST",
        "/produtos",
        corpo_original,
        timestamp
    )

    corpo_alterado = '{"nome":"Teclado","preco":999}'

    resposta = requests.post(
        f"{URL_BASE}/produtos",
        data=corpo_alterado,
        headers=cabecalhos
    )

    print("Status:", resposta.status_code)
    print("Resposta:", resposta.text)
    print("-" * 40)

def caso_3_replay_attack():
    print("CASO 3 - replay attack")
    corpo = '{"nome":"Mouse","preco":80}'

    timestamp_antigo = str(int(time.time() * 1000) - 10 * 60 * 1000)

    cabecalhos = montar_cabecalhos(
        id_cliente,
        chave,
        "POST",
        "/produtos",
        corpo,
        timestamp_antigo
    )

    resposta = requests.post(
        f"{URL_BASE}/produtos",
        data=corpo,
        headers=cabecalhos
    )

    print("Status:", resposta.status_code)
    print("Resposta:", resposta.text)
    print("-" * 40)

if __name__ == "__main__":
    caso_1_sucesso()
    caso_2_mac_invalido()
    caso_3_replay_attack()