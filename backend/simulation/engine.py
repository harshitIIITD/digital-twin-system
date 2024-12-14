from typing import Dict, Any, List
from datetime import datetime, timedelta
from modeling.physiological.base_model import PhysiologicalModel
from ml.pipeline import MLPipeline

class SimulationEngine:
    def __init__(
        self,
        physiological_models: Dict[str, PhysiologicalModel],
        ml_pipeline: MLPipeline
    ):
        self.models = physiological_models
        self.ml_pipeline = ml_pipeline
        self.current_time = datetime.utcnow()
        
    async def initialize_simulation(self, patient_data: Dict[str, Any]) -> None:
        """Initialize all models with patient data"""
        for model in self.models.values():
            await model.initialize(patient_data)
    
    async def run_simulation(
        self,
        duration_hours: int,
        time_step_minutes: int = 15,
        interventions: List[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Run simulation for specified duration"""
        steps = (duration_hours * 60) // time_step_minutes
        results = []
        
        for step in range(steps):
            current_time = self.current_time + timedelta(minutes=step * time_step_minutes)
            
            # Apply interventions if any
            inputs = self._get_intervention_for_time(current_time, interventions)
            
            # Update all models
            state = {}
            for system, model in self.models.items():
                system_state = await model.update(inputs)
                state[system] = system_state
            
            # Get ML predictions
            ml_prediction = await self.ml_pipeline.predict(state)
            
            results.append({
                "timestamp": current_time.isoformat(),
                "state": state,
                "predictions": ml_prediction
            })
        
        return {
            "simulation_id": datetime.utcnow().strftime("%Y%m%d_%H%M%S"),
            "duration_hours": duration_hours,
            "time_step_minutes": time_step_minutes,
            "results": results
        }
    
    def _get_intervention_for_time(
        self,
        current_time: datetime,
        interventions: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Get applicable interventions for current time"""
        if not interventions:
            return {}
            
        applicable_interventions = {}
        for intervention in interventions:
            start_time = datetime.fromisoformat(intervention["start_time"])
            end_time = datetime.fromisoformat(intervention["end_time"])
            
            if start_time <= current_time <= end_time:
                applicable_interventions.update(intervention["parameters"])
                
        return applicable_interventions 