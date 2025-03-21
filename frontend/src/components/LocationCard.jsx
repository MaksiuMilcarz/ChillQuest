import React, { useState, useEffect } from 'react';
import { addVisit, deleteVisit } from '../services/api';

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
  const [rating, setRating] = useState(isVisited?.rating || 0);
  const [notes, setNotes] = useState(isVisited?.notes || '');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  // Update local state when props change
  useEffect(() => {
    if (isVisited) {
      setRating(isVisited.rating || 0);
      setNotes(isVisited.notes || '');
    } else {
      setRating(0);
      setNotes('');
    }
  }, [isVisited]);

  // Ensure location object exists
  if (!location) {
    return <div className="bg-red-100 p-4 rounded-md">Location data not available</div>;
  }

  const handleVisitToggle = () => {
    if (onVisitChange) {
      console.log(`Toggling visit status for ${location.name} (ID: ${location.id}) to ${!isVisited}`);
      onVisitChange(location, !isVisited);
    }
  };

  return (
    <div className="bg-white rounded-lg shadow-md overflow-hidden">
      {/* Card Header */}
      <div className={`p-4 ${isVisited ? 'bg-green-50' : 'bg-gray-50'}`}>
        <h3 className="font-bold text-lg">{location.name}</h3>
        <p className="text-gray-600">
          {location.city}, {location.country}
        </p>
      </div>
      
      {/* Card Body */}
      <div className="p-4">
        <div className="flex justify-between items-center mb-2">
          <span className="text-sm font-medium text-gray-600">Type:</span>
          <span className="text-sm">{location.type}</span>
        </div>
        
        <div className="flex justify-between items-center">
          <span className="text-sm font-medium text-gray-600">Rating:</span>
          <div className="flex items-center">
            <span className="text-sm mr-1">{location.rating || 'N/A'}</span>
            {location.rating && (
              <svg
                xmlns="http://www.w3.org/2000/svg"
                className="h-4 w-4 text-yellow-500"
                fill="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"
                />
              </svg>
            )}
          </div>
        </div>
        
        {detailed && (
          <div className="mt-4">
            <p className="text-sm text-gray-600 mb-2">Location Type: {location.type}</p>
            {location.description && (
              <p className="text-sm text-gray-600">{location.description}</p>
            )}
          </div>
        )}
        
        {/* Visit Button */}
        <button
          onClick={handleVisitToggle}
          className={`mt-4 w-full py-2 px-4 rounded transition-colors ${
            isVisited
              ? 'bg-red-100 hover:bg-red-200 text-red-700'
              : 'bg-green-100 hover:bg-green-200 text-green-700'
          }`}
        >
          {isVisited ? 'Remove from Visited' : 'Mark as Visited'}
        </button>
      </div>
    </div>
  );
};

export default LocationCard;