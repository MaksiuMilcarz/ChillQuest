import React, { useState, useEffect, useRef } from 'react';
import { MapContainer, TileLayer, Marker, Popup } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import L from 'leaflet';
import { getAllLocations, getRecommendations } from '../services/api';

// Custom hook to handle icon loading
function useLeafletIcons() {
  const [iconsLoaded, setIconsLoaded] = useState(false);
  
  // Create refs for all custom icons
  const defaultIconRef = useRef(null);
  const visitedIconRef = useRef(null);
  const recommendedIconRef = useRef(null);
  
  useEffect(() => {
    // Set a timeout to ensure we don't hang indefinitely
    const loadTimeout = setTimeout(() => {
      console.log("Icon loading timed out, proceeding anyway");
      if (!iconsLoaded) {
        setIconsLoaded(true);
      }
    }, 3000); // 3 second timeout
    
    // Create the icons only once
    defaultIconRef.current = new L.Icon({
      iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-blue.png',
      shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-shadow.png',
      iconSize: [25, 41],
      iconAnchor: [12, 41],
      popupAnchor: [1, -34],
      shadowSize: [41, 41]
    });
    
    visitedIconRef.current = new L.Icon({
      iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-green.png',
      shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-shadow.png',
      iconSize: [25, 41],
      iconAnchor: [12, 41],
      popupAnchor: [1, -34],
      shadowSize: [41, 41]
    });
    
    recommendedIconRef.current = new L.Icon({
      iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-gold.png',
      shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-shadow.png',
      iconSize: [25, 41],
      iconAnchor: [12, 41],
      popupAnchor: [1, -34],
      shadowSize: [41, 41]
    });
    
    // Immediately set icons as loaded since we're creating them synchronously
    console.log("Icons created, proceeding with map rendering");
    setIconsLoaded(true);
    
    // Preload images in the background (not blocking)
    const iconUrls = [
      'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-blue.png',
      'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-green.png',
      'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-gold.png',
      'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-shadow.png'
    ];
    
    iconUrls.forEach(url => {
      const img = new Image();
      img.src = url;
    });
    
    return () => {
      clearTimeout(loadTimeout);
    };
  }, []);
  
  // Return the icons and loading state
  return { 
    defaultIcon: defaultIconRef.current, 
    visitedIcon: visitedIconRef.current, 
    recommendedIcon: recommendedIconRef.current,
    iconsLoaded 
  };
}

const Map = ({ userVisits = [], onMarkerClick }) => {
  const [locations, setLocations] = useState([]);
  const [recommendedLocationIds, setRecommendedLocationIds] = useState(new Set()); 
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const { defaultIcon, visitedIcon, recommendedIcon, iconsLoaded } = useLeafletIcons();
  
  // Only fetch data and render map when icons are loaded
  useEffect(() => {
    if (iconsLoaded) {
      const fetchData = async () => {
        setLoading(true);
        setError(null);
        
        try {
          // Use Promise.all to fetch locations and recommendations in parallel
          const [locationsResponse, recommendationsResponse] = await Promise.all([
            getAllLocations(),
            getRecommendations()
          ]);
          
          console.log('Locations response:', locationsResponse);
          console.log('Recommendations response:', recommendationsResponse);
          
          // Process locations
          if (locationsResponse && locationsResponse.locations) {
            setLocations(locationsResponse.locations);
          } else {
            throw new Error('Invalid location data format');
          }
          
          // Process recommendations
          if (recommendationsResponse && recommendationsResponse.recommendations) {
            // Create a set of recommended location IDs for easy lookup
            const recIds = new Set(recommendationsResponse.recommendations.map(loc => loc.id));
            setRecommendedLocationIds(recIds);
            console.log('Recommended location IDs:', [...recIds]);
          }
        } catch (err) {
          console.error('Failed to load map data:', err);
          setError('Failed to load map data. Please try refreshing the page.');
          
          // If at least locations loaded, show them anyway
          if (locations.length === 0) {
            try {
              const fallbackLocations = await getAllLocations();
              if (fallbackLocations && fallbackLocations.locations) {
                setLocations(fallbackLocations.locations);
              }
            } catch (fallbackErr) {
              console.error('Failed to load fallback locations:', fallbackErr);
            }
          }
        } finally {
          setLoading(false);
        }
      };

      fetchData();
    }
  }, [iconsLoaded, userVisits]); // This ensures the map refreshes when user visits change

  // Debug user visits whenever they change
  useEffect(() => {
    console.log('User visits updated:', userVisits);
    // Print out location IDs that should be marked as visited
    if (userVisits && userVisits.length > 0) {
      const visitedIds = userVisits.map(visit => visit.location_id);
      console.log('Visited location IDs:', visitedIds);
    }
  }, [userVisits]);

  // Create a set of location IDs that user has visited (for quick lookup)
  const visitedLocationIds = new Set(userVisits.map(visit => visit.location_id));

  // Helper function to determine which icon to use
  const getMarkerIcon = (locationId) => {
    if (visitedLocationIds.has(locationId)) {
      return visitedIcon;
    } else if (recommendedLocationIds.has(locationId)) {
      return recommendedIcon;
    }
    return defaultIcon;
  };

  if (!iconsLoaded || loading) return <div className="h-full flex items-center justify-center">Loading map...</div>;
  if (error) return <div className="h-full flex items-center justify-center text-red-500">{error}</div>;

  return (
    <div className="h-full w-full relative">
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
      <div className="absolute bottom-5 left-5 bg-white p-2 rounded shadow z-[1000]">
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