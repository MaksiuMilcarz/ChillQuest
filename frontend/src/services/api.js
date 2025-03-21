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
    // Make sure to format the header correctly
    config.headers.Authorization = `Bearer ${token}`;
    console.log('Adding auth token to request');
  }
  return config;
});

// Handle token errors globally
api.interceptors.response.use(
  response => response,
  error => {
    console.error('API error:', error.response ? error.response.status : 'No response');
    console.error('Error details:', error.response ? error.response.data : error.message);
    
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
    // Let the interceptor handle the token
    const response = await api.get('/visits/');
    return response.data;
  } catch (error) {
    console.error('Error fetching user visits:', error);
    throw error;
  }
};

export const addVisit = async (locationId, rating = null, notes = '') => {
  try {
    // Ensure we're passing exactly what the backend expects
    const payload = {
      location_id: parseInt(locationId, 10),
      rating: rating,
      notes: notes || ''
    };
    
    console.log('Sending visit data:', JSON.stringify(payload));
    const response = await api.post('/visits/', payload);
    return response.data;
  } catch (error) {
    console.error('Error adding visit:', error);
    // Check for specific error details
    if (error.response && error.response.data && error.response.data.message) {
      throw new Error(`Failed to add visit: ${error.response.data.message}`);
    }
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

// Verify token is working
export const verifyAuth = async () => {
  try {
    const response = await api.get('/auth/verify');
    console.log('Auth verification response:', response.data);
    return response.data;
  } catch (error) {
    console.error('Auth verification failed:', error);
    throw error;
  }
};

export default api;