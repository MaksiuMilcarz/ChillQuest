import React, { useState, useEffect, useRef } from 'react';
import { MapContainer, TileLayer, Marker, Popup } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import L from 'leaflet';

// Custom icon for different location types
const createCustomIcon = (iconUrl) => {
  return new L.Icon({
    iconUrl,
    iconSize: [25, 41],
    iconAnchor: [12, 41],
    popupAnchor: [1, -34],
    shadowSize: [41, 41],
    shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-shadow.png',
  });
};

const Map = ({ userVisits = [], locations = [], recommendations = [], onMarkerClick }) => {
  // State
  const [visitedLocationIds, setVisitedLocationIds] = useState(new Set());
  const [recommendedLocationIds, setRecommendedLocationIds] = useState(new Set());
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [mappableLocations, setMappableLocations] = useState([]);
  
  // Icons for different location types
  const regularIcon = useRef(null);
  const visitedIcon = useRef(null);
  const recommendedIcon = useRef(null);
  
  // Initialize icons
  useEffect(() => {
    try {
      regularIcon.current = createCustomIcon('https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon.png');
      visitedIcon.current = createCustomIcon('https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-green.png');
      recommendedIcon.current = createCustomIcon('https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-gold.png');
      setLoading(false);
    } catch (err) {
      console.error('Error initializing map icons:', err);
      setError('Failed to initialize map icons.');
      setLoading(false);
    }
  }, []);
  
  // Update visited locations when userVisits changes
  useEffect(() => {
    if (userVisits && userVisits.length > 0) {
      const visitedIds = new Set();
      userVisits.forEach(visit => {
        if (visit.location && visit.location.id) {
          visitedIds.add(visit.location.id);
        } else if (visit.location_id) {
          visitedIds.add(visit.location_id);
        }
      });
      setVisitedLocationIds(visitedIds);
    } else {
      setVisitedLocationIds(new Set());
    }
  }, [userVisits]);
  
  // Update recommended locations
  useEffect(() => {
    if (recommendations && recommendations.length > 0) {
      const recommendedIds = new Set(recommendations.map(rec => rec.id));
      setRecommendedLocationIds(recommendedIds);
    } else {
      setRecommendedLocationIds(new Set());
    }
  }, [recommendations]);
  
  // Update mappable locations
  useEffect(() => {
    if (locations && locations.length > 0) {
      // Filter out any locations without proper coordinates
      const validLocations = locations.filter(
        loc => loc && typeof loc.latitude === 'number' && typeof loc.longitude === 'number'
      );
      setMappableLocations(validLocations);
    } else {
      setMappableLocations([]);
    }
  }, [locations]);
  
  // Get the appropriate marker icon based on location status
  const getMarkerIcon = (locationId) => {
    if (visitedLocationIds.has(locationId)) {
      return visitedIcon.current;
    }
    if (recommendedLocationIds.has(locationId)) {
      return recommendedIcon.current;
    }
    return regularIcon.current;
  };
  
  if (loading) return <div className="h-full flex items-center justify-center">Loading map...</div>;
  if (error) return <div className="h-full flex items-center justify-center text-red-500">{error}</div>;
  
  return (
    <div className="h-full w-full relative" style={{ zIndex: 0 }}>
      <MapContainer 
        center={[20, 0]} 
        zoom={2} 
        className="map-container"
        style={{ height: 'calc(100% - 10px)', width: '100%', zIndex: 0 }}
        scrollWheelZoom={true}
        zoomControl={true}
      >
        <TileLayer
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />
        
        {mappableLocations.map(location => (
          <Marker 
            key={location.id} 
            position={[location.latitude, location.longitude]}
            icon={getMarkerIcon(location.id)}
            eventHandlers={{
              click: () => onMarkerClick && onMarkerClick(location)
            }}
          >
            <Popup>
              <div>
                <h3 className="font-bold">{location.name}</h3>
                <p>{location.city}, {location.country}</p>
                <p>Type: {location.type}</p>
                <p>Rating: {location.rating}/5</p>
                {visitedLocationIds.has(location.id) && (
                  <p className="text-green-600 font-semibold">✓ Visited</p>
                )}
                {recommendedLocationIds.has(location.id) && (
                  <p className="text-yellow-500 font-semibold">⭐ Recommended</p>
                )}
              </div>
            </Popup>
          </Marker>
        ))}
      </MapContainer>
      
      {/* Map Legend */}
      <div className="absolute bottom-5 left-5 bg-white p-2 rounded shadow map-legend" style={{ zIndex: 1000 }}>
        <div className="flex items-center mb-1">
          <div className="w-4 h-4 bg-blue-500 rounded-full mr-2"></div>
          <span>Regular Location</span>
        </div>
        <div className="flex items-center mb-1">
          <div className="w-4 h-4 bg-green-500 rounded-full mr-2"></div>
          <span>Visited</span>
        </div>
        <div className="flex items-center">
          <div className="w-4 h-4 bg-yellow-500 rounded-full mr-2"></div>
          <span>Recommended</span>
        </div>
      </div>
    </div>
  );
};

export default Map;