from pydantic import BaseModel
from typing import Dict, Optional
from datetime import datetime

class PatientBase(BaseModel):
    external_id: str
    demographic_data: Dict
    medical_history: Optional[Dict] = None
    genetic_data: Optional[Dict] = None

class PatientCreate(PatientBase):
    pass

class PatientResponse(PatientBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True 