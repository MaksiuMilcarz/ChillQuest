import React, { useState, useEffect } from 'react';
import { getRecommendations, getPersonalizedRecommendations } from '../services/api';
import { isAuthenticated } from '../services/auth';
import LocationCard from './LocationCard';

const RecommendationList = ({ userVisits = [], onVisitChange }) => {
  const [recommendations, setRecommendations] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [usePersonalization, setUsePersonalization] = useState(true);
  
  const authenticated = isAuthenticated();

  useEffect(() => {
    const fetchRecommendations = async () => {
      setLoading(true);
      setError('');
      
      try {
        let data;
        if (authenticated) {
          console.log('Fetching personalized recommendations');
          data = await getPersonalizedRecommendations(usePersonalization);
        } else {
          console.log('Fetching general recommendations');
          data = await getRecommendations();
        }
        
        if (data && data.recommendations) {
          console.log(`Received ${data.recommendations.length} recommendations`);
          setRecommendations(data.recommendations);
        } else {
          console.warn('Invalid recommendations data:', data);
          setRecommendations([]);
        }
      } catch (err) {
        console.error('Failed to load recommendations:', err);
        setError('Failed to load recommendations. Please try again.');
      } finally {
        setLoading(false);
      }
    };

    fetchRecommendations();
  }, [authenticated, usePersonalization]);

  const handleVisitChange = (locationId, visit) => {
    onVisitChange && onVisitChange(locationId, visit);
  };

  const togglePersonalization = () => {
    setUsePersonalization(!usePersonalization);
  };

  if (loading) return <div className="p-4">Loading recommendations...</div>;
  if (error) return <div className="p-4 text-red-500">{error}</div>;

  return (
    <div className="p-4">
      <div className="flex justify-between items-center mb-4">
        <h2 className="text-2xl font-bold">
          {authenticated && usePersonalization ? 'Personalized Recommendations' : 'Popular Destinations'}
        </h2>
        
        {authenticated && (
          <div className="flex items-center">
            <span className="mr-2 text-sm">Personalized:</span>
            <label className="inline-flex items-center cursor-pointer">
              <input 
                type="checkbox" 
                className="sr-only peer"
                checked={usePersonalization}
                onChange={togglePersonalization}
              />
              <div className="relative w-11 h-6 bg-gray-200 rounded-full peer peer-focus:ring-4 peer-focus:ring-blue-300 peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-0.5 after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-blue-600"></div>
            </label>
          </div>
        )}
      </div>
      
      {recommendations.length === 0 ? (
        <p>No recommendations available at this time.</p>
      ) : (
        <div>
          {recommendations.map(location => (
            <LocationCard
              key={location.id}
              location={location}
              isVisited={userVisits.find(v => v.location_id === location.id)}
              onVisitChange={(visit) => handleVisitChange(location.id, visit)}
            />
          ))}
        </div>
      )}
    </div>
  );
};

export default RecommendationList;