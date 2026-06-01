from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import os
from dotenv import load_dotenv

load_dotenv()

KEYS_DIR = './Lista10/keys'
MESSAGES_DIR = './Lista10/messages'
SENDER = os.getenv('USERNAME', 't')
RECEIVER = os.getenv('RECEIVER', 'c')

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

def encrypt_aes_key(aes_key, public_key):
    return public_key.encrypt(
        aes_key,
        padding.OAEP(
            mgf=padding.MGF1(hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

def decrypt_aes_key(ciphertext, private_key):
    return private_key.decrypt(
        ciphertext,
        padding.OAEP(
            mgf=padding.MGF1(hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

def generate_aes_key():
    return AESGCM.generate_key(bit_length=256)

def encrypt_image(image_path, aes_key):
    aes = AESGCM(aes_key)

    nonce = os.urandom(12)

    with open(image_path, 'rb') as f:
        image_data = f.read()

    ciphertext = aes.encrypt(nonce, image_data, None)

    return nonce + ciphertext

def decrypt_image(encrypted_path, aes_key):
    aes = AESGCM(aes_key)

    with open(encrypted_path, 'rb') as f:
        encrypted_data = f.read()

    nonce = encrypted_data[:12]
    ciphertext = encrypted_data[12:]

    return aes.decrypt(nonce, ciphertext, None)

def save_bytes(filename, data):
    with open(filename, 'wb') as f:
        f.write(data)

def load_bytes(filename):
    with open(filename, 'rb') as f:
        return f.read()

def send_image(image_path, receiver):
    receiver_public_key = load_public_key(receiver)

    aes_key = generate_aes_key()

    encrypted_image = encrypt_image(image_path, aes_key)

    encrypted_aes_key = encrypt_aes_key(aes_key, receiver_public_key)

    save_bytes(f'./{MESSAGES_DIR}/{SENDER}_image.enc', encrypted_image)

    save_bytes(f'{MESSAGES_DIR}/{SENDER}_aes_key.enc', encrypted_aes_key)

def receive_image(encrypted_image_path, encrypted_key_path, user, output_image):
    private_key = load_private_key(user)

    encrypted_aes_key = load_bytes(encrypted_key_path)

    aes_key = decrypt_aes_key(encrypted_aes_key, private_key)

    image_data = decrypt_image(encrypted_image_path, aes_key)

    save_bytes(output_image, image_data)

if __name__ == '__main__':
    # send_image(f'./{MESSAGES_DIR}/imagem_legal.jpg', RECEIVER)

    # receive_image(
    #     f'{MESSAGES_DIR}/{RECEIVER}_image.enc',
    #     f'{MESSAGES_DIR}/{RECEIVER}_aes_key.enc',
    #     SENDER,
    #     f'{MESSAGES_DIR}/{RECEIVER}_recovered.jpg'
    #     )