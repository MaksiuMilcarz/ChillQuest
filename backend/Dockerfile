# Backend Dockerfile
FROM python:3.9-slim

WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install curl for healthchecks
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Create instance directory
RUN mkdir -p /app/instance && chmod 777 /app/instance

# Copy the application code
COPY . .

EXPOSE 8000

# Default command (will be overridden by docker-compose)
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "app:create_app()"]