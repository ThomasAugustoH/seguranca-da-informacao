from Crypto.Cipher import Blowfish
from Crypto.Util.Padding import pad

def print_hex(texto_bytes: bytes):

    texto_hex = ""
    contador = 0

    for i in range (len(texto_bytes)):
        if (contador == 8):
            contador = 0
            texto_hex += "\n"
        texto_hex += f"{texto_bytes[i]:02X} "
        contador += 1

    
    return texto_hex

chave = bytes([65, 66, 67, 68, 69])
texto_simples = "FURB"

cipher = Blowfish.new(chave, Blowfish.MODE_ECB)

texto_preenchido = pad(bytes(texto_simples, "UTF-8"), Blowfish.block_size)
texto_cifrado = cipher.encrypt(texto_preenchido)

print("Texto cifrado:", print_hex(texto_cifrado))
print("Tamanho:", len(texto_cifrado))

