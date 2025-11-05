import React, { useState } from 'react';
import { useMutation } from '@tanstack/react-query';
import { requestsAPI } from '../services/api';
import { useNavigate } from 'react-router-dom';
import { Send, CheckCircle, AlertCircle } from 'lucide-react';

export default function SubmitRequest() {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    description: '',
    location_lat: 18.5204,
    location_lng: 73.8567,
    location_address: ''
  });

  const mutation = useMutation({
    mutationFn: requestsAPI.submit,
    onSuccess: (data) => {
      navigate(`/track/${data.tracking_id}`);
    }
  });

  const handleSubmit = (e) => {
    e.preventDefault();
    mutation.mutate(formData);
  };

  return (
    <div className="max-w-2xl mx-auto space-y-6">
      <h1 className="text-3xl font-bold">Submit Service Request</h1>

      {mutation.isSuccess && (
        <div className="card bg-green-50 border border-green-200">
          <div className="flex items-center space-x-2 text-green-800">
            <CheckCircle className="w-5 h-5" />
            <span>Request submitted successfully! Redirecting to tracking...</span>
          </div>
        </div>
      )}

      {mutation.isError && (
        <div className="card bg-red-50 border border-red-200">
          <div className="flex items-center space-x-2 text-red-800">
            <AlertCircle className="w-5 h-5" />
            <span>Error: {mutation.error.message}</span>
          </div>
        </div>
      )}

      <form onSubmit={handleSubmit} className="card space-y-4">
        <div>
          <label className="block text-sm font-medium mb-2">Description *</label>
          <textarea
            className="input-field"
            rows={4}
            required
            value={formData.description}
            onChange={(e) => setFormData({...formData, description: e.target.value})}
            placeholder="Describe your issue in detail..."
          />
        </div>

        <div className="grid grid-cols-2 gap-4">
          <div>
            <label className="block text-sm font-medium mb-2">Latitude</label>
            <input
              type="number"
              step="0.0001"
              className="input-field"
              value={formData.location_lat}
              onChange={(e) => setFormData({...formData, location_lat: parseFloat(e.target.value)})}
            />
          </div>
          <div>
            <label className="block text-sm font-medium mb-2">Longitude</label>
            <input
              type="number"
              step="0.0001"
              className="input-field"
              value={formData.location_lng}
              onChange={(e) => setFormData({...formData, location_lng: parseFloat(e.target.value)})}
            />
          </div>
        </div>

        <div>
          <label className="block text-sm font-medium mb-2">Address</label>
          <input
            type="text"
            className="input-field"
            value={formData.location_address}
            onChange={(e) => setFormData({...formData, location_address: e.target.value})}
            placeholder="Enter address..."
          />
        </div>

        <button 
          type="submit" 
          className="btn-primary w-full flex items-center justify-center space-x-2"
          disabled={mutation.isPending}
        >
          {mutation.isPending ? (
            <>
              <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white"></div>
              <span>Submitting...</span>
            </>
          ) : (
            <>
              <Send className="w-4 h-4" />
              <span>Submit Request</span>
            </>
          )}
        </button>
      </form>

      <div className="card bg-gray-50">
        <h3 className="font-bold mb-2">What happens next?</h3>
        <ol className="list-decimal list-inside space-y-2 text-sm text-gray-700">
          <li>AI categorizes your request using Gemini Pro</li>
          <li>Priority score calculated based on multiple factors</li>
          <li>Automatically routed to appropriate department</li>
          <li>You receive a tracking ID to monitor progress</li>
          <li>Estimated resolution time provided</li>
        </ol>
      </div>
    </div>
  );
}
