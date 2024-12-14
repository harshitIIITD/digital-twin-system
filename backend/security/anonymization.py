from typing import Dict, Any, List
import hashlib
import re

class DataAnonymizer:
    def __init__(self):
        self.salt = "your-salt-here"  # Move to environment variables
    
    def anonymize_patient_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Anonymize patient data according to HIPAA guidelines"""
        anonymized = data.copy()
        
        # Anonymize direct identifiers
        if "name" in anonymized:
            anonymized["name"] = self._hash_identifier(str(anonymized["name"]))
        if "email" in anonymized:
            anonymized["email"] = self._anonymize_email(str(anonymized["email"]))
        if "phone" in anonymized:
            anonymized["phone"] = "XXX-XXX-XXXX"
        if "address" in anonymized:
            anonymized["address"] = self._anonymize_address(str(anonymized["address"]))
        if "ssn" in anonymized:
            anonymized["ssn"] = "XXX-XX-XXXX"
        
        # Handle dates according to HIPAA (keep only year for dates >89 years)
        if "birth_date" in anonymized:
            anonymized["birth_date"] = self._anonymize_date(str(anonymized["birth_date"]))
        
        return anonymized
    
    def _hash_identifier(self, identifier: str) -> str:
        """Create one-way hash of identifier"""
        return hashlib.sha256(
            (identifier + self.salt).encode()
        ).hexdigest()[:12]
    
    def _anonymize_email(self, email: str) -> str:
        """Anonymize email address"""
        parts = email.split("@")
        if len(parts) != 2:
            return self._hash_identifier(email)
        return f"{self._hash_identifier(parts[0])}@{parts[1]}"
    
    def _anonymize_address(self, address: str) -> str:
        """Anonymize address to zip code only"""
        zip_pattern = r"\d{5}(-\d{4})?"
        zip_match = re.search(zip_pattern, address)
        if zip_match:
            return f"ZIP: {zip_match.group()}"
        return "Address Redacted"
    
    def _anonymize_date(self, date_str: str) -> str:
        """Anonymize dates according to HIPAA guidelines"""
        try:
            # Implement date anonymization logic
            # For this example, we're just returning the year
            return date_str.split("-")[0]
        except Exception:
            return "Date Redacted" 