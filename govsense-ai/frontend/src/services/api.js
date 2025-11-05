import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8080';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Predictions API (Feature 1)
export const predictionsAPI = {
  getForecast: async (params) => {
    const response = await api.post('/api/predictions/forecast', params);
    return response.data;
  },
  
  getCategories: async () => {
    const response = await api.get('/api/predictions/categories');
    return response.data;
  },
  
  getZones: async () => {
    const response = await api.get('/api/predictions/zones');
    return response.data;
  },
  
  getHistorical: async (category, days = 90) => {
    const response = await api.get('/api/predictions/historical', {
      params: { category, days }
    });
    return response.data;
  },
  
  getAccuracy: async () => {
    const response = await api.get('/api/predictions/accuracy');
    return response.data;
  },
};

// Service Requests API (Feature 2)
export const requestsAPI = {
  submit: async (requestData) => {
    const response = await api.post('/api/requests/submit', requestData);
    return response.data;
  },
  
  list: async (params) => {
    const response = await api.get('/api/requests/list', { params });
    return response.data;
  },
  
  getStats: async () => {
    const response = await api.get('/api/requests/stats');
    return response.data;
  },
  
  generateDemoData: async (count = 20) => {
    const response = await api.post('/api/requests/demo-data', null, {
      params: { count }
    });
    return response.data;
  },
};

// Tracking API
export const trackingAPI = {
  track: async (trackingId) => {
    const response = await api.get(`/api/tracking/${trackingId}`);
    return response.data;
  },
  
  updateStatus: async (trackingId, newStatus) => {
    const response = await api.post(`/api/tracking/${trackingId}/update`, null, {
      params: { new_status: newStatus }
    });
    return response.data;
  },
  
  submitFeedback: async (trackingId, satisfaction, feedbackText) => {
    const response = await api.post(`/api/tracking/${trackingId}/feedback`, null, {
      params: { satisfaction, feedback_text: feedbackText }
    });
    return response.data;
  },
};

// Public API (Feature 3)
export const publicAPI = {
  getDashboard: async () => {
    const response = await api.get('/api/public/dashboard');
    return response.data;
  },
  
  getCurrentMetrics: async () => {
    const response = await api.get('/api/public/metrics/current');
    return response.data;
  },
  
  getComparison: async () => {
    const response = await api.get('/api/public/metrics/comparison');
    return response.data;
  },
  
  getOpenData: async (limit = 100, offset = 0) => {
    const response = await api.get('/api/public/open-data/requests', {
      params: { limit, offset }
    });
    return response.data;
  },
  
  getDataCatalog: async () => {
    const response = await api.get('/api/public/data-catalog');
    return response.data;
  },
};

// Health check
export const healthCheck = async () => {
  const response = await api.get('/health');
  return response.data;
};

export default api;
