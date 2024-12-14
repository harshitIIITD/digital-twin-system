import React, { useEffect, useState } from 'react';
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer
} from 'recharts';
import { api } from '../../services/api';
import { format } from 'date-fns';

interface VitalsChartProps {
  patientId: string;
}

interface VitalData {
  timestamp: string;
  heart_rate: number;
  systolic_bp: number;
  diastolic_bp: number;
}

export const VitalsChart: React.FC<VitalsChartProps> = ({ patientId }) => {
  const [data, setData] = useState<VitalData[]>([]);

  useEffect(() => {
    const fetchVitals = async () => {
      try {
        const response = await api.get(`/patients/${patientId}/vitals`);
        setData(response.data.map((item: VitalData) => ({
          ...item,
          timestamp: format(new Date(item.timestamp), 'HH:mm:ss')
        })));
      } catch (error) {
        console.error('Error fetching vitals:', error);
      }
    };

    fetchVitals();
    const interval = setInterval(fetchVitals, 5000); // Update every 5 seconds
    return () => clearInterval(interval);
  }, [patientId]);

  return (
    <ResponsiveContainer width="100%" height={400}>
      <LineChart data={data}>
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis dataKey="timestamp" />
        <YAxis />
        <Tooltip />
        <Legend />
        <Line 
          type="monotone" 
          dataKey="heart_rate" 
          stroke="#8884d8" 
          name="Heart Rate"
        />
        <Line 
          type="monotone" 
          dataKey="systolic_bp" 
          stroke="#82ca9d" 
          name="Systolic BP"
        />
        <Line 
          type="monotone" 
          dataKey="diastolic_bp" 
          stroke="#ffc658" 
          name="Diastolic BP"
        />
      </LineChart>
    </ResponsiveContainer>
  );
}; 