from typing import Dict, Any
from .base_collector import DataCollector
import aiohttp
from datetime import datetime

class EHRCollector(DataCollector):
    def __init__(self, api_endpoint: str, api_key: str):
        self.api_endpoint = api_endpoint
        self.headers = {"Authorization": f"Bearer {api_key}"}
    
    async def collect(self) -> Dict[str, Any]:
        """Collect EHR data from healthcare system"""
        async with aiohttp.ClientSession() as session:
            async with session.get(
                self.api_endpoint,
                headers=self.headers
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    return self._transform_ehr_data(data)
                raise Exception(f"Failed to collect EHR data: {response.status}")
    
    async def validate(self, data: Dict[str, Any]) -> bool:
        """Validate EHR data format and completeness"""
        required_fields = ["patient_id", "medical_history", "medications"]
        return all(field in data for field in required_fields)
    
    def _transform_ehr_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Transform EHR data into standardized format"""
        return {
            "patient_id": data.get("id"),
            "medical_history": data.get("history", []),
            "medications": data.get("medications", []),
            "allergies": data.get("allergies", []),
            "vitals": data.get("vitals", {}),
            "collected_at": datetime.utcnow().isoformat()
        } 