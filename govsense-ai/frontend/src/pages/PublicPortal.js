import React from 'react';
import { useQuery } from '@tanstack/react-query';
import { publicAPI } from '../services/api';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts';
import { TrendingUp, Users, Clock, Star } from 'lucide-react';

const COLORS = ['#2563eb', '#10b981', '#f59e0b', '#ef4444'];

export default function PublicPortal() {
  const { data: dashboardData, isLoading } = useQuery({
    queryKey: ['publicDashboard'],
    queryFn: publicAPI.getDashboard
  });

  const { data: comparison } = useQuery({
    queryKey: ['comparison'],
    queryFn: publicAPI.getComparison
  });

  if (isLoading) {
    return (
      <div className="flex justify-center items-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
      </div>
    );
  }

  const overview = dashboardData?.overview || {};
  const categoryData = dashboardData?.category_breakdown || [];

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold mb-2">Public Transparency Portal</h1>
        <p className="text-gray-600">Real-time government performance metrics - No login required</p>
      </div>

      {/* Key Metrics */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        <div className="card">
          <div className="flex items-center justify-between mb-2">
            <div className="text-sm text-gray-600">Completion Rate</div>
            <TrendingUp className="w-5 h-5 text-green-600" />
          </div>
          <div className="text-3xl font-bold text-green-600">
            {Math.round((overview.completion_rate || 0) * 100)}%
          </div>
          <div className="text-xs text-gray-500 mt-1">+37% from baseline</div>
        </div>

        <div className="card">
          <div className="flex items-center justify-between mb-2">
            <div className="text-sm text-gray-600">Avg Response Time</div>
            <Clock className="w-5 h-5 text-blue-600" />
          </div>
          <div className="text-3xl font-bold text-blue-600">
            {Math.round(overview.avg_response_time_hours || 0)}h
          </div>
          <div className="text-xs text-gray-500 mt-1">60% faster</div>
        </div>

        <div className="card">
          <div className="flex items-center justify-between mb-2">
            <div className="text-sm text-gray-600">Citizen Satisfaction</div>
            <Star className="w-5 h-5 text-yellow-600" />
          </div>
          <div className="text-3xl font-bold text-yellow-600">
            {(overview.citizen_satisfaction || 0).toFixed(1)}/5
          </div>
          <div className="text-xs text-gray-500 mt-1">+50% improvement</div>
        </div>

        <div className="card">
          <div className="flex items-center justify-between mb-2">
            <div className="text-sm text-gray-600">Requests This Month</div>
            <Users className="w-5 h-5 text-purple-600" />
          </div>
          <div className="text-3xl font-bold text-purple-600">
            {overview.total_requests_month || 0}
          </div>
          <div className="text-xs text-gray-500 mt-1">{overview.resolved_this_month || 0} resolved</div>
        </div>
      </div>

      {/* Before/After Comparison */}
      {comparison && (
        <div className="card">
          <h3 className="text-xl font-bold mb-4">Before vs After AI Implementation</h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <h4 className="font-medium mb-3 text-gray-600">Before AI (Traditional)</h4>
              <div className="space-y-2 text-sm">
                <div className="flex justify-between">
                  <span>Response Time:</span>
                  <span className="font-medium">{comparison.before_ai.avg_response_time_hours}h</span>
                </div>
                <div className="flex justify-between">
                  <span>Completion Rate:</span>
                  <span className="font-medium">{Math.round(comparison.before_ai.completion_rate * 100)}%</span>
                </div>
                <div className="flex justify-between">
                  <span>Satisfaction:</span>
                  <span className="font-medium">{comparison.before_ai.citizen_satisfaction}/5</span>
                </div>
              </div>
            </div>
            <div>
              <h4 className="font-medium mb-3 text-green-600">After AI (GovSense)</h4>
              <div className="space-y-2 text-sm">
                <div className="flex justify-between">
                  <span>Response Time:</span>
                  <span className="font-medium text-green-600">{comparison.after_ai.avg_response_time_hours}h</span>
                </div>
                <div className="flex justify-between">
                  <span>Completion Rate:</span>
                  <span className="font-medium text-green-600">{Math.round(comparison.after_ai.completion_rate * 100)}%</span>
                </div>
                <div className="flex justify-between">
                  <span>Satisfaction:</span>
                  <span className="font-medium text-green-600">{comparison.after_ai.citizen_satisfaction}/5</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Category Breakdown */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="card">
          <h3 className="text-xl font-bold mb-4">Requests by Category</h3>
          <ResponsiveContainer width="100%" height={300}>
            <PieChart>
              <Pie
                data={categoryData}
                dataKey="total_requests"
                nameKey="category"
                cx="50%"
                cy="50%"
                outerRadius={100}
                label
              >
                {categoryData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                ))}
              </Pie>
              <Tooltip />
              <Legend />
            </PieChart>
          </ResponsiveContainer>
        </div>

        <div className="card">
          <h3 className="text-xl font-bold mb-4">Performance by Category</h3>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={categoryData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="category" />
              <YAxis />
              <Tooltip />
              <Legend />
              <Bar dataKey="completion_rate" fill="#2563eb" name="Completion Rate" />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Impact Stories */}
      {dashboardData?.impact_stories && (
        <div className="card">
          <h3 className="text-xl font-bold mb-4">Impact Stories</h3>
          <div className="space-y-4">
            {dashboardData.impact_stories.map((story, index) => (
              <div key={index} className="p-4 bg-blue-50 rounded-lg border border-blue-200">
                <p className="text-gray-700">{story}</p>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Open Data */}
      <div className="card bg-gray-50">
        <h3 className="text-xl font-bold mb-2">Open Data API</h3>
        <p className="text-gray-600 mb-4">
          Access anonymized government data for research and development
        </p>
        <a 
          href="/api/public/data-catalog" 
          target="_blank"
          rel="noopener noreferrer"
          className="btn-primary inline-block"
        >
          View Data Catalog
        </a>
      </div>
    </div>
  );
}
