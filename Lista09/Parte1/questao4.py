from cryptography.hazmat.primitives.ciphers.aead import AESGCM


def separar_bytes(mensagem):
    saida = ""

    for i, byte in enumerate(mensagem):
        saida += f"{byte:02X} "

        if (i + 1) % 8 == 0:
            saida += "\n"

    return saida.strip()


def separar_tag(dados):
    tag = dados[-16:]

    saida = ""

    for i, byte in enumerate(tag):
        saida += f"{byte:02X} "

        if (i + 1) % 8 == 0:
            saida += "\n"

    return saida.strip()

with open("Lista09/Parte1/output.bin", "rb") as file:
    entrada = file.read()

chave = bytes(range(50, 66))
nonce = bytes([99] * 12)
aad = b"questao2.py"

aesgcm = AESGCM(chave)

texto_decifrado = aesgcm.decrypt(nonce, entrada, aad)

print(texto_decifrado.decode("utf-8"))
    