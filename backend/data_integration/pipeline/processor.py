from typing import Dict, Any, List
import asyncio
from datetime import datetime
from ..collectors.base_collector import DataCollector

class DataProcessor:
    def __init__(self, collectors: Dict[str, DataCollector]):
        self.collectors = collectors
        self.processing_queue = asyncio.Queue()
        
    async def collect_and_process(self, patient_id: str) -> Dict[str, Any]:
        """Collect and process data from all sources for a patient"""
        tasks = []
        for source, collector in self.collectors.items():
            task = asyncio.create_task(
                self._collect_and_validate(source, collector)
            )
            tasks.append(task)
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        return self._merge_results(patient_id, results)
    
    async def _collect_and_validate(
        self,
        source: str,
        collector: DataCollector
    ) -> Dict[str, Any]:
        """Collect and validate data from a single source"""
        try:
            data = await collector.collect()
            if await collector.validate(data):
                return {
                    "source": source,
                    "data": data,
                    "collected_at": datetime.utcnow().isoformat(),
                    "status": "success"
                }
            return {
                "source": source,
                "status": "validation_failed",
                "error": "Data validation failed"
            }
        except Exception as e:
            return {
                "source": source,
                "status": "error",
                "error": str(e)
            }
    
    def _merge_results(
        self,
        patient_id: str,
        results: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Merge results from different collectors"""
        return {
            "patient_id": patient_id,
            "timestamp": datetime.utcnow().isoformat(),
            "data_sources": {
                result["source"]: result
                for result in results
                if isinstance(result, dict)
            }
        } 