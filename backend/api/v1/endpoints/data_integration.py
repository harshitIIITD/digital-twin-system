from fastapi import APIRouter, Depends, HTTPException
from typing import Dict, Any
from datetime import datetime
from data_integration.pipeline.processor import DataProcessor
from data_integration.storage.data_lake import DataLake
from data_integration.collectors.ehr_collector import EHRCollector
from data_integration.collectors.imaging_collector import ImagingCollector
from core.config import settings

router = APIRouter()

# Initialize collectors and data lake
data_lake = DataLake(settings.DATA_LAKE_PATH)
collectors = {
    "ehr": EHRCollector(settings.EHR_API_ENDPOINT, settings.EHR_API_KEY),
    "imaging": ImagingCollector(settings.IMAGING_STORAGE_PATH)
}
processor = DataProcessor(collectors)

@router.post("/collect/{patient_id}")
async def collect_patient_data(patient_id: str) -> Dict[str, Any]:
    """Collect and process all available data for a patient"""
    try:
        # Collect and process data
        processed_data = await processor.collect_and_process(patient_id)
        
        # Store in data lake
        await data_lake.store(
            patient_id=patient_id,
            data=processed_data,
            data_type="integrated"
        )
        
        return processed_data
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to collect data: {str(e)}"
        )

@router.get("/retrieve/{patient_id}")
async def retrieve_patient_data(
    patient_id: str,
    start_date: datetime = None,
    end_date: datetime = None
) -> Dict[str, Any]:
    """Retrieve processed data for a patient"""
    try:
        data = await data_lake.retrieve(
            patient_id=patient_id,
            data_type="integrated",
            start_date=start_date,
            end_date=end_date
        )
        return {"patient_id": patient_id, "data": data}
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to retrieve data: {str(e)}"
        ) 