import React from 'react';
import { Box, Grid, Paper, Typography } from '@mui/material';
import VitalsChart from './VitalsChart';
import PatientInfo from './PatientInfo';
import ModelViewer from '../3D/ModelViewer';
import SimulationControls from './SimulationControls';

interface DashboardLayoutProps {
  patientId: string;
}

export const DashboardLayout: React.FC<DashboardLayoutProps> = ({ patientId }) => {
  return (
    <Box sx={{ flexGrow: 1, p: 3 }}>
      <Grid container spacing={3}>
        <Grid item xs={12} md={4}>
          <Paper sx={{ p: 2 }}>
            <Typography variant="h6">Patient Information</Typography>
            <PatientInfo patientId={patientId} />
          </Paper>
        </Grid>
        
        <Grid item xs={12} md={8}>
          <Paper sx={{ p: 2 }}>
            <Typography variant="h6">Vital Signs</Typography>
            <VitalsChart patientId={patientId} />
          </Paper>
        </Grid>
        
        <Grid item xs={12} md={8}>
          <Paper sx={{ p: 2, height: '500px' }}>
            <Typography variant="h6">3D Visualization</Typography>
            <ModelViewer patientId={patientId} />
          </Paper>
        </Grid>
        
        <Grid item xs={12} md={4}>
          <Paper sx={{ p: 2 }}>
            <Typography variant="h6">Simulation Controls</Typography>
            <SimulationControls patientId={patientId} />
          </Paper>
        </Grid>
      </Grid>
    </Box>
  );
}; 