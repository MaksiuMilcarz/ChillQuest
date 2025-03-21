import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import Map from '../components/Map';
import LocationCard from '../components/LocationCard';
import RecommendationList from '../components/RecommendationList';
import Navbar from '../components/Navbar';
import { getUserVisits, getAllLocations, getRecommendations, addVisit, deleteVisit, verifyAuth } from '../services/api';
import { isAuthenticated } from '../services/auth';
import axios from 'axios';

const Dashboard = () => {
  const navigate = useNavigate();
  
  // State
  const [userVisits, setUserVisits] = useState([]);
  const [selectedLocation, setSelectedLocation] = useState(null);
  const [locations, setLocations] = useState([]);
  const [recommendations, setRecommendations] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [activeTab, setActiveTab] = useState('map');
  const [visitedLocationIds, setVisitedLocationIds] = useState(new Set());
  
  // Authentication verification
  useEffect(() => {
    const checkAuth = async () => {
      if (!isAuthenticated()) {
        console.log('User not authenticated, redirecting to login');
        navigate('/login');
        return;
      }
      
      // Attempt to verify auth with backend
      try {
        console.log('Verifying authentication...');
        // Log current token
        const token = localStorage.getItem('token');
        console.log('Current token:', token?.substring(0, 20) + '...');
        
        // Manually set axios auth header for debugging
        axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;
        
        // Try to verify auth
        await verifyAuth();
        console.log('Authentication verified successfully');
      } catch (err) {
        console.error('Auth verification failed:', err);
        setError('Authentication failed. Please log in again.');
        navigate('/login');
      }
    };
    
    checkAuth();
  }, [navigate]);
  
  // Load initial data
  useEffect(() => {
    const loadData = async () => {
      setLoading(true);
      setError('');
      
      try {
        console.log('Loading dashboard data...');
        
        // Load data in parallel
        const [locationsData, recommendationsData, visitsData] = await Promise.all([
          getAllLocations(),
          getRecommendations(),
          getUserVisits().catch(err => {
            console.error('Failed to load visits:', err);
            return { visits: [] };
          })
        ]);
        
        console.log('Loaded locations:', locationsData?.locations?.length || 0);
        console.log('Loaded recommendations:', recommendationsData?.recommendations?.length || 0);
        console.log('Loaded visits:', visitsData?.visits?.length || 0);
        
        // Update state
        if (locationsData?.locations) {
          setLocations(locationsData.locations);
        }
        
        if (recommendationsData?.recommendations) {
          setRecommendations(recommendationsData.recommendations);
        }
        
        if (visitsData?.visits) {
          // Filter out visits without location data
          const validVisits = visitsData.visits.filter(visit => visit.location);
          setUserVisits(validVisits);
          
          // Create a set of visited location IDs for quick lookup
          const visitedIds = new Set();
          validVisits.forEach(visit => {
            if (visit.location) {
              visitedIds.add(visit.location.id);
            }
          });
          setVisitedLocationIds(visitedIds);
        }
      } catch (err) {
        console.error('Failed to load dashboard data:', err);
        setError('Failed to load dashboard data. Please try refreshing the page.');
      } finally {
        setLoading(false);
      }
    };
    
    loadData();
  }, []);
  
  // Handle marker click on map
  const handleMarkerClick = (location) => {
    setSelectedLocation(location);
  };
  
  // Handle visit toggle (add/remove)
  const handleVisitChange = async (location, isNowVisited) => {
    try {
      if (isNowVisited) {
        // Add visit
        console.log(`Adding visit for location ${location.id}`);
        const response = await addVisit(location.id);
        console.log('Visit added:', response);
        
        if (response && response.visit) {
          // Add to state
          setUserVisits(prev => [...prev, response.visit]);
          setVisitedLocationIds(prev => new Set([...prev, location.id]));
        }
      } else {
        // Find the visit to remove
        const visit = userVisits.find(v => v.location && v.location.id === location.id);
        
        if (visit) {
          // Remove visit
          console.log(`Removing visit ${visit.id} for location ${location.id}`);
          await deleteVisit(visit.id);
          
          // Update state
          setUserVisits(prev => prev.filter(v => v.id !== visit.id));
          setVisitedLocationIds(prev => {
            const newSet = new Set([...prev]);
            newSet.delete(location.id);
            return newSet;
          });
        }
      }
    } catch (err) {
      console.error('Failed to update visit:', err);
      setError(`Failed to ${isNowVisited ? 'add' : 'remove'} visit: ${err.message}`);
    }
  };
  
  // Handle showing error/loading states
  if (loading) {
    return (
      <div className="flex flex-col h-screen">
        <Navbar />
        <div className="flex-grow flex items-center justify-center">
          <div className="text-xl">Loading your travel data...</div>
        </div>
      </div>
    );
  }

  return (
    <div className="flex flex-col h-screen">
      <Navbar />
      
      {error && (
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 m-4 rounded">
          <p>{error}</p>
          <button 
            onClick={() => window.location.reload()}
            className="underline mt-2"
          >
            Refresh Page
          </button>
        </div>
      )}
      
      <div className="flex-grow flex flex-col md:flex-row">
        {/* Left side - Map or Recommendations */}
        <div className="w-full md:w-2/3 h-[60vh] md:h-full overflow-hidden">
          {/* Tabs */}
          <div className="bg-white p-4 shadow-sm relative dashboard-tabs" style={{ zIndex: 50 }}>
            <div className="flex border-b">
              {/* Map Tab with Icon */}
              <button
                className={`py-2 px-4 flex items-center ${
                  activeTab === 'map' 
                    ? 'border-b-2 border-blue-500 text-blue-500' 
                    : 'text-gray-500'
                }`}
                onClick={() => setActiveTab('map')}
              >
                <svg 
                  xmlns="http://www.w3.org/2000/svg" 
                  className="h-5 w-5 mr-2" 
                  fill="none" 
                  viewBox="0 0 24 24" 
                  stroke="currentColor"
                >
                  <path 
                    strokeLinecap="round" 
                    strokeLinejoin="round" 
                    strokeWidth={2} 
                    d="M9 20l-5.447-2.724A1 1 0 013 16.382V5.618a1 1 0 011.447-.894L9 7m0 13l6-3m-6 3V7m6 10l4.553 2.276A1 1 0 0021 18.382V7.618a1 1 0 00-.553-.894L15 4m0 13V4m0 0L9 7" 
                  />
                </svg>
                Map View
              </button>
              
              {/* Recommendations Tab with Icon */}
              <button
                className={`py-2 px-4 flex items-center ${
                  activeTab === 'recommendations' 
                    ? 'border-b-2 border-blue-500 text-blue-500' 
                    : 'text-gray-500'
                }`}
                onClick={() => setActiveTab('recommendations')}
              >
                <svg 
                  xmlns="http://www.w3.org/2000/svg" 
                  className="h-5 w-5 mr-2" 
                  fill="none" 
                  viewBox="0 0 24 24" 
                  stroke="currentColor"
                >
                  <path 
                    strokeLinecap="round" 
                    strokeLinejoin="round" 
                    strokeWidth={2} 
                    d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" 
                  />
                </svg>
                Recommendations
              </button>
            </div>
          </div>
          
          {/* Content area */}
          <div className="h-full dashboard-content" style={{ zIndex: 10 }}>
            {activeTab === 'map' ? (
              <Map 
                userVisits={userVisits} 
                onMarkerClick={handleMarkerClick} 
              />
            ) : (
              <div className="h-full overflow-y-auto">
                <div className="p-4">
                  <h2 className="text-2xl font-bold mb-4">Recommended Destinations</h2>
                  <div className="space-y-4">
                    {recommendations.slice(0, 5).map(location => (
                      <LocationCard
                        key={location.id}
                        location={location}
                        isVisited={visitedLocationIds.has(location.id)}
                        onVisitChange={handleVisitChange}
                      />
                    ))}
                  </div>
                </div>
              </div>
            )}
          </div>
        </div>
        
        {/* Right side - Selected Location or Visits */}
        <div className="w-full md:w-1/3 bg-gray-100 p-4 overflow-y-auto">
          {selectedLocation ? (
            <div>
              <h2 className="text-xl font-bold mb-4">Location Details</h2>
              <LocationCard 
                location={selectedLocation} 
                isVisited={visitedLocationIds.has(selectedLocation.id)}
                onVisitChange={handleVisitChange}
                detailed={true}
              />
            </div>
          ) : (
            <div>
              <h2 className="text-xl font-bold mb-4">My Visited Places</h2>
              {userVisits.length > 0 ? (
                <div className="space-y-4">
                  {userVisits.map(visit => visit.location && (
                    <LocationCard 
                      key={visit.id}
                      location={visit.location}
                      isVisited={true}
                      onVisitChange={handleVisitChange}
                    />
                  ))}
                </div>
              ) : (
                <div className="bg-white rounded-lg p-4 shadow text-center">
                  <p className="text-gray-600 mb-4">
                    You haven't visited any places yet!
                  </p>
                  <p className="text-gray-600">
                    Click on a location on the map or in the recommendations 
                    section to add it to your visited places.
                  </p>
                </div>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default Dashboard;