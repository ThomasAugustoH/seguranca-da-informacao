from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding
from dotenv import load_dotenv
import os

load_dotenv(dotenv_path='./Lista10/.env')

MESSAGE = os.getenv('MESSAGE', 'Hello, World!')
RECEIVER = os.getenv('RECEIVER', 'c')
SENDER = os.getenv('USERNAME', 't')
KEYS_DIR = f'./Lista10/keys'
MESSAGES_DIR = f'./Lista10/messages'

def encrypt_message(text, receiver):
    public_key = load_public_key(receiver)

    if not public_key:
        print(f'Chave pública de \'{receiver}\' não encontrada.')
        return

    ciphertext = encrypt(text, public_key)
    return ciphertext

def decrypt_message(ciphertext, user):
    private_key = load_private_key(user)

    if not private_key:
        print(f'Chave privada de \'{user}\' não encontrada.')
        return

    plaintext = decrypt(ciphertext, private_key)
    return plaintext

def load_public_key(user):
    with open(f'{KEYS_DIR}/{user}_pub.pem', 'rb') as f:
        public_key = serialization.load_pem_public_key(
            f.read(),
        )

    return public_key

def load_private_key(user):
    with open(f'{KEYS_DIR}/{user}_priv.pem', 'rb') as f:
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

def save_bytes(filename, data):
    with open(filename, 'wb') as f:
        f.write(data)

def load_bytes(filename):
    with open(filename, 'rb') as f:
        return f.read()

def send_message(message, receiver):
    ciphertext = encrypt_message(message.encode(), receiver)
    save_bytes(f'{MESSAGES_DIR}/{SENDER}_ciphertext.bin', ciphertext)

def read_message(sender, receiver):
    ciphertext = load_bytes(f'{MESSAGES_DIR}/{sender}_ciphertext.bin')
    plaintext = decrypt_message(ciphertext, receiver)
    return plaintext

if __name__ == '__main__':

    # Exercício 1
    # send_message(MESSAGE, RECEIVER)

    # Teste de descriptografia
    # plaintext = read_message(SENDER, RECEIVER)
    # print(f'Mensagem recebida: {plaintext}')

    # Exercício 2
    # message = load_bytes(f'./Lista10/enunciado.pdf')
    # ciphertext = encrypt_message(message, receiver=RECEIVER)
