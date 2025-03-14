# Travel Tracker Web Application

A full-stack web application for tracking your travels, discovering new destinations, and getting personalized recommendations.

## Features

- User authentication (login/signup)
- Interactive map with location markers
- Track visited locations
- Add personal ratings and notes to visited places
- View general and personalized location recommendations with toggle option
- User profile with travel statistics
- Demo user (nightlife enthusiast) with pre-populated data

## Tech Stack

### Backend
- Python with Flask
- SQLAlchemy ORM
- SQLite database
- JWT authentication

### Frontend
- React
- React Router
- Leaflet for interactive maps
- Custom CSS for styling (no Tailwind)

### Infrastructure
- Docker & Docker Compose for containerization

## Project Structure

The project follows a standard structure with separate frontend and backend directories:

- `backend/`: Flask API server
- `frontend/`: React frontend application
- `docker-compose.yml`: Docker Compose configuration

## Getting Started

### Prerequisites

- Docker and Docker Compose installed on your machine
- Git for cloning the repository

### Installation & Setup

1. Clone the repository:

```bash
git clone 
cd travel-tracker
```

2. Start the application with Docker Compose:

```bash
docker-compose up -d
```

This will build and start both the frontend and backend services. The application will be accessible at:
- Frontend: http://localhost
- Backend API: http://localhost:8000/api

### Demo User

You can log in with the following demo credentials:
- Username: `demouser`
- Password: `password123`

This demo user is a nightlife enthusiast who has visited many nightlife locations with high ratings.

### Development

For development purposes, you can run the frontend and backend separately:

#### Backend

```bash
cd backend
pip install -r requirements.txt
python app.py
```

The API will be available at http://localhost:8000.

#### Frontend

```bash
cd frontend
npm install
npm start
```

The development server will start at http://localhost:80.

## API Documentation

The backend provides the following API endpoints:

### Authentication

- `POST /api/auth/register`: Register a new user
- `POST /api/auth/login`: Login a user
- `GET /api/auth/profile`: Get user profile

### Locations

- `GET /api/locations`: Get all locations
- `GET /api/locations/:id`: Get a specific location
- `GET /api/locations/search`: Search locations

### Visits

- `GET /api/visits`: Get user's visited locations
- `POST /api/visits`: Add a location to visited
- `DELETE /api/visits/:id`: Remove a location from visited

### Recommendations

- `GET /api/recommendations`: Get general recommendations
- `GET /api/recommendations/personalized`: Get personalized recommendations

## Database Schema

The application uses the following main data models:

- **User**: User account information
- **Location**: Information about travel destinations (nature, recreational, nightlife, culture, food)
- **Visit**: Tracks which users have visited which locations