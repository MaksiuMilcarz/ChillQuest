import axios from 'axios';

// Simple login function using direct axios
export const loginUser = async (credentials) => {
  try {
    const response = await axios.post('/api/auth/login', credentials);
    
    // Store token and user data
    localStorage.setItem('token', response.data.access_token);
    localStorage.setItem('user', JSON.stringify(response.data.user));
    
    // Set token for all future axios requests
    axios.defaults.headers.common['Authorization'] = `Bearer ${response.data.access_token}`;
    
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
    
    // Set token for all future axios requests
    axios.defaults.headers.common['Authorization'] = `Bearer ${response.data.access_token}`;
    
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
  
  // Also remove from axios defaults
  delete axios.defaults.headers.common['Authorization'];
};

// Important! Don't clear auth on app start
export const clearAuthOnStart = () => {
  console.log("Authentication preserved");
};