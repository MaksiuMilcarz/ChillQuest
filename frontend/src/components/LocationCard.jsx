import React, { useState, useEffect } from 'react';
import { addVisit, deleteVisit } from '../services/api';

const LocationCard = ({ location, isVisited, onVisitChange }) => {
  const [rating, setRating] = useState(isVisited?.rating || 0);
  const [notes, setNotes] = useState(isVisited?.notes || '');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

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

  const handleVisitToggle = async () => {
    setLoading(true);
    setError('');
    
    try {
      console.log('Toggle visit for location:', location.id);
      
      if (isVisited) {
        // Delete visit
        await deleteVisit(isVisited.id);
        console.log('Visit deleted successfully');
        onVisitChange && onVisitChange(null);
      } else {
        // Add visit
        const visitData = {
          location_id: location.id,
          rating: rating > 0 ? rating : undefined,
          notes: notes || undefined
        };
        console.log('Adding visit with data:', visitData);
        
        const response = await addVisit(visitData);
        console.log('Visit added:', response);
        onVisitChange && onVisitChange(response.visit);
      }
    } catch (err) {
      console.error('Failed to update visit:', err);
      setError(err.response?.data?.message || 'Failed to update visit. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleRatingChange = async (newRating) => {
    if (!isVisited) return;
    
    setLoading(true);
    setError('');
    setRating(newRating);
    
    try {
      console.log('Updating rating for location:', location.id);
      
      const response = await addVisit({
        location_id: location.id,
        rating: newRating,
        notes
      });
      
      console.log('Rating updated:', response);
      onVisitChange && onVisitChange(response.visit);
    } catch (err) {
      console.error('Failed to update rating:', err);
      setError(err.response?.data?.message || 'Failed to update rating');
    } finally {
      setLoading(false);
    }
  };

  const handleNotesChange = async () => {
    if (!isVisited) return;
    
    setLoading(true);
    setError('');
    
    try {
      console.log('Updating notes for location:', location.id);
      
      const response = await addVisit({
        location_id: location.id,
        rating,
        notes
      });
      
      console.log('Notes updated:', response);
      onVisitChange && onVisitChange(response.visit);
    } catch (err) {
      console.error('Failed to update notes:', err);
      setError(err.response?.data?.message || 'Failed to update notes');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="bg-white rounded-lg shadow-md p-4 mb-4">
      <div className="flex justify-between items-start">
        <div>
          <h3 className="text-xl font-bold">{location.name}</h3>
          <p className="text-gray-600">{location.city}, {location.country}</p>
        </div>
        
        <div className="flex items-center">
          <span className="text-yellow-500 mr-1">★</span>
          <span>{location.rating ? location.rating.toFixed(1) : "N/A"}</span>
        </div>
      </div>
      
      <p className="mt-2 text-gray-700">{location.description || 'No description available.'}</p>
      
      <div className="flex items-center mt-2">
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
      
      <div className="mt-4">
        <button
          className={`px-4 py-2 rounded-md w-full ${
            isVisited 
              ? 'bg-red-500 hover:bg-red-600 text-white' 
              : 'bg-green-500 hover:bg-green-600 text-white'
          }`}
          onClick={handleVisitToggle}
          disabled={loading}
        >
          {loading ? 'Processing...' : isVisited ? 'Remove from Visited' : 'Mark as Visited'}
        </button>
      </div>
      
      {error && (
        <p className="mt-2 text-red-500 text-sm">{error}</p>
      )}
      
      {isVisited && (
        <div className="mt-4">
          <div className="mb-3">
            <label className="block text-gray-700 text-sm font-bold mb-2">
              Your Rating:
            </label>
            <div className="flex">
              {Array.from({ length: 5 }).map((_, i) => (
                <button
                  key={i}
                  onClick={() => handleRatingChange(i + 1)}
                  className={`text-2xl ${i < rating ? 'text-yellow-500' : 'text-gray-300'} focus:outline-none`}
                >
                  ★
                </button>
              ))}
            </div>
          </div>
          
          <div>
            <label className="block text-gray-700 text-sm font-bold mb-2">
              Notes:
            </label>
            <textarea
              className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
              rows="3"
              value={notes}
              onChange={(e) => setNotes(e.target.value)}
              onBlur={handleNotesChange}
              placeholder="Add your personal notes about this place..."
            ></textarea>
          </div>
        </div>
      )}
    </div>
  );
};

export default LocationCard;