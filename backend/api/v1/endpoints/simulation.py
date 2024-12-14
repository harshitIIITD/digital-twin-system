from fastapi import APIRouter, HTTPException
from typing import Dict, Any, List
from datetime import datetime
from modeling.physiological.cardiovascular import CardiovascularModel
from ml.pipeline import MLPipeline
from simulation.engine import SimulationEngine
from core.config import settings

router = APIRouter()

# Initialize models and simulation engine
cardiovascular_model = CardiovascularModel(model_params={})
ml_pipeline = MLPipeline(model_path=settings.ML_MODEL_PATH)
simulation_engine = SimulationEngine(
    physiological_models={"cardiovascular": cardiovascular_model},
    ml_pipeline=ml_pipeline
)

@router.post("/run/{patient_id}")
async def run_simulation(
    patient_id: str,
    duration_hours: int,
    interventions: List[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """Run simulation for a patient"""
    try:
        # Get patient data
        # This should be replaced with actual patient data retrieval
        patient_data = {
            "vitals": {
                "heart_rate": 70,
                "systolic_bp": 120,
                "diastolic_bp": 80
            },
            "medical_history": {
                "conditions": [],
                "medications": []
            }
        }
        
        # Initialize and run simulation
        await simulation_engine.initialize_simulation(patient_data)
        results = await simulation_engine.run_simulation(
            duration_hours=duration_hours,
            interventions=interventions
        )
        
        return results
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Simulation failed: {str(e)}"
        ) 