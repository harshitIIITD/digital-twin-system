from abc import ABC, abstractmethod
from typing import Any, Dict

class DataCollector(ABC):
    """Base class for all data collectors"""
    
    @abstractmethod
    async def collect(self) -> Dict[str, Any]:
        """Collect data from source"""
        pass

    @abstractmethod
    async def validate(self, data: Dict[str, Any]) -> bool:
        """Validate collected data"""
        pass 