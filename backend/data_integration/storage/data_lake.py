from typing import Dict, Any, List
import json
from datetime import datetime
from pathlib import Path
import asyncio
import aiofiles

class DataLake:
    def __init__(self, base_path: str):
        self.base_path = Path(base_path)
        self.base_path.mkdir(parents=True, exist_ok=True)
    
    async def store(
        self,
        patient_id: str,
        data: Dict[str, Any],
        data_type: str
    ) -> str:
        """Store data in the data lake"""
        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        file_path = self.base_path / f"{data_type}/{patient_id}/{timestamp}.json"
        file_path.parent.mkdir(parents=True, exist_ok=True)
        
        async with aiofiles.open(file_path, mode='w') as f:
            await f.write(json.dumps(data, indent=2))
        
        return str(file_path)
    
    async def retrieve(
        self,
        patient_id: str,
        data_type: str,
        start_date: datetime = None,
        end_date: datetime = None
    ) -> List[Dict[str, Any]]:
        """Retrieve data from the data lake"""
        path = self.base_path / f"{data_type}/{patient_id}"
        if not path.exists():
            return []
        
        files = sorted(path.glob("*.json"))
        results = []
        
        for file_path in files:
            if self._is_file_in_date_range(file_path, start_date, end_date):
                async with aiofiles.open(file_path, mode='r') as f:
                    content = await f.read()
                    results.append(json.loads(content))
        
        return results
    
    def _is_file_in_date_range(
        self,
        file_path: Path,
        start_date: datetime,
        end_date: datetime
    ) -> bool:
        """Check if file timestamp is within date range"""
        if not (start_date or end_date):
            return True
            
        timestamp_str = file_path.stem
        file_date = datetime.strptime(timestamp_str.split("_")[0], "%Y%m%d")
        
        if start_date and file_date < start_date:
            return False
        if end_date and file_date > end_date:
            return False
        return True 