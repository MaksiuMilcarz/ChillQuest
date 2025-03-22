import React, { useState, useEffect } from 'react';
import LocationCard from './LocationCard';

const RecommendationList = ({ recommendations = [], userVisits = [], onVisitChange }) => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  
  // Handle visit change - pass to parent
  const handleVisitChange = (location, isVisited, rating, notes) => {
    onVisitChange && onVisitChange(location, isVisited, rating, notes);
  };

  if (loading) return <div className="p-4">Loading popular destinations...</div>;
  if (error) return <div className="p-4 text-red-500">{error}</div>;
  
  return (
    <div className="p-4">
      <div className="mb-4">
        <h2 className="text-2xl font-bold flex items-center">
          <svg xmlns="http://www.w3.org/2000/svg" 
               className="h-6 w-6 mr-2" 
               fill="none" 
               viewBox="0 0 24 24" 
               stroke="currentColor">
            <path 
              strokeLinecap="round" 
              strokeLinejoin="round" 
              strokeWidth={2} 
              d="M11.049 2.927c.3-.921 1.603-.921 1.902 0l1.519 4.674a1 1 0 00.95.69h4.915c.969 0 1.371 1.24.588 1.81l-3.976 2.888a1 1 0 00-.363 1.118l1.518 4.674c.3.921-.755 1.688-1.538 1.118l-3.976-2.888a1 1 0 00-1.176 0l-3.976 2.888c-.783.57-1.838-.197-1.538-1.118l1.518-4.674a1 1 0 00-.363-1.118l-3.976-2.888c-.783-.57-.38-1.81.588-1.81h4.914a1 1 0 00.951-.69l1.519-4.674z"
            />
          </svg>
          Popular Destinations
        </h2>
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
              onVisitChange={(isVisited, rating, notes) => handleVisitChange(location, isVisited, rating, notes)}
            />
          ))}
        </div>
      )}
    </div>
  );
};

export default RecommendationList;