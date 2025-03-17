# ChillQuest Web Application

A full-stack web application for discovering exciting destinations and getting personalized recommendations.

## Features

- User authentication (login/signup)
- Interactive map with location markers
- Track visited locations
- Add personal ratings and notes to visited places
- View general and personalized location recommendations with toggle option
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
cd chillquest