from cryptography.fernet import Fernet
from dotenv import load_dotenv
import os

load_dotenv()# Load environment variables from .env file

def load_key():
    key = os.getenv("FERNET_KEY")
    if not key:
        raise Exception("FERNET_KEY not found in .env")
    return key.encode()

def encrypt_log(data: str) -> bytes:
    return Fernet(load_key()).encrypt(data.encode())

def decrypt_log(token: bytes) -> str:
    return Fernet(load_key()).decrypt(token).decode()