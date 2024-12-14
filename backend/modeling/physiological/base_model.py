from abc import ABC, abstractmethod
from typing import Dict, Any, List
from datetime import datetime

class PhysiologicalModel(ABC):
    def __init__(self, model_params: Dict[str, Any]):
        self.model_params = model_params
        self.state = {}
        self.history = []
        
    @abstractmethod
    async def initialize(self, patient_data: Dict[str, Any]) -> None:
        """Initialize model with patient data"""
        pass
    
    @abstractmethod
    async def update(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """Update model state based on new inputs"""
        pass
    
    @abstractmethod
    async def predict(self, time_steps: int) -> List[Dict[str, Any]]:
        """Predict future states"""
        pass
    
    def save_state(self) -> None:
        """Save current state to history"""
        self.history.append({
            "timestamp": datetime.utcnow().isoformat(),
            "state": self.state.copy()
        }) 