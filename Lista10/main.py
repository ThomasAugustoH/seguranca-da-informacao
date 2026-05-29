from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
import os

USER = "c"

def main():
    if no_keys():
        private_key, public_key = generate_keypair()
        
        serialize_private_key(private_key)
        serialize_public_key(public_key)

def no_keys():
    return not os.path.exists(f"./Lista10/keys/{USER}_priv.pem") or not os.path.exists(f"./Lista10/keys/{USER}_pub.pem")

def generate_keypair():
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
    )
    public_key = private_key.public_key()
    return private_key, public_key

def serialize_private_key(private_key):
    with open(f"./Lista10/keys/{USER}_priv.pem", "wb") as f:
        f.write(
            private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption()
            )
        )

def serialize_public_key(public_key):
    with open(f"./Lista10/keys/{USER}_pub.pem", "wb") as f:
        f.write(
            public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            )
        )

if __name__ == "__main__":
    main()