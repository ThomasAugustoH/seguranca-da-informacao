from cryptography.hazmat.primitives import serialization
from dotenv import load_dotenv
import os

load_dotenv(dotenv_path="./Lista10/.env")

MESSAGE = os.getenv('MESSAGE', 'Hello, World!')
RECEIVER = os.getenv('RECEIVER', 't')
USER = os.getenv('USERNAME', 'c')

def load_public_key():
    try:
        with open(f"./Lista10/keys/{os.getenv('RECEIVER', 'notme')}_pub.pem", "rb") as f:
            public_key = serialization.load_pem_public_key(
                f.read(),
            )
    except FileNotFoundError:
        print(f"Chave pública do usuário '{RECEIVER}' não encontrada.")
        
        exit(1)
        
    return public_key

def encript_message(public_key):
    ciphertext = public_key.encrypt(
        MESSAGE.encode(),
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    return ciphertext

def serialize_ciphertext(ciphertext):
    with open(f"./Lista10/ciphertexts/{USER}_to_{RECEIVER}.bin", "wb") as f:
        f.write(ciphertext)


if __name__ == "__main__":
    public_key = load_public_key()

    # Exercise 1
    ciphertext = encript_message(public_key)
    serialize_ciphertext(ciphertext)