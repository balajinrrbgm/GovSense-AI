import React from 'react';
import { useQuery } from '@tanstack/react-query';
import { predictionsAPI } from '../services/api';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { TrendingUp, AlertCircle } from 'lucide-react';

export default function PredictiveDashboard() {
  const [days, setDays] = React.useState(30);
  
  const { data, isLoading, error } = useQuery({
    queryKey: ['predictions', days],
    queryFn: () => predictionsAPI.getForecast({ days })
  });

  if (isLoading) {
    return (
      <div className="flex justify-center items-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="card bg-red-50 border border-red-200">
        <div className="flex items-center space-x-2 text-red-800">
          <AlertCircle className="w-5 h-5" />
          <span>Error loading predictions: {error.message}</span>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h1 className="text-3xl font-bold">Predictive Service Demand Dashboard</h1>
        <select 
          className="input-field w-48"
          value={days}
          onChange={(e) => setDays(Number(e.target.value))}
        >
          <option value={7}>7 Days</option>
          <option value={14}>14 Days</option>
          <option value={30}>30 Days</option>
          <option value={60}>60 Days</option>
          <option value={90}>90 Days</option>
        </select>
      </div>

      {/* AI Insights */}
      {data?.insights && (
        <div className="card bg-blue-50 border border-blue-200">
          <div className="flex items-start space-x-3">
            <TrendingUp className="w-6 h-6 text-blue-600 mt-1" />
            <div>
              <h3 className="font-bold text-lg mb-2">AI-Generated Insights</h3>
              <p className="text-gray-700 whitespace-pre-line">{data.insights}</p>
            </div>
          </div>
        </div>
      )}

      {/* Forecast Chart */}
      <div className="card">
        <h3 className="text-xl font-bold mb-4">Demand Forecast - Next {days} Days</h3>
        <ResponsiveContainer width="100%" height={400}>
          <LineChart data={data?.predictions || []}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="date" />
            <YAxis />
            <Tooltip />
            <Legend />
            <Line 
              type="monotone" 
              dataKey="predicted_requests" 
              stroke="#2563eb" 
              strokeWidth={2}
              name="Predicted Requests"
            />
            <Line 
              type="monotone" 
              dataKey="confidence_upper" 
              stroke="#93c5fd" 
              strokeDasharray="5 5"
              name="Upper Bound"
            />
            <Line 
              type="monotone" 
              dataKey="confidence_lower" 
              stroke="#93c5fd" 
              strokeDasharray="5 5"
              name="Lower Bound"
            />
          </LineChart>
        </ResponsiveContainer>
      </div>

      {/* Summary Stats */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="card">
          <div className="text-sm text-gray-600 mb-1">Total Predicted Requests</div>
          <div className="text-3xl font-bold text-primary-600">
            {data?.predictions?.reduce((sum, p) => sum + p.predicted_requests, 0) || 0}
          </div>
        </div>
        <div className="card">
          <div className="text-sm text-gray-600 mb-1">Average Daily Demand</div>
          <div className="text-3xl font-bold text-success-600">
            {Math.round((data?.predictions?.reduce((sum, p) => sum + p.predicted_requests, 0) || 0) / days)}
          </div>
        </div>
        <div className="card">
          <div className="text-sm text-gray-600 mb-1">Model Confidence</div>
          <div className="text-3xl font-bold text-warning-600">
            {Math.round((data?.predictions?.[0]?.confidence_score || 0) * 100)}%
          </div>
        </div>
      </div>
    </div>
  );
}
