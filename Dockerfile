# ==============================================================================
# AutoMileage AI - Multi-Stage Dockerfile for Render Deployment
# ==============================================================================

# Stage 1: Build React Frontend
FROM node:20-alpine AS frontend-builder
WORKDIR /app/frontend

COPY frontend/package*.json ./
RUN npm ci

COPY frontend/ ./
RUN npm run build

# Stage 2: Python Backend with Trained ML Model
FROM python:3.12-slim
WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=8000

# Install minimal curl for health checks
RUN apt-get update && apt-get install -y --no-install-recommends curl && rm -rf /var/lib/apt/lists/*

# Install Python ML dependencies
COPY backend/requirements.txt ./backend/
RUN pip install --no-cache-dir -r backend/requirements.txt

# Copy backend code
COPY backend/ ./backend/

# Copy compiled React frontend from builder stage
COPY --from=frontend-builder /app/frontend/dist ./frontend/dist

# Download real EPA dataset and train Random Forest during build
RUN python backend/download_data.py && python backend/train_model.py

# Expose default port
EXPOSE 8000

# Start server binding to Render's dynamic PORT
CMD ["sh", "-c", "uvicorn backend.main:app --host 0.0.0.0 --port ${PORT:-8000}"]
