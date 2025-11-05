import React, { useState } from 'react';
import { useParams } from 'react-router-dom';
import { useQuery } from '@tanstack/react-query';
import { trackingAPI } from '../services/api';
import { Search, CheckCircle, Clock, AlertCircle } from 'lucide-react';

export default function TrackRequest() {
  const { trackingId: urlTrackingId } = useParams();
  const [trackingId, setTrackingId] = useState(urlTrackingId || '');
  const [searchId, setSearchId] = useState(urlTrackingId || '');

  const { data, isLoading, error } = useQuery({
    queryKey: ['tracking', searchId],
    queryFn: () => trackingAPI.track(searchId),
    enabled: !!searchId
  });

  const handleSearch = (e) => {
    e.preventDefault();
    setSearchId(trackingId);
  };

  return (
    <div className="max-w-3xl mx-auto space-y-6">
      <h1 className="text-3xl font-bold">Track Service Request</h1>

      {/* Search Form */}
      <form onSubmit={handleSearch} className="card">
        <label className="block text-sm font-medium mb-2">Enter Tracking ID</label>
        <div className="flex space-x-2">
          <input
            type="text"
            className="input-field flex-1"
            value={trackingId}
            onChange={(e) => setTrackingId(e.target.value)}
            placeholder="TRK-XXXXXXXXXXXX"
          />
          <button type="submit" className="btn-primary flex items-center space-x-2">
            <Search className="w-4 h-4" />
            <span>Track</span>
          </button>
        </div>
      </form>

      {/* Loading */}
      {isLoading && (
        <div className="flex justify-center py-12">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
        </div>
      )}

      {/* Error */}
      {error && (
        <div className="card bg-red-50 border border-red-200">
          <div className="flex items-center space-x-2 text-red-800">
            <AlertCircle className="w-5 h-5" />
            <span>Request not found. Please check your tracking ID.</span>
          </div>
        </div>
      )}

      {/* Results */}
      {data && (
        <div className="space-y-6">
          {/* Status Card */}
          <div className="card">
            <div className="flex justify-between items-start mb-4">
              <div>
                <h3 className="text-xl font-bold mb-1">{data.current_stage}</h3>
                <p className="text-gray-600">Tracking ID: {data.tracking_id}</p>
              </div>
              <span className={`badge ${
                data.status === 'Resolved' ? 'badge-low' :
                data.status === 'In Progress' ? 'badge-medium' :
                'badge-high'
              }`}>
                {data.status}
              </span>
            </div>

            {/* Progress Bar */}
            <div className="mb-4">
              <div className="flex justify-between text-sm mb-2">
                <span>Progress</span>
                <span>{data.progress_percentage}%</span>
              </div>
              <div className="w-full bg-gray-200 rounded-full h-2">
                <div 
                  className="bg-primary-600 h-2 rounded-full transition-all"
                  style={{ width: `${data.progress_percentage}%` }}
                ></div>
              </div>
            </div>

            {data.estimated_completion && (
              <div className="flex items-center space-x-2 text-sm text-gray-600">
                <Clock className="w-4 h-4" />
                <span>Estimated completion: {new Date(data.estimated_completion).toLocaleString()}</span>
              </div>
            )}
          </div>

          {/* Timeline */}
          <div className="card">
            <h3 className="text-xl font-bold mb-4">Timeline</h3>
            <div className="space-y-4">
              {data.timeline?.map((event, index) => (
                <div key={index} className="flex items-start space-x-3">
                  <div className={`mt-1 ${event.completed ? 'text-green-600' : 'text-gray-400'}`}>
                    <CheckCircle className="w-5 h-5" />
                  </div>
                  <div className="flex-1">
                    <div className="font-medium">{event.stage}</div>
                    <div className="text-sm text-gray-600">{event.description}</div>
                    <div className="text-xs text-gray-500 mt-1">
                      {new Date(event.timestamp).toLocaleString()}
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
