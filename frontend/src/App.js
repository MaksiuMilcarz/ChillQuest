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
  // Fix Leaflet icon issues on component mount
  useEffect(() => {
    // IMPORTANT: We've removed clearAuthOnStart() which was causing authentication loss
    
    // Fix Leaflet icon issues once on load
    delete L.Icon.Default.prototype._getIconUrl;
    L.Icon.Default.mergeOptions({
      iconRetinaUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon-2x.png',
      iconUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon.png',
      shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-shadow.png'
    });
    
    // Make sure global axios default has the auth token
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
        <Route path="/" element={<Navigate to="/login" />} />
      </Routes>
    </Router>
  );
};

export default App;