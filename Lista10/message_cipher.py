from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding
from dotenv import load_dotenv
import os

load_dotenv(dotenv_path="./Lista10/.env")

MESSAGE = os.getenv('MESSAGE', 'Hello, World!')
RECEIVER = os.getenv('RECEIVER', 'c')
SENDER = os.getenv('USERNAME', 't')
FILE_PATH = f"./Lista10/keys"

def encrypt_message(text, receiver):
    public_key = load_public_key(receiver)

    if not public_key:
        print(f"Chave pública de '{receiver}' não encontrada.")
        return

    ciphertext = encrypt(text, public_key)
    return ciphertext

def decrypt_message(ciphertext, user):
    private_key = load_private_key(user)

    if not private_key:
        print(f"Chave privada de '{user}' não encontrada.")
        return

    plaintext = decrypt(ciphertext, private_key)
    return plaintext

def load_public_key(user):
    with open(f"{FILE_PATH}/{user}_pub.pem", "rb") as f:
        public_key = serialization.load_pem_public_key(
            f.read(),
        )

    return public_key

def load_private_key(user):
    with open(f"{FILE_PATH}/{user}_priv.pem", "rb") as f:
        private_key = serialization.load_pem_private_key(
            f.read(),
            password=None
        )

    return private_key

def encrypt(message, public_key):
    ciphertext = public_key.encrypt(
        message,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    return ciphertext

def decrypt(ciphertext, private_key):
    plaintext = private_key.decrypt(
        ciphertext,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    ).decode()

    return plaintext

def serialize_bytes(data, filename):
    with open(filename, "wb") as f:
        f.write(data)

def load_bytes(filename):
    with open(filename, "rb") as f:
        return f.read()

if __name__ == "__main__":

    # # Exercício 1
    ciphertext = encrypt_message(MESSAGE.encode(), RECEIVER)
    serialize_bytes(ciphertext, f"./Lista10/messages/{SENDER}_ciphertext.bin")

    # # Teste de descriptografia
    # loaded_ciphertext = load_bytes(f"./Lista10/messages/{SENDER}_ciphertext.bin")
    # plaintext = decrypt_message(loaded_ciphertext, RECEIVER)
    # print(f"Mensagem descriptografada: {plaintext}")

    # Exercício 2
    # message = load_bytes(f"./Lista10/enunciado.pdf")
    # ciphertext = encrypt_message(message, receiver=RECEIVER)
