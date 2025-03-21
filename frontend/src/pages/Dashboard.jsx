import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import Map from '../components/Map';
import LocationCard from '../components/LocationCard';
import RecommendationList from '../components/RecommendationList';
import Navbar from '../components/Navbar';
import { getUserVisits, addVisit, deleteVisit } from '../services/api';
import { isAuthenticated } from '../services/auth';

const Dashboard = () => {
  const navigate = useNavigate();
  
  // Authentication state
  const [authenticated, setAuthenticated] = useState(isAuthenticated());
  
  // Content state
  const [userVisits, setUserVisits] = useState([]);
  const [selectedLocation, setSelectedLocation] = useState(null);
  const [activeTab, setActiveTab] = useState('map');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [visitSuccess, setVisitSuccess] = useState('');

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
        
        // Improved error handling with detailed information
        if (err.response) {
          console.error('Error response:', err.response.status, err.response.data);
          
          if (err.response.status === 422) {
            setError('Failed to load your visited locations. There was a validation error.');
          } else if (err.response.status === 401) {
            setError('Your session has expired. Please log in again.');
            navigate('/login');
          } else {
            setError(`Failed to load your visited locations. Server error: ${err.response.data.message || 'Unknown error'}`);
          }
        } else {
          setError('Failed to load your visited locations. Please try refreshing the page.');
        }
      } finally {
        setLoading(false);
      }
    };

    fetchUserVisits();
  }, [authenticated, navigate]);

  // Handle marker click on map
  const handleMarkerClick = (location) => {
    console.log('Location selected:', location);
    setSelectedLocation(location);
  };

  // Handle visit change (add/remove)
  const handleVisitChange = async (location, isVisited) => {
    try {
      setError('');
      setVisitSuccess('');
      
      if (isVisited) {
        // Add location to visited
        console.log(`Adding visit to ${location.name}`);
        const visitData = {
          location_id: location.id,
          rating: null,
          notes: ''
        };
        
        const response = await addVisit(visitData);
        console.log('Visit added:', response);
        
        if (response && response.visit) {
          // Add the new visit to the state
          setUserVisits(prev => [...prev, response.visit]);
          setVisitSuccess(`Added ${location.name} to your visited places!`);
          
          // Automatically clear success message after 3 seconds
          setTimeout(() => setVisitSuccess(''), 3000);
        }
      } else {
        // Remove location from visited
        console.log(`Removing visit to ${location.name}`);
        const visit = userVisits.find(v => v.location && v.location.id === location.id);
        
        if (visit) {
          await deleteVisit(visit.id);
          console.log('Visit deleted');
          
          // Remove the visit from state
          setUserVisits(prev => prev.filter(v => v.id !== visit.id));
          setVisitSuccess(`Removed ${location.name} from your visited places!`);
          
          // Automatically clear success message after 3 seconds
          setTimeout(() => setVisitSuccess(''), 3000);
        } else {
          console.error(`Couldn't find visit for location ${location.id}`);
          setError(`Could not find this location in your visits.`);
        }
      }
    } catch (err) {
      console.error('Error updating visit:', err);
      setError(err.message || 'Failed to update your visited locations.');
    }
  };

  // Check if a location is already visited
  const isLocationVisited = (locationId) => {
    return userVisits.some(visit => visit.location && visit.location.id === locationId);
  };

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
      
      {visitSuccess && (
        <div className="bg-green-100 border border-green-400 text-green-700 px-4 py-3 m-4 rounded">
          <p>{visitSuccess}</p>
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
          {selectedLocation ? (
            <div>
              <h2 className="text-xl font-bold mb-4">Location Details</h2>
              <LocationCard 
                location={selectedLocation} 
                isVisited={isLocationVisited(selectedLocation.id)}
                onVisitChange={handleVisitChange}
                detailed={true}
              />
            </div>
          ) : (
            <div>
              <h2 className="text-xl font-bold mb-4">My Visited Places</h2>
              {loading ? (
                <p>Loading your visits...</p>
              ) : userVisits.length > 0 ? (
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