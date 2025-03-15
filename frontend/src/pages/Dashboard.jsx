import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import Map from '../components/Map';
import LocationCard from '../components/LocationCard';
import RecommendationList from '../components/RecommendationList';
import Navbar from '../components/Navbar';
import { getUserVisits } from '../services/api';
import { isAuthenticated } from '../services/auth';

const Dashboard = () => {
  const [userVisits, setUserVisits] = useState([]);
  const [selectedLocation, setSelectedLocation] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [activeTab, setActiveTab] = useState('map'); // 'map' or 'recommendations'
  
  const navigate = useNavigate();
  const authenticated = isAuthenticated();

  // Load user visits when component mounts
  useEffect(() => {
    // Check if user is authenticated
    if (!authenticated) {
      console.log('User not authenticated, redirecting to login');
      navigate('/login');
      return;
    }

    // Fetch user visits
    const fetchUserVisits = async () => {
      setLoading(true);
      setError('');
      
      try {
        console.log('Fetching user visits...');
        const response = await getUserVisits();
        console.log('Visits response:', response);
        
        if (response && response.visits) {
          // Filter out visits without location data
          const validVisits = response.visits.filter(visit => visit.location);
          setUserVisits(validVisits);
          
          if (validVisits.length < response.visits.length) {
            console.warn(`Found ${response.visits.length - validVisits.length} visits with missing location data`);
          }
        } else {
          console.warn('No visits found in response:', response);
          setUserVisits([]);
        }
      } catch (err) {
        console.error('Failed to load user visits:', err);
        setError('Failed to load your visited locations. Please try refreshing the page.');
        
        // If unauthorized, redirect to login
        if (err.response && err.response.status === 401) {
          navigate('/login');
        }
      } finally {
        setLoading(false);
      }
    };

    fetchUserVisits();
  }, [authenticated, navigate]);

  const handleMarkerClick = (location) => {
    console.log('Location marker clicked:', location);
    setSelectedLocation(location);
  };

  const handleVisitChange = async (locationId, visit) => {
    try {
      if (visit) {
        console.log('Adding/updating visit for location:', locationId);
        // Add or update visit in local state
        const existingIndex = userVisits.findIndex(v => v.location_id === locationId);
        if (existingIndex >= 0) {
          const updatedVisits = [...userVisits];
          updatedVisits[existingIndex] = visit;
          setUserVisits(updatedVisits);
        } else {
          // Make sure the location data is included
          if (!visit.location && selectedLocation && selectedLocation.id === locationId) {
            visit.location = selectedLocation;
          }
          setUserVisits([...userVisits, visit]);
        }
      } else {
        console.log('Removing visit for location:', locationId);
        // Remove visit from local state
        setUserVisits(userVisits.filter(v => v.location_id !== locationId));
      }
    } catch (err) {
      console.error('Error updating visit:', err);
      setError('Failed to update visit. Please try again.');
    }
  };

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
          <div className="bg-white p-4 shadow-sm">
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
                {/* Map Icon */}
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
                {/* Magnifying Glass Icon */}
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
          
          <div className="h-full">
            {activeTab === 'map' ? (
              <Map 
                userVisits={userVisits} 
                onMarkerClick={handleMarkerClick} 
              />
            ) : (
              <div className="h-full overflow-y-auto">
                <RecommendationList 
                  userVisits={userVisits}
                  onVisitChange={handleVisitChange}
                />
              </div>
            )}
          </div>
        </div>
        
        {/* Right side - Selected Location or Visits */}
        <div className="w-full md:w-1/3 bg-gray-100 p-4 overflow-y-auto">
          <h2 className="text-2xl font-bold mb-4 flex items-center">
            {selectedLocation ? (
              <>
                <svg 
                  xmlns="http://www.w3.org/2000/svg" 
                  className="h-6 w-6 mr-2 text-blue-500" 
                  fill="none" 
                  viewBox="0 0 24 24" 
                  stroke="currentColor"
                >
                  <path 
                    strokeLinecap="round" 
                    strokeLinejoin="round" 
                    strokeWidth={2} 
                    d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" 
                  />
                  <path 
                    strokeLinecap="round" 
                    strokeLinejoin="round" 
                    strokeWidth={2} 
                    d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" 
                  />
                </svg>
                Selected Location
              </>
            ) : (
              <>
                <svg 
                  xmlns="http://www.w3.org/2000/svg" 
                  className="h-6 w-6 mr-2 text-green-500" 
                  fill="none" 
                  viewBox="0 0 24 24" 
                  stroke="currentColor"
                >
                  <path 
                    strokeLinecap="round" 
                    strokeLinejoin="round" 
                    strokeWidth={2} 
                    d="M5 13l4 4L19 7" 
                  />
                </svg>
                Your Visited Places
              </>
            )}
          </h2>
          
          {selectedLocation ? (
            <LocationCard
              location={selectedLocation}
              isVisited={userVisits.find(v => v.location_id === selectedLocation.id)}
              onVisitChange={(visit) => handleVisitChange(selectedLocation.id, visit)}
            />
          ) : userVisits.length === 0 ? (
            <div className="bg-white rounded-lg shadow p-6 text-center">
              <p className="text-lg text-gray-600">
                You haven't visited any places yet. 
              </p>
              <p className="text-gray-600 mt-2">
                Click on a marker on the map to add your first visit!
              </p>
            </div>
          ) : (
            <div>
              {userVisits
                .filter(visit => visit.location) // Only show visits with location data
                .map(visit => (
                  <LocationCard
                    key={visit.id}
                    location={visit.location}
                    isVisited={visit}
                    onVisitChange={(updatedVisit) => 
                      handleVisitChange(visit.location_id, updatedVisit)
                    }
                  />
                ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default Dashboard;