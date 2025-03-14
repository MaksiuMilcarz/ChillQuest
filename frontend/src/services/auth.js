import axios from 'axios';

// Use relative URL for APIs - will work with NGINX proxy
const API_URL = '/api';

// Simple login function using direct axios
export const loginUser = async (credentials) => {
  try {
    const response = await axios.post(`${API_URL}/auth/login`, credentials, {
      headers: {
        'Content-Type': 'application/json'
      }
    });
    return response.data;
  } catch (error) {
    console.error('Login error:', error);
    throw error;
  }
};

// Simple registration function using direct axios
export const registerUser = async (userData) => {
  try {
    const response = await axios.post(`${API_URL}/auth/register`, userData, {
      headers: {
        'Content-Type': 'application/json'
      }
    });
    return response.data;
  } catch (error) {
    console.error('Registration error:', error);
    throw error;
  }
};

// Get user profile with token from localStorage
export const getUser = async () => {
  const token = localStorage.getItem('token');
  if (!token) return null;
  
  try {
    const response = await axios.get(`${API_URL}/auth/profile`, {
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      }
    });
    return response.data;
  } catch (error) {
    console.error('Get user error:', error);
    if (error.response && error.response.status === 401) {
      // Token expired or invalid
      localStorage.removeItem('token');
      localStorage.removeItem('user');
    }
    return null;
  }
};

// Simple auth check based on token presence
export const isAuthenticated = () => {
  return !!localStorage.getItem('token');
};

// Logout by removing token and user data
export const logoutUser = () => {
  localStorage.removeItem('token');
  localStorage.removeItem('user');
};