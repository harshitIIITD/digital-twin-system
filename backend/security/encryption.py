from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64
from typing import Dict, Any
import json
from core.config import settings

class DataEncryption:
    def __init__(self):
        self.key = self._generate_key()
        self.fernet = Fernet(self.key)
    
    def _generate_key(self) -> bytes:
        """Generate encryption key from master key"""
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=settings.ENCRYPTION_SALT.encode(),
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(
            kdf.derive(settings.MASTER_KEY.encode())
        )
        return key
    
    def encrypt_data(self, data: Dict[str, Any]) -> str:
        """Encrypt dictionary data"""
        json_data = json.dumps(data)
        encrypted_data = self.fernet.encrypt(json_data.encode())
        return base64.urlsafe_b64encode(encrypted_data).decode()
    
    def decrypt_data(self, encrypted_data: str) -> Dict[str, Any]:
        """Decrypt data back to dictionary"""
        try:
            decoded_data = base64.urlsafe_b64decode(encrypted_data.encode())
            decrypted_data = self.fernet.decrypt(decoded_data)
            return json.loads(decrypted_data.decode())
        except Exception as e:
            raise ValueError(f"Failed to decrypt data: {str(e)}")
    
    def encrypt_file(self, file_path: str) -> None:
        """Encrypt file in place"""
        with open(file_path, 'rb') as file:
            data = file.read()
        encrypted_data = self.fernet.encrypt(data)
        with open(file_path, 'wb') as file:
            file.write(encrypted_data)
    
    def decrypt_file(self, file_path: str) -> bytes:
        """Decrypt file contents"""
        with open(file_path, 'rb') as file:
            encrypted_data = file.read()
        return self.fernet.decrypt(encrypted_data) 