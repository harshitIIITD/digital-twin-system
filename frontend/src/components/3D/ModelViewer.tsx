import React, { useRef, useState } from 'react';
import { Canvas } from '@react-three/fiber';
import { OrbitControls, useGLTF } from '@react-three/drei';
import { Box, FormControl, InputLabel, Select, MenuItem } from '@mui/material';

interface ModelViewerProps {
  patientId: string;
}

const Model: React.FC<{ modelPath: string }> = ({ modelPath }) => {
  const { scene } = useGLTF(modelPath);
  return <primitive object={scene} />;
};

export const ModelViewer: React.FC<ModelViewerProps> = ({ patientId }) => {
  const [viewMode, setViewMode] = useState('cardiovascular');
  
  return (
    <Box sx={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
      <FormControl sx={{ m: 1, minWidth: 120 }}>
        <InputLabel>View Mode</InputLabel>
        <Select
          value={viewMode}
          label="View Mode"
          onChange={(e) => setViewMode(e.target.value)}
        >
          <MenuItem value="cardiovascular">Cardiovascular</MenuItem>
          <MenuItem value="respiratory">Respiratory</MenuItem>
          <MenuItem value="skeletal">Skeletal</MenuItem>
        </Select>
      </FormControl>
      
      <Box sx={{ flexGrow: 1 }}>
        <Canvas camera={{ position: [0, 0, 5] }}>
          <ambientLight intensity={0.5} />
          <spotLight position={[10, 10, 10]} angle={0.15} penumbra={1} />
          <Model modelPath={`/models/${viewMode}.glb`} />
          <OrbitControls />
        </Canvas>
      </Box>
    </Box>
  );
}; 