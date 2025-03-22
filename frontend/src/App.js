import React, { useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { isAuthenticated } from './services/auth';
import axios from 'axios';

// Import Leaflet CSS early to ensure proper loading
import "leaflet/dist/leaflet.css";
import L from 'leaflet';

// Pages
import Login from './pages/Login';
import Register from './pages/Register';
import Dashboard from './pages/Dashboard';

// Protected Route component
const ProtectedRoute = ({ children }) => {
  if (!isAuthenticated()) {
    return <Navigate to="/login" />;
  }
  return children;
};

const App = () => {
  // Initialize application state
  useEffect(() => {
    // Add app version check
    const APP_VERSION = '1.0.1'; // Increment this whenever you deploy changes
    const storedVersion = localStorage.getItem('appVersion');
    
    if (storedVersion !== APP_VERSION) {
      // Clear cache and refresh if version doesn't match
      localStorage.setItem('appVersion', APP_VERSION);
      
      // Keep authentication data
      const token = localStorage.getItem('token');
      const user = localStorage.getItem('user');
      
      if (token && user) {
        // Only force refresh if the user is actually logged in
        window.location.reload(true); // Force reload from server, not from cache
      }
    }

    // Fix Leaflet icon issues
    delete L.Icon.Default.prototype._getIconUrl;
    L.Icon.Default.mergeOptions({
      iconRetinaUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon-2x.png',
      iconUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon.png',
      shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-shadow.png'
    });
    
    // Set up global axios auth header from localStorage
    const token = localStorage.getItem('token');
    if (token) {
      console.log("Setting global auth token");
      axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;
    }
    
    // Force the base URL for the application
    document.head.innerHTML += `
      <base href="${window.location.origin}/">
    `;
  }, []);

  return (
    <Router>
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
        <Route 
          path="/dashboard" 
          element={
            <ProtectedRoute>
              <Dashboard />
            </ProtectedRoute>
          } 
        />
        <Route path="/" element={<Navigate to="/dashboard" />} />
      </Routes>
    </Router>
  );
};

export default App;