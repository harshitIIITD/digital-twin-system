import React, { useState } from 'react';
import {
  Box,
  Button,
  Slider,
  Typography,
  TextField,
  CircularProgress
} from '@mui/material';
import { api } from '../../services/api';

interface SimulationControlsProps {
  patientId: string;
}

export const SimulationControls: React.FC<SimulationControlsProps> = ({ patientId }) => {
  const [duration, setDuration] = useState<number>(24);
  const [loading, setLoading] = useState<boolean>(false);
  const [intervention, setIntervention] = useState<string>('');

  const handleRunSimulation = async () => {
    setLoading(true);
    try {
      const response = await api.post(`/simulation/run/${patientId}`, {
        duration_hours: duration,
        interventions: intervention ? JSON.parse(intervention) : null
      });
      console.log('Simulation results:', response.data);
    } catch (error) {
      console.error('Simulation failed:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Box sx={{ width: '100%' }}>
      <Typography gutterBottom>
        Simulation Duration (hours)
      </Typography>
      <Slider
        value={duration}
        onChange={(_, value) => setDuration(value as number)}
        min={1}
        max={168}
        valueLabelDisplay="auto"
      />
      
      <TextField
        fullWidth
        multiline
        rows={4}
        margin="normal"
        label="Interventions (JSON)"
        value={intervention}
        onChange={(e) => setIntervention(e.target.value)}
        placeholder='{"start_time": "2023-01-01T00:00:00", "parameters": {...}}'
      />
      
      <Button
        fullWidth
        variant="contained"
        onClick={handleRunSimulation}
        disabled={loading}
        sx={{ mt: 2 }}
      >
        {loading ? <CircularProgress size={24} /> : 'Run Simulation'}
      </Button>
    </Box>
  );
}; 