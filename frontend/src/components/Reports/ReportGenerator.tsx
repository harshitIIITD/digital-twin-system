import React, { useState } from 'react';
import {
  Box,
  Button,
  Checkbox,
  FormControlLabel,
  FormGroup,
  Paper,
  Typography
} from '@mui/material';
import { api } from '../../services/api';

interface ReportGeneratorProps {
  patientId: string;
}

export const ReportGenerator: React.FC<ReportGeneratorProps> = ({ patientId }) => {
  const [sections, setSections] = useState({
    vitals: true,
    medications: true,
    simulations: true,
    predictions: true
  });
  const [generating, setGenerating] = useState(false);

  const handleGenerateReport = async () => {
    setGenerating(true);
    try {
      const response = await api.post(`/reports/generate/${patientId}`, {
        sections: Object.entries(sections)
          .filter(([_, included]) => included)
          .map(([section]) => section)
      });
      
      // Handle PDF download
      const blob = new Blob([response.data], { type: 'application/pdf' });
      const url = window.URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.download = `patient_${patientId}_report.pdf`;
      link.click();
    } catch (error) {
      console.error('Report generation failed:', error);
    } finally {
      setGenerating(false);
    }
  };

  return (
    <Paper sx={{ p: 2 }}>
      <Typography variant="h6" gutterBottom>
        Generate Report
      </Typography>
      
      <FormGroup>
        <FormControlLabel
          control={
            <Checkbox
              checked={sections.vitals}
              onChange={(e) => setSections({ ...sections, vitals: e.target.checked })}
            />
          }
          label="Vital Signs"
        />
        <FormControlLabel
          control={
            <Checkbox
              checked={sections.medications}
              onChange={(e) => setSections({ ...sections, medications: e.target.checked })}
            />
          }
          label="Medications"
        />
        <FormControlLabel
          control={
            <Checkbox
              checked={sections.simulations}
              onChange={(e) => setSections({ ...sections, simulations: e.target.checked })}
            />
          }
          label="Simulation Results"
        />
        <FormControlLabel
          control={
            <Checkbox
              checked={sections.predictions}
              onChange={(e) => setSections({ ...sections, predictions: e.target.checked })}
            />
          }
          label="Predictions"
        />
      </FormGroup>
      
      <Button
        variant="contained"
        onClick={handleGenerateReport}
        disabled={generating}
        sx={{ mt: 2 }}
      >
        Generate Report
      </Button>
    </Paper>
  );
}; 