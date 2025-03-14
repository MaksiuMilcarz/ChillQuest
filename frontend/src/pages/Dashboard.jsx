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
          setUserVisits(response.visits);
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
      
      <div className="flex-grow flex">
        {/* Left side - Map or Recommendations */}
        <div className="w-2/3 h-full overflow-hidden">
          <div className="bg-white p-4 shadow-sm">
            <div className="flex border-b">
              <button
                className={`py-2 px-4 ${
                  activeTab === 'map' 
                    ? 'border-b-2 border-blue-500 text-blue-500' 
                    : 'text-gray-500'
                }`}
                onClick={() => setActiveTab('map')}
              >
                Map View
              </button>
              <button
                className={`py-2 px-4 ${
                  activeTab === 'recommendations' 
                    ? 'border-b-2 border-blue-500 text-blue-500' 
                    : 'text-gray-500'
                }`}
                onClick={() => setActiveTab('recommendations')}
              >
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
        <div className="w-1/3 bg-gray-100 p-4 overflow-y-auto">
          <h2 className="text-2xl font-bold mb-4">
            {selectedLocation ? 'Selected Location' : 'Your Visited Places'}
          </h2>
          
          {selectedLocation ? (
            <LocationCard
              location={selectedLocation}
              isVisited={userVisits.find(v => v.location_id === selectedLocation.id)}
              onVisitChange={(visit) => handleVisitChange(selectedLocation.id, visit)}
            />
          ) : userVisits.length === 0 ? (
            <p>You haven't visited any places yet. Click on a marker on the map to add your first visit!</p>
          ) : (
            <div>
              {userVisits.map(visit => (
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