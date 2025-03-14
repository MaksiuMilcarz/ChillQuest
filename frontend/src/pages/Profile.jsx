import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { getUser } from '../services/auth';
import { getUserVisits } from '../services/api';
import Navbar from '../components/Navbar';

const Profile = () => {
  const [user, setUser] = useState(null);
  const [visits, setVisits] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const navigate = useNavigate();
  
  useEffect(() => {
    const fetchUserData = async () => {
      setLoading(true);
      setError('');
      
      try {
        console.log('Fetching user profile...');
        
        // First check if we have user data in localStorage
        const storedUser = localStorage.getItem('user');
        if (storedUser) {
          const parsedUser = JSON.parse(storedUser);
          console.log('User data from localStorage:', parsedUser);
          setUser(parsedUser);
        } else {
          // If not, try to fetch from API
          const userData = await getUser();
          console.log('User data from API:', userData);
          if (userData) {
            setUser(userData);
          } else {
            throw new Error('Failed to load user data');
          }
        }
        
        // Fetch user visits
        const visitsData = await getUserVisits();
        console.log('Visits data:', visitsData);
        
        if (visitsData && visitsData.visits) {
          setVisits(visitsData.visits);
        } else {
          console.warn('No visits found in response');
          setVisits([]);
        }
      } catch (err) {
        console.error('Failed to load profile data:', err);
        setError('Failed to load profile data. Please try again.');
        
        // If unauthorized, redirect to login
        if (err.response && err.response.status === 401) {
          navigate('/login');
        }
      } finally {
        setLoading(false);
      }
    };
    
    fetchUserData();
  }, [navigate]);
  
  if (loading) {
    return (
      <div>
        <Navbar />
        <div className="container mx-auto p-4 flex justify-center items-center h-screen">
          <div>Loading profile data...</div>
        </div>
      </div>
    );
  }
  
  if (error) {
    return (
      <div>
        <Navbar />
        <div className="container mx-auto p-4">
          <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded">
            <p>{error}</p>
            <button 
              className="underline mt-2"
              onClick={() => window.location.reload()}
            >
              Try Again
            </button>
          </div>
        </div>
      </div>
    );
  }
  
  // Get unique countries from visits
  const countries = [...new Set(
    visits
      .filter(visit => visit.location && visit.location.country) // Only include visits with location data
      .map(visit => visit.location.country)
  )];
  
  // Get highly rated visits (4-5 stars)
  const highlyRated = visits.filter(visit => visit.rating >= 4);
  
  return (
    <div>
      <Navbar />
      <div className="container mx-auto p-4">
        <div className="bg-white shadow-md rounded-lg p-6 mb-6">
          <h2 className="text-2xl font-bold mb-4">Profile</h2>
          
          {user && (
            <div>
              <div className="mb-4">
                <p className="text-gray-600">Username</p>
                <p className="text-lg">{user.username}</p>
              </div>
              
              <div className="mb-4">
                <p className="text-gray-600">Email</p>
                <p className="text-lg">{user.email}</p>
              </div>
              
              {user.created_at && (
                <div>
                  <p className="text-gray-600">Member Since</p>
                  <p className="text-lg">
                    {new Date(user.created_at).toLocaleDateString()}
                  </p>
                </div>
              )}
            </div>
          )}
        </div>
        
        <div className="bg-white shadow-md rounded-lg p-6">
          <h2 className="text-2xl font-bold mb-4">Your Travel Stats</h2>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
            <div className="bg-blue-100 p-4 rounded-lg text-center">
              <p className="text-4xl font-bold text-blue-600">{visits.length}</p>
              <p className="text-gray-700">Places Visited</p>
            </div>
            
            <div className="bg-green-100 p-4 rounded-lg text-center">
              <p className="text-4xl font-bold text-green-600">{countries.length}</p>
              <p className="text-gray-700">Countries</p>
            </div>
            
            <div className="bg-purple-100 p-4 rounded-lg text-center">
              <p className="text-4xl font-bold text-purple-600">{highlyRated.length}</p>
              <p className="text-gray-700">Highly Rated (4-5★)</p>
            </div>
          </div>
          
          {visits.length > 0 ? (
            <div>
              <h3 className="text-xl font-bold mb-2">Recently Visited</h3>
              <ul className="divide-y divide-gray-200">
                {visits
                  .filter(visit => visit.location) // Only include visits with location data
                  .sort((a, b) => new Date(b.visit_date) - new Date(a.visit_date))
                  .slice(0, 5)
                  .map(visit => (
                    <li key={visit.id} className="py-3">
                      <div className="flex justify-between">
                        <div>
                          <p className="font-semibold">{visit.location.name}</p>
                          <p className="text-sm text-gray-600">
                            {visit.location.city}, {visit.location.country}
                          </p>
                        </div>
                        <div className="text-right">
                          <p className="text-sm text-gray-600">
                            {new Date(visit.visit_date).toLocaleDateString()}
                          </p>
                          {visit.rating && (
                            <p className="text-yellow-500">
                              {'★'.repeat(visit.rating)}
                              {'☆'.repeat(5 - visit.rating)}
                            </p>
                          )}
                        </div>
                      </div>
                    </li>
                  ))}
              </ul>
            </div>
          ) : (
            <p>You haven't visited any places yet.</p>
          )}
        </div>
      </div>
    </div>
  );
};

export default Profile;