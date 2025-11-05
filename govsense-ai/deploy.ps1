# GovSense AI - Deployment Script for Windows PowerShell
# Deploys to Google Cloud Platform (India Region)

Write-Host "🚀 GovSense AI Deployment Script" -ForegroundColor Cyan
Write-Host "=================================" -ForegroundColor Cyan
Write-Host ""

# Configuration
$PROJECT_ID = "govsense-ai-mvp"
$REGION = "asia-south1"
$SERVICE_NAME = "govsense-api"

# Check if gcloud is installed
Write-Host "📋 Checking prerequisites..." -ForegroundColor Yellow
try {
    $gcloudVersion = gcloud version 2>&1
    Write-Host "✅ Google Cloud SDK found" -ForegroundColor Green
} catch {
    Write-Host "❌ Google Cloud SDK not found. Please install from: https://cloud.google.com/sdk" -ForegroundColor Red
    exit 1
}

# Set project and region
Write-Host ""
Write-Host "🔧 Configuring Google Cloud..." -ForegroundColor Yellow
gcloud config set project $PROJECT_ID
gcloud config set run/region $REGION

# Enable required APIs
Write-Host ""
Write-Host "🔌 Enabling required APIs..." -ForegroundColor Yellow
gcloud services enable run.googleapis.com
gcloud services enable cloudbuild.googleapis.com
gcloud services enable artifactregistry.googleapis.com

# Deploy Backend to Cloud Run
Write-Host ""
Write-Host "📦 Deploying Backend to Cloud Run..." -ForegroundColor Yellow
Set-Location backend

# Create Dockerfile if not exists
if (-not (Test-Path "Dockerfile")) {
    Write-Host "📝 Creating Dockerfile..." -ForegroundColor Yellow
    @"
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PORT=8080
ENV API_HOST=0.0.0.0
ENV API_PORT=8080
ENV USE_MOCK_DATA=true

CMD ["python", "main.py"]
"@ | Out-File -FilePath "Dockerfile" -Encoding UTF8
}

# Deploy to Cloud Run
Write-Host "🚢 Deploying to Cloud Run (asia-south1)..." -ForegroundColor Yellow
gcloud run deploy $SERVICE_NAME `
    --source . `
    --platform managed `
    --region $REGION `
    --allow-unauthenticated `
    --set-env-vars "USE_MOCK_DATA=true,ENABLE_GEMINI=false,ENABLE_VERTEX_AI=false,ENABLE_BIGQUERY=false" `
    --memory 512Mi `
    --cpu 1 `
    --timeout 300 `
    --max-instances 10

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Backend deployed successfully!" -ForegroundColor Green
    
    # Get service URL
    $SERVICE_URL = gcloud run services describe $SERVICE_NAME --region $REGION --format="value(status.url)"
    Write-Host ""
    Write-Host "🌐 Backend URL: $SERVICE_URL" -ForegroundColor Cyan
    Write-Host "📚 API Docs: $SERVICE_URL/docs" -ForegroundColor Cyan
} else {
    Write-Host "❌ Backend deployment failed" -ForegroundColor Red
    exit 1
}

# Return to root directory
Set-Location ..

# Build Frontend
Write-Host ""
Write-Host "🎨 Building Frontend..." -ForegroundColor Yellow
Set-Location frontend

# Update API URL in environment
$envContent = "REACT_APP_API_URL=$SERVICE_URL"
$envContent | Out-File -FilePath ".env.production" -Encoding UTF8

# Install dependencies and build
npm install
npm run build

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Frontend built successfully!" -ForegroundColor Green
} else {
    Write-Host "❌ Frontend build failed" -ForegroundColor Red
    exit 1
}

# Deploy Frontend to Firebase (optional)
Write-Host ""
Write-Host "🔥 Firebase Deployment (Optional)" -ForegroundColor Yellow
Write-Host "To deploy frontend to Firebase Hosting:" -ForegroundColor White
Write-Host "  1. Install Firebase CLI: npm install -g firebase-tools" -ForegroundColor White
Write-Host "  2. Login: firebase login" -ForegroundColor White
Write-Host "  3. Initialize: firebase init hosting" -ForegroundColor White
Write-Host "  4. Deploy: firebase deploy --only hosting" -ForegroundColor White

# Return to root
Set-Location ..

# Summary
Write-Host ""
Write-Host "=================================" -ForegroundColor Cyan
Write-Host "✅ Deployment Complete!" -ForegroundColor Green
Write-Host "=================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "📊 Deployment Summary:" -ForegroundColor Yellow
Write-Host "  Project ID: $PROJECT_ID" -ForegroundColor White
Write-Host "  Region: $REGION (Mumbai, India)" -ForegroundColor White
Write-Host "  Backend URL: $SERVICE_URL" -ForegroundColor White
Write-Host "  API Docs: $SERVICE_URL/docs" -ForegroundColor White
Write-Host ""
Write-Host "🧪 Test your deployment:" -ForegroundColor Yellow
Write-Host "  curl $SERVICE_URL/health" -ForegroundColor White
Write-Host ""
Write-Host "📝 Next Steps:" -ForegroundColor Yellow
Write-Host "  1. Test API endpoints at $SERVICE_URL/docs" -ForegroundColor White
Write-Host "  2. Generate demo data using /api/requests/demo-data" -ForegroundColor White
Write-Host "  3. Deploy frontend to Firebase Hosting" -ForegroundColor White
Write-Host "  4. Configure custom domain (optional)" -ForegroundColor White
Write-Host ""
