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


entrada = "SEGURANÇA DA INFORMACAO".encode("utf-8")
chave = bytes(range(50, 66))
nonce = bytes([99] * 12)
aad = b"questao2.py"

aesgcm = AESGCM(chave)

texto_cifrado = aesgcm.encrypt(nonce, entrada, aad)

print(separar_bytes(texto_cifrado))
print(f"Tag de autenticação: \n{separar_tag(texto_cifrado)}")

with open('Lista09/Parte1/output.bin', 'wb') as file:
    file.write(texto_cifrado)
