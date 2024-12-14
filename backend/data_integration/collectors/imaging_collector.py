from typing import Dict, Any, List
import pydicom
from pathlib import Path
from .base_collector import DataCollector

class ImagingCollector(DataCollector):
    def __init__(self, storage_path: str):
        self.storage_path = Path(storage_path)
    
    async def collect(self) -> Dict[str, Any]:
        """Collect medical imaging data (DICOM files)"""
        image_data = []
        for dicom_file in self.storage_path.glob("*.dcm"):
            try:
                ds = pydicom.dcmread(dicom_file)
                image_data.append(self._process_dicom(ds))
            except Exception as e:
                print(f"Error processing {dicom_file}: {e}")
        
        return {"images": image_data}
    
    async def validate(self, data: Dict[str, Any]) -> bool:
        """Validate imaging data quality and metadata"""
        if not data.get("images"):
            return False
        return all(
            self._validate_image_metadata(img)
            for img in data["images"]
        )
    
    def _process_dicom(self, dataset: pydicom.dataset.FileDataset) -> Dict[str, Any]:
        """Process DICOM dataset into standardized format"""
        return {
            "study_id": str(dataset.StudyInstanceUID),
            "modality": dataset.Modality,
            "study_date": str(dataset.StudyDate),
            "body_part": dataset.BodyPartExamined,
            "metadata": self._extract_metadata(dataset)
        }
    
    def _validate_image_metadata(self, image_data: Dict[str, Any]) -> bool:
        """Validate individual image metadata"""
        required_fields = ["study_id", "modality", "study_date"]
        return all(field in image_data for field in required_fields)
    
    def _extract_metadata(self, dataset: pydicom.dataset.FileDataset) -> Dict[str, Any]:
        """Extract relevant metadata from DICOM dataset"""
        return {
            "manufacturer": getattr(dataset, "Manufacturer", None),
            "slice_thickness": getattr(dataset, "SliceThickness", None),
            "pixel_spacing": getattr(dataset, "PixelSpacing", None),
        } 