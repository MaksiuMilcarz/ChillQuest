import React, { useState, useEffect, useCallback } from 'react';
import { useNavigate } from 'react-router-dom';
import Map from '../components/Map';
import LocationCard from '../components/LocationCard';
import Navbar from '../components/Navbar';
import { getUserVisits, getAllLocations, addVisit, deleteVisit } from '../services/api';
import { isAuthenticated } from '../services/auth';

const Dashboard = () => {
  const navigate = useNavigate();
  
  // State
  const [userVisits, setUserVisits] = useState([]);
  const [selectedLocation, setSelectedLocation] = useState(null);
  const [locations, setLocations] = useState([]);
  const [recommendations, setRecommendations] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [activeTab, setActiveTab] = useState('map');
  const [visitedLocationIds, setVisitedLocationIds] = useState(new Set());
  
  // Function to update recommendations - separated as requested
  const updateRecommendations = useCallback((allLocations, visitedIds) => {
    if (!allLocations || allLocations.length === 0) return [];
    
    // Filter out visited locations
    const unvisitedLocations = allLocations.filter(
      location => !visitedIds.has(location.id)
    );
    
    // Randomize selection from unvisited locations
    let shuffled = [...unvisitedLocations].sort(() => 0.5 - Math.random());
    
    // Select up to 10 random locations for recommendations
    const randomRecommendations = shuffled.slice(0, 10);
    
    console.log(`Generated ${randomRecommendations.length} new recommendations`);
    return randomRecommendations;
  }, []);
  
  // Load data when component mounts
  useEffect(() => {
    if (!isAuthenticated()) {
      navigate('/login');
      return;
    }

    const loadData = async () => {
      setLoading(true);
      setError('');
      
      try {
        // Load data in parallel for better performance
        const [locationsData, visitsData] = await Promise.all([
          getAllLocations(),
          getUserVisits().catch(err => {
            console.error('Failed to load visits:', err);
            return { visits: [] };
          })
        ]);
        
        // Update locations state
        let allLocations = [];
        if (locationsData?.locations) {
          allLocations = locationsData.locations;
          setLocations(allLocations);
        }
        
        // Process visits
        let visitedIds = new Set();
        if (visitsData?.visits) {
          const validVisits = visitsData.visits.filter(visit => visit.location);
          setUserVisits(validVisits);
          
          // Create a set of visited location IDs for quick lookup
          visitedIds = new Set();
          validVisits.forEach(visit => {
            if (visit.location) {
              visitedIds.add(visit.location.id);
            }
          });
          setVisitedLocationIds(visitedIds);
        }
        
        // Generate initial recommendations
        const newRecommendations = updateRecommendations(allLocations, visitedIds);
        setRecommendations(newRecommendations);
      } catch (err) {
        console.error('Failed to load dashboard data:', err);
        setError('Failed to load dashboard data. Please try refreshing the page.');
      } finally {
        setLoading(false);
      }
    };
    
    loadData();
  }, [navigate, updateRecommendations]);
  
  // Handle marker click on map
  const handleMarkerClick = (location) => {
    setSelectedLocation(location);
  };
  
  // Return to overview
  const handleReturnToOverview = () => {
    setSelectedLocation(null);
  };
  
  // Handle visit toggle (add/remove)
  const handleVisitChange = async (location, isNowVisited, rating = null, notes = '') => {
    try {
      if (isNowVisited) {
        // Add visit - rating is required
        if (rating === null || rating < 1) {
          setError('Please provide a rating (1-5) before marking as visited');
          return;
        }
        
        const response = await addVisit(location.id, rating, notes);
        console.log('Visit added:', response);
        
        if (response && response.visit) {
          // Add to state
          setUserVisits(prev => [...prev, response.visit]);
          
          // Update visited IDs
          setVisitedLocationIds(prev => {
            const newSet = new Set([...prev]);
            newSet.add(location.id);
            return newSet;
          });
          
          setSuccess(`Added ${location.name} to your visited places!`);
          
          // Clear success message after 3 seconds
          setTimeout(() => setSuccess(''), 3000);
          
          // Update recommendations after adding visit
          setRecommendations(prev => 
            updateRecommendations(locations, new Set([...visitedLocationIds, location.id]))
          );
        }
      } else {
        // Find the visit to remove
        const visit = userVisits.find(v => v.location && v.location.id === location.id);
        
        if (visit) {
          // Remove visit
          await deleteVisit(visit.id);
          
          // Update state
          setUserVisits(prev => prev.filter(v => v.id !== visit.id));
          
          // Update visited IDs
          setVisitedLocationIds(prev => {
            const newSet = new Set([...prev]);
            newSet.delete(location.id);
            return newSet;
          });
          
          setSuccess(`Removed ${location.name} from your visited places!`);
          
          // Clear success message after 3 seconds
          setTimeout(() => setSuccess(''), 3000);
          
          // If we're removing the selected location, deselect it
          if (selectedLocation && selectedLocation.id === location.id) {
            setSelectedLocation(null);
          }
          
          // Update recommendations after removing visit
          const newVisitedIds = new Set([...visitedLocationIds]);
          newVisitedIds.delete(location.id);
          setRecommendations(prev => 
            updateRecommendations(locations, newVisitedIds)
          );
        }
      }
    } catch (err) {
      console.error('Failed to update visit:', err);
      setError(`Failed to ${isNowVisited ? 'add' : 'remove'} visit: ${err.message}`);
    }
  };
  
  // Effect to refresh recommendations when switching to recommendations tab
  useEffect(() => {
    if (activeTab === 'recommendations' && !loading) {
      // Generate new recommendations when tab is selected
      setRecommendations(updateRecommendations(locations, visitedLocationIds));
    }
  }, [activeTab, loading, locations, updateRecommendations, visitedLocationIds]);
  
  // Check if a location is already visited
  const isLocationVisited = (locationId) => {
    return visitedLocationIds.has(locationId);
  };
  
  // Get visit details for a location
  const getVisitDetails = (locationId) => {
    return userVisits.find(visit => visit.location && visit.location.id === locationId);
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
            onClick={() => setError('')}
            className="underline mt-2"
          >
            Dismiss
          </button>
        </div>
      )}
      
      {success && (
        <div className="bg-green-100 border border-green-400 text-green-700 px-4 py-3 m-4 rounded">
          <p>{success}</p>
        </div>
      )}
      
      <div className="flex-grow flex flex-col md:flex-row">
        {/* Left side - Map or Recommendations */}
        <div className="w-full md:w-2/3 h-[60vh] md:h-full overflow-hidden">
          {/* Tabs - with fixed position to ensure they're always visible */}
          <div className="bg-white p-4 shadow-md sticky top-0 z-50">
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
          <div className="h-full relative" style={{ height: 'calc(100% - 73px)' }}>
            {activeTab === 'map' ? (
              <Map 
                userVisits={userVisits} 
                onMarkerClick={handleMarkerClick}
              />
            ) : (
              <div className="h-full overflow-y-auto">
                <div className="p-4">
                  <h2 className="text-2xl font-bold mb-4">
                    Recommended Destinations
                    <button 
                      onClick={() => setRecommendations(updateRecommendations(locations, visitedLocationIds))}
                      className="ml-4 text-sm bg-blue-500 hover:bg-blue-600 text-white px-3 py-1 rounded"
                      title="Get new recommendations"
                    >
                      Refresh
                    </button>
                  </h2>
                  <div className="space-y-4">
                    {recommendations.length > 0 ? (
                      recommendations.map(location => (
                        <LocationCard
                          key={location.id}
                          location={location}
                          isVisited={isLocationVisited(location.id)}
                          visitDetails={getVisitDetails(location.id)}
                          onVisitChange={handleVisitChange}
                          requireRating={true}
                        />
                      ))
                    ) : (
                      <p>No recommendations available. You might have visited all locations!</p>
                    )}
                  </div>
                </div>
              </div>
            )}
          </div>
        </div>
        
        {/* Right side - Selected Location or Brief Stats */}
        <div className="w-full md:w-1/3 bg-gray-100 p-4 overflow-y-auto">
          {selectedLocation ? (
            <div>
              <div className="flex justify-between items-center mb-4">
                <h2 className="text-2xl font-bold">Location Details</h2>
                <button 
                  onClick={handleReturnToOverview}
                  className="bg-gray-200 hover:bg-gray-300 text-gray-800 px-3 py-1 rounded flex items-center"
                >
                  <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 19l-7-7m0 0l7-7m-7 7h18" />
                  </svg>
                  Back to Overview
                </button>
              </div>
              <LocationCard 
                location={selectedLocation} 
                isVisited={isLocationVisited(selectedLocation.id)}
                visitDetails={getVisitDetails(selectedLocation.id)}
                onVisitChange={handleVisitChange}
                detailed={true}
                requireRating={true}
              />
            </div>
          ) : (
            <div>
              <h2 className="text-2xl font-bold mb-4">Your Travel Stats</h2>
              
              {/* Summary stats cards */}
              <div className="grid grid-cols-2 gap-4 mb-6">
                <div className="bg-blue-100 p-4 rounded-lg text-center">
                  <p className="text-3xl font-bold text-blue-600">{userVisits.length}</p>
                  <p className="text-gray-700">Places Visited</p>
                </div>
                
                <div className="bg-green-100 p-4 rounded-lg text-center">
                  <p className="text-3xl font-bold text-green-600">
                    {new Set(userVisits.map(v => v.location?.country).filter(Boolean)).size}
                  </p>
                  <p className="text-gray-700">Countries</p>
                </div>
              </div>
              
              <div className="bg-white rounded-lg p-4 shadow mb-4">
                <h3 className="font-bold text-lg mb-2">How to Use</h3>
                <p className="text-gray-600 mb-2">
                  Click on a location on the map or in the recommendations section to view its details and mark it as visited.
                </p>
                <p className="text-gray-600">
                  When marking a location as visited, you'll need to provide a rating from 1 to 5 stars.
                </p>
              </div>
              
              {userVisits.length > 0 && (
                <div className="bg-white rounded-lg p-4 shadow">
                  <h3 className="font-bold text-lg mb-2">Recent Visits</h3>
                  <ul className="divide-y divide-gray-200">
                    {userVisits
                      .slice(0, 3) // Only show 3 most recent visits
                      .map(visit => visit.location && (
                        <li key={visit.id} className="py-2">
                          <div className="flex justify-between">
                            <p className="font-medium">{visit.location.name}</p>
                            <div className="flex items-center">
                              <span className="text-yellow-500 mr-1">★</span>
                              <span>{visit.rating || "N/A"}</span>
                            </div>
                          </div>
                          <p className="text-sm text-gray-600">{visit.location.city}, {visit.location.country}</p>
                        </li>
                      ))}
                  </ul>
                  <button 
                    className="mt-3 text-blue-500 text-sm"
                    onClick={() => setActiveTab('map')}
                  >
                    View all on map
                  </button>
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