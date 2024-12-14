from typing import Dict, Any, List, Optional
import numpy as np
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor
import joblib
from datetime import datetime

class MLPipeline:
    def __init__(self, model_path: Optional[str] = None):
        self.pipeline = self._create_pipeline()
        self.model_path = model_path
        if model_path:
            self.load_model(model_path)
    
    def _create_pipeline(self) -> Pipeline:
        """Create ML pipeline with preprocessing and model"""
        return Pipeline([
            ('scaler', StandardScaler()),
            ('model', RandomForestRegressor(n_estimators=100))
        ])
    
    def prepare_features(self, patient_data: Dict[str, Any]) -> np.ndarray:
        """Extract and prepare features from patient data"""
        features = []
        vitals = patient_data.get("vitals", {})
        medical_history = patient_data.get("medical_history", {})
        
        # Extract relevant features
        features.extend([
            vitals.get("heart_rate", 0),
            vitals.get("systolic_bp", 0),
            vitals.get("diastolic_bp", 0),
            len(medical_history.get("conditions", [])),
            len(medical_history.get("medications", []))
        ])
        
        return np.array(features).reshape(1, -1)
    
    async def train(self, training_data: List[Dict[str, Any]], labels: np.ndarray) -> None:
        """Train the ML pipeline"""
        X = np.vstack([self.prepare_features(data) for data in training_data])
        self.pipeline.fit(X, labels)
        
        if self.model_path:
            self.save_model()
    
    async def predict(self, patient_data: Dict[str, Any]) -> Dict[str, Any]:
        """Make predictions for patient data"""
        features = self.prepare_features(patient_data)
        prediction = self.pipeline.predict(features)[0]
        
        return {
            "prediction": float(prediction),
            "timestamp": datetime.utcnow().isoformat(),
            "confidence": self._calculate_confidence(features)
        }
    
    def _calculate_confidence(self, features: np.ndarray) -> float:
        """Calculate prediction confidence"""
        # Simple confidence calculation based on feature proximity to training data
        return float(np.random.uniform(0.7, 0.9))  # Placeholder
    
    def save_model(self) -> None:
        """Save ML pipeline to disk"""
        joblib.dump(self.pipeline, self.model_path)
    
    def load_model(self, path: str) -> None:
        """Load ML pipeline from disk"""
        self.pipeline = joblib.load(path) 