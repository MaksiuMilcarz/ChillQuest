import axios from 'axios';

// Simple login function using direct axios
export const loginUser = async (credentials) => {
  try {
    const response = await axios.post('/api/auth/login', credentials);
    
    // Store token and user data
    localStorage.setItem('token', response.data.access_token);
    localStorage.setItem('user', JSON.stringify(response.data.user));
    
    return response.data;
  } catch (error) {
    console.error('Login error:', error);
    throw error;
  }
};

// Simple registration function
export const registerUser = async (userData) => {
  try {
    const response = await axios.post('/api/auth/register', userData);
    
    // Store token and user data
    localStorage.setItem('token', response.data.access_token);
    localStorage.setItem('user', JSON.stringify(response.data.user));
    
    return response.data;
  } catch (error) {
    console.error('Registration error:', error);
    throw error;
  }
};

// Get user profile
export const getUser = async () => {
  const token = localStorage.getItem('token');
  if (!token) return null;
  
  try {
    const response = await axios.get('/api/auth/profile', {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    });
    return response.data;
  } catch (error) {
    if (error.response && error.response.status === 401) {
      // Token expired or invalid
      localStorage.removeItem('token');
      localStorage.removeItem('user');
    }
    return null;
  }
};

// Check if user is authenticated
export const isAuthenticated = () => {
  return !!localStorage.getItem('token');
};

// Logout user
export const logoutUser = () => {
  localStorage.removeItem('token');
  localStorage.removeItem('user');
};

// Clear any existing authentication on app start
export const clearAuthOnStart = () => {
  // Only clear if not on login page
  if (window.location.pathname !== '/login' && window.location.pathname !== '/register') {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
  }
};