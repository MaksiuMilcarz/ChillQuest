import React, { useState } from 'react';
import { addVisit } from '../services/api';

// Category icon mapping
const CategoryIcon = ({ type }) => {
  switch (type) {
    case 'nature':
      return (
        <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6 text-green-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 3v4M3 5h4M6 17v4m-2-2h4m5-16l2.286 6.857L21 12l-5.714 2.143L13 21l-2.286-6.857L5 12l5.714-2.143L13 3z" />
        </svg>
      );
    case 'recreational':
      return (
        <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6 text-blue-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M14.828 14.828a4 4 0 01-5.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
      );
    case 'nightlife':
      return (
        <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6 text-purple-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
        </svg>
      );
    case 'culture':
      return (
        <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6 text-red-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 14v3m4-3v3m4-3v3M3 21h18M3 10h18M3 7l9-4 9 4M4 10h16v11H4V10z" />
        </svg>
      );
    case 'food':
      return (
        <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6 text-yellow-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
      );
    default:
      return (
        <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6 text-gray-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
        </svg>
      );
  }
};

// Category name formatting
const getCategoryName = (type) => {
  switch (type) {
    case 'nature':
      return 'Nature & Outdoors';
    case 'recreational':
      return 'Fun & Entertainment';
    case 'nightlife':
      return 'Nightlife & Parties';
    case 'culture':
      return 'Culture & History';
    case 'food':
      return 'Food & Dining';
    default:
      return type ? type.charAt(0).toUpperCase() + type.slice(1) : 'Unknown';
  }
};

const LocationCard = ({ location, isVisited, onVisitChange, detailed = false }) => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  const handleVisitToggle = async () => {
    if (!location || !location.id) {
      setError('Invalid location data');
      return;
    }
    
    setLoading(true);
    setError('');
    setSuccess('');
    
    try {
      if (isVisited) {
        // The parent component handles removal
        if (onVisitChange) {
          onVisitChange(location, false);
        }
      } else {
        // Add a visit with direct API call for simplicity
        console.log(`Adding visit for location ${location.id}`);
        await addVisit(location.id);
        setSuccess('Location marked as visited!');
        
        // Notify parent component
        if (onVisitChange) {
          onVisitChange(location, true);
        }
      }
    } catch (err) {
      console.error('Failed to update visit:', err);
      setError('Failed to update. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  // Ensure location object exists
  if (!location) {
    return <div className="bg-red-100 p-4 rounded-md">Location data not available</div>;
  }

  return (
    <div className="bg-white rounded-lg shadow-md overflow-hidden mb-4">
      {/* Card Header */}
      <div className={`p-4 ${isVisited ? 'bg-green-50' : 'bg-gray-50'}`}>
        <div className="flex justify-between items-start">
          <div className="flex items-center">
            <CategoryIcon type={location.type} />
            <div className="ml-2">
              <h3 className="text-xl font-bold">{location.name}</h3>
              <p className="text-gray-600">{location.city}, {location.country}</p>
            </div>
          </div>
          
          <div className="flex items-center">
            <span className="text-yellow-500 mr-1">★</span>
            <span>{location.rating ? location.rating.toFixed(1) : "N/A"}</span>
          </div>
        </div>
      </div>
      
      {/* Card Body */}
      <div className="p-4">
        {/* Category badge */}
        <div className="mt-2 mb-2">
          <span className="inline-block bg-gray-100 rounded-full px-3 py-1 text-sm font-semibold text-gray-700">
            {getCategoryName(location.type)}
          </span>
        </div>
        
        {/* Description */}
        {detailed && location.description && (
          <p className="mt-2 mb-4 text-gray-700">{location.description}</p>
        )}
        
        {/* Price level */}
        <div className="flex items-center mt-2 mb-4">
          <span className="text-gray-700 mr-2">Price Level:</span>
          <div className="flex">
            {Array.from({ length: 5 }).map((_, i) => (
              <span 
                key={i} 
                className={`${i < (location.price_level || 0) ? 'text-green-500' : 'text-gray-300'}`}
              >
                $
              </span>
            ))}
          </div>
        </div>
        
        {/* Visit button */}
        <button
          className={`w-full py-2 px-4 rounded transition-colors ${
            isVisited
              ? 'bg-red-500 hover:bg-red-600 text-white'
              : 'bg-green-500 hover:bg-green-600 text-white'
          }`}
          onClick={handleVisitToggle}
          disabled={loading}
        >
          {loading ? 'Processing...' : isVisited ? 'Remove from Visited' : 'Mark as Visited'}
        </button>
        
        {error && (
          <p className="mt-2 text-red-500 text-sm">{error}</p>
        )}
        
        {success && (
          <p className="mt-2 text-green-500 text-sm">{success}</p>
        )}
      </div>
    </div>
  );
};

export default LocationCard;