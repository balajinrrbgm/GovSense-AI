FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Set environment variables
ENV PORT=8080
ENV API_HOST=0.0.0.0
ENV API_PORT=8080
ENV USE_MOCK_DATA=true
ENV ENABLE_GEMINI=true
ENV ENABLE_VERTEX_AI=false
ENV ENABLE_BIGQUERY=false
ENV PROJECT_ID=govsense-ai-mvp
ENV REGION=asia-south1
ENV CORS_ORIGINS=*
ENV API_RELOAD=false

# Expose port
EXPOSE 8080

# Run the application
CMD exec uvicorn main:app --host 0.0.0.0 --port ${PORT:-8080}
