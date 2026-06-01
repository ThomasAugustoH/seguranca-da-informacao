from pathlib import Path
from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding
import argparse
import os
from dotenv import load_dotenv

load_dotenv()

KEYS_DIR = "./Lista10/keys"
MESSAGES_DIR = "./Lista10/messages"
SENDER = os.getenv("USERNAME", "t")
RECEIVER = os.getenv("RECEIVER", "c")


def load_public_key(user):
    with open(f"{KEYS_DIR}/{user}_pub.pem", "rb") as f:
        public_key = serialization.load_pem_public_key(f.read())
    return public_key


def load_private_key(user):
    with open(f"{KEYS_DIR}/{user}_priv.pem", "rb") as f:
        private_key = serialization.load_pem_private_key(f.read(), password=None)
    return private_key


def save_bytes(filename, data):
    with open(filename, "wb") as f:
        f.write(data)


def load_bytes(filename):
    with open(filename, "rb") as f:
        return f.read()


def sign_file(file_path, signer):
    private_key = load_private_key(signer)

    if not private_key:
        print(f"Chave privada de '{signer}' não encontrada.")
        return None

    with open(file_path, "rb") as f:
        file_data = f.read()

    signature = private_key.sign(
        file_data,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256(),
    )

    return signature


def verify_file(file_path, signature_path, signer):
    public_key = load_public_key(signer)

    with open(file_path, "rb") as f:
        file_data = f.read()

    signature = load_bytes(signature_path)

    try:
        public_key.verify(
            signature,
            file_data,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256(),
        )
        return True
    except InvalidSignature:
        return False


def send_signed_file(file_path, signer):
    signature = sign_file(file_path, signer)

    if signature is None:
        return

    signature_file = f"{MESSAGES_DIR}/{signer}_signature.sig"
    save_bytes(signature_file, signature)

    with open(file_path, "rb") as f:
        file_data = f.read()
    save_bytes(f"{MESSAGES_DIR}/{signer}_signedfile.txt", file_data)


def receive_and_verify_file(file_path, signature_path, signer):
    if verify_file(file_path, signature_path, signer):
        print("Assinatura válida.")
    else:
        print("Assinatura inválida.")


if __name__ == "__main__":
    send_signed_file(f"./{MESSAGES_DIR}/{SENDER}_unsigned.txt", SENDER)

    receive_and_verify_file(
        f"{MESSAGES_DIR}/{RECEIVER}_signedfile.txt", f"{MESSAGES_DIR}/{RECEIVER}_signature.sig", RECEIVER
    )

