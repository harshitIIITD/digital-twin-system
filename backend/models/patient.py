from sqlalchemy import Column, Integer, String, JSON
from .base import Base, TimeStampedModel

class Patient(Base, TimeStampedModel):
    __tablename__ = "patients"

    id = Column(Integer, primary_key=True)
    external_id = Column(String, unique=True, index=True)
    demographic_data = Column(JSON)
    medical_history = Column(JSON)
    genetic_data = Column(JSON) 