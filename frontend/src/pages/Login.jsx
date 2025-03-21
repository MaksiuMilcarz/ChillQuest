import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import axios from 'axios';

const Login = () => {
  const [formData, setFormData] = useState({
    username: '',
    password: ''
  });
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      console.log('Login attempt with:', formData.username);
      
      // Direct API call to login
      const response = await axios.post('/api/auth/login', formData);
      
      console.log('Login successful:', response.data);
      
      // Store token and user info in localStorage
      localStorage.setItem('token', response.data.access_token);
      localStorage.setItem('user', JSON.stringify(response.data.user));
      
      // Set token for all future axios requests (important!)
      axios.defaults.headers.common['Authorization'] = `Bearer ${response.data.access_token}`;
      
      // Test the token by making a simple API call
      try {
        await axios.get('/api/auth/verify');
        console.log('Token verified successfully');
      } catch (verifyErr) {
        console.warn('Token verification failed:', verifyErr);
        // Continue anyway, as this is just for debugging
      }

      // Redirect to dashboard
      navigate('/dashboard');
    } catch (err) {
      console.error('Login error:', err);
      setError('Login failed. Please check your credentials and try again.');
      
      // Handle specific error messages from the server
      if (err.response && err.response.data && err.response.data.message) {
        setError(`Login failed: ${err.response.data.message}`);
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-100 flex items-center justify-center">
      <div className="bg-white p-8 rounded-lg shadow-md w-full max-w-md">
        <h2 className="text-2xl font-bold mb-6 text-center">Login to ChillQuest</h2>
        
        {error && (
          <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
            {error}
          </div>
        )}
        
        <form onSubmit={handleSubmit}>
          <div className="mb-4">
            <label className="block text-gray-700 text-sm font-bold mb-2" htmlFor="username">
              Username
            </label>
            <input
              className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
              id="username"
              type="text"
              name="username"
              value={formData.username}
              onChange={handleChange}
              required
            />
          </div>
          
          <div className="mb-6">
            <label className="block text-gray-700 text-sm font-bold mb-2" htmlFor="password">
              Password
            </label>
            <input
              className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
              id="password"
              type="password"
              name="password"
              value={formData.password}
              onChange={handleChange}
              required
            />
          </div>
          
          <div className="flex items-center justify-between">
            <button
              className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline w-full"
              type="submit"
              disabled={loading}
            >
              {loading ? 'Logging in...' : 'Login'}
            </button>
          </div>
          
          <div className="text-center mt-4">
            <p>
              Don't have an account?{' '}
              <Link to="/register" className="text-blue-500 hover:text-blue-700">
                Register
              </Link>
            </p>
            <p className="mt-2 text-sm text-gray-500">
              Demo credentials: demouser / password123
            </p>
          </div>
        </form>
      </div>
    </div>
  );
};

export default Login;