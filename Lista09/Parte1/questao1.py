from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes


def separar_bytes(mensagem):
    saida = ""

    for i, byte in enumerate(mensagem):
        saida += f"{byte:02X} "

        if (i + 1) % 8 == 0:
            saida += "\n"

    return saida.strip()


entrada = "SEGURANÇA DA INFORMACAO".encode("utf-8")
chave = bytes(range(50, 66))
nonce = bytes([99] * 12)
contador_inicial = bytes([0, 0, 0, 2])
iv = nonce + contador_inicial

encriptador = Cipher(algorithms.AES(chave), modes.CTR(iv)).encryptor()

texto_cifrado = encriptador.update(entrada) + encriptador.finalize()

print(f'A mensagem tem {len(texto_cifrado)} bytes')
print(separar_bytes(texto_cifrado))
