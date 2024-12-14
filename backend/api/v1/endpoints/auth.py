from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from typing import Any
from datetime import timedelta
from auth.jwt import (
    create_access_token,
    get_current_user,
    ACCESS_TOKEN_EXPIRE_MINUTES,
    Token
)
from security.encryption import DataEncryption
from security.anonymization import DataAnonymizer
from core.config import settings

router = APIRouter()
encryption = DataEncryption()
anonymizer = DataAnonymizer()

@router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends()
) -> Any:
    # Authenticate user (implement your user authentication logic)
    if not authenticate_user(form_data.username, form_data.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": form_data.username},
        expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/secure-data/{patient_id}")
async def get_secure_patient_data(
    patient_id: str,
    current_user: Any = Depends(get_current_user)
) -> Any:
    # Get patient data
    patient_data = await get_patient_data(patient_id)
    
    # Apply security measures based on settings
    if settings.ENABLE_ANONYMIZATION:
        patient_data = anonymizer.anonymize_patient_data(patient_data)
    
    if settings.ENABLE_DATA_ENCRYPTION:
        return {"data": encryption.encrypt_data(patient_data)}
    
    return patient_data 