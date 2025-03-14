import axios from 'axios';

// Create axios instance with auth header
const api = axios.create({
  baseURL: '/api',
  headers: {
    'Content-Type': 'application/json'
  }
});

// Add auth token to requests
api.interceptors.request.use(config => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
    console.log('Using token in request');
  }
  return config;
});

// Handle token errors globally
api.interceptors.response.use(
  response => response,
  error => {
    if (error.response && error.response.status === 401) {
      // Redirect to login on auth errors
      console.log('Authentication error, redirecting to login');
      localStorage.removeItem('token');
      localStorage.removeItem('user');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// Locations
export const getAllLocations = async () => {
  try {
    const response = await api.get('/locations/');
    return response.data;
  } catch (error) {
    console.error('Error fetching locations:', error);
    throw error;
  }
};

// Visits
export const getUserVisits = async () => {
  try {
    const response = await api.get('/visits/');
    return response.data;
  } catch (error) {
    console.error('Error fetching user visits:', error);
    throw error;
  }
};

export const addVisit = async (visitData) => {
  try {
    const response = await api.post('/visits/', visitData);
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
    const response = await api.get('/recommendations/');
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