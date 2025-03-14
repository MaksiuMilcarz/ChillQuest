import axios from 'axios';

// Use relative URL for APIs - will work with NGINX proxy
const API_URL = '/api';

// Create axios instance with auth header
const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json'
  },
  timeout: 10000 // 10 seconds timeout
});

// Add auth token to requests
api.interceptors.request.use(config => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  console.log(`API Request: ${config.method?.toUpperCase() || 'GET'} ${config.url}`);
  return config;
}, error => {
  console.error("Request setup error:", error);
  return Promise.reject(error);
});

// Add response interceptor for debugging
api.interceptors.response.use(
  response => {
    console.log(`API Response [${response.config.url}]: Success`);
    return response;
  },
  error => {
    if (error.response) {
      console.error(`API Error [${error.config?.url}]:`, error.response.status, error.response.data);
    } else if (error.request) {
      console.error(`API Error [${error.config?.url}]: No response received`);
    } else {
      console.error(`API Error: ${error.message}`);
    }
    return Promise.reject(error);
  }
);

// Locations
export const getAllLocations = async () => {
  try {
    const response = await api.get('/locations');
    return response.data;
  } catch (error) {
    console.error('Error fetching locations:', error);
    throw error;
  }
};

export const getLocation = async (id) => {
  try {
    const response = await api.get(`/locations/${id}`);
    return response.data;
  } catch (error) {
    console.error(`Error fetching location ${id}:`, error);
    throw error;
  }
};

export const searchLocations = async (query, type) => {
  try {
    const params = new URLSearchParams();
    if (query) params.append('q', query);
    if (type) params.append('type', type);
    
    const response = await api.get(`/locations/search?${params.toString()}`);
    return response.data;
  } catch (error) {
    console.error('Error searching locations:', error);
    throw error;
  }
};

// Visits
export const getUserVisits = async () => {
  try {
    const response = await api.get('/visits');
    return response.data;
  } catch (error) {
    console.error('Error fetching user visits:', error);
    if (error.response && error.response.status === 401) {
      // Token expired or invalid
      localStorage.removeItem('token');
      localStorage.removeItem('user');
      window.location.href = '/login'; // Redirect to login on auth error
    }
    throw error;
  }
};

export const addVisit = async (visitData) => {
  try {
    const response = await api.post('/visits', visitData);
    return response.data;
  } catch (error) {
    console.error('Error adding visit:', error);
    throw error;
  }
};

export const deleteVisit = async (visitId) => {
  try {
    const response = await api.delete(`/visits/${visitId}`);
    return response.data;
  } catch (error) {
    console.error(`Error deleting visit ${visitId}:`, error);
    throw error;
  }
};

// Recommendations
export const getRecommendations = async () => {
  try {
    const response = await api.get('/recommendations');
    return response.data;
  } catch (error) {
    console.error('Error fetching recommendations:', error);
    throw error;
  }
};

export const getPersonalizedRecommendations = async (usePersonalization = true) => {
  try {
    const response = await api.get(`/recommendations/personalized?personalized=${usePersonalization}`);
    return response.data;
  } catch (error) {
    console.error('Error fetching personalized recommendations:', error);
    throw error;
  }
};

export default api;