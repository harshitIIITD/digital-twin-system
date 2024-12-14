from cryptography.fernet import Fernet
from typing import Any

class DataEncryption:
    def __init__(self, key: bytes):
        self.fernet = Fernet(key)

    def encrypt_patient_data(self, data: Any) -> bytes:
        """Encrypt sensitive patient data"""
        return self.fernet.encrypt(str(data).encode())

    def decrypt_patient_data(self, encrypted_data: bytes) -> Any:
        """Decrypt patient data"""
        return self.fernet.decrypt(encrypted_data) 