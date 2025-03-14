import React, { useState, useEffect } from 'react';
import { MapContainer, TileLayer, Marker, Popup } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import L from 'leaflet';
import { getAllLocations } from '../services/api';

// Fix Leaflet icon issues
const customIcon = L.icon({
  iconUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon.png',
  shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-shadow.png',
  iconSize: [25, 41],
  iconAnchor: [12, 41],
  popupAnchor: [1, -34],
  shadowSize: [41, 41]
});

// Create a custom icon for visited locations
const visitedIcon = L.icon({
  iconUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon.png',
  shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-shadow.png',
  iconSize: [25, 41],
  iconAnchor: [12, 41],
  popupAnchor: [1, -34],
  shadowSize: [41, 41]
});

const Map = ({ userVisits = [], onMarkerClick }) => {
  const [locations, setLocations] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchLocations = async () => {
      try {
        console.log('Fetching locations for map...');
        const response = await getAllLocations();
        console.log('Locations fetched:', response);
        
        if (response && response.locations) {
          setLocations(response.locations);
        } else {
          throw new Error('Invalid location data format');
        }
      } catch (err) {
        console.error('Failed to load map locations:', err);
        setError('Failed to load map locations. Please try refreshing the page.');
      } finally {
        setLoading(false);
      }
    };

    fetchLocations();
  }, []);

  // Create a set of location IDs that user has visited
  const visitedLocationIds = new Set(userVisits.map(visit => visit.location_id));

  if (loading) return <div className="h-full flex items-center justify-center">Loading map...</div>;
  if (error) return <div className="h-full flex items-center justify-center text-red-500">{error}</div>;

  return (
    <MapContainer 
      center={[20, 0]} 
      zoom={2} 
      style={{ height: '100%', width: '100%' }}
      scrollWheelZoom={true}
    >
      <TileLayer
        attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
      />
      
      {locations.map(location => (
        <Marker 
          key={location.id} 
          position={[location.latitude, location.longitude]}
          icon={visitedLocationIds.has(location.id) ? visitedIcon : customIcon}
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
            </div>
          </Popup>
        </Marker>
      ))}
    </MapContainer>
  );
};

export default Map;