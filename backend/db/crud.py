from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List, Optional
from models.patient import Patient
from schemas.patient import PatientCreate

async def create_patient(db: AsyncSession, patient: PatientCreate) -> Patient:
    db_patient = Patient(**patient.dict())
    db.add(db_patient)
    await db.commit()
    await db.refresh(db_patient)
    return db_patient

async def get_patient(db: AsyncSession, patient_id: int) -> Optional[Patient]:
    query = select(Patient).where(Patient.id == patient_id)
    result = await db.execute(query)
    return result.scalar_one_or_none()

async def get_patients(db: AsyncSession, skip: int = 0, limit: int = 100) -> List[Patient]:
    query = select(Patient).offset(skip).limit(limit)
    result = await db.execute(query)
    return result.scalars().all() 