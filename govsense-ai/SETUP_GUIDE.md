# 🚀 GovSense AI - Complete Setup Guide

## Quick Start (5 Minutes)

### Option 1: Automated Setup (Recommended)

```powershell
# Navigate to project directory
cd "d:\Balaji Galaxies\Dev Universe\Dev Star\WorkSpace\Hack2Skills\New folder (2)\govsense-ai"

# Run automated startup script
.\start-local.ps1
```

This will:
- ✅ Check prerequisites
- ✅ Set up backend virtual environment
- ✅ Install all dependencies
- ✅ Start backend server (http://localhost:8080)
- ✅ Start frontend server (http://localhost:3000)
- ✅ Open browser automatically

### Option 2: Manual Setup

#### Step 1: Backend Setup

```powershell
# Navigate to backend
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
.\venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
copy ..\.env.example .env

# Start server
python main.py
```

Backend runs on: **http://localhost:8080**

#### Step 2: Frontend Setup

```powershell
# Open new terminal
# Navigate to frontend
cd frontend

# Install dependencies
npm install

# Start development server
npm start
```

Frontend runs on: **http://localhost:3000**

---

## 📋 Prerequisites

### Required Software

1. **Python 3.11+**
   - Download: https://www.python.org/downloads/
   - Verify: `python --version`

2. **Node.js 18+**
   - Download: https://nodejs.org/
   - Verify: `node --version`

3. **Git** (optional, for version control)
   - Download: https://git-scm.com/

### Optional (for GCP deployment)

4. **Google Cloud SDK**
   - Download: https://cloud.google.com/sdk/docs/install
   - Verify: `gcloud --version`

5. **Firebase CLI** (for frontend hosting)
   - Install: `npm install -g firebase-tools`
   - Verify: `firebase --version`

---

## 🧪 Testing the Application

### 1. Generate Demo Data

Visit: http://localhost:8080/docs

Find the endpoint: **POST /api/requests/demo-data**

Click "Try it out" → Execute

This creates 20 sample service requests.

### 2. Test All Features

#### Feature 1: Predictive Dashboard
- Navigate to: http://localhost:3000/dashboard
- Select different time ranges (7, 14, 30, 60, 90 days)
- View AI-generated insights
- Check forecast charts

#### Feature 2: Service Request Submission
- Navigate to: http://localhost:3000/submit
- Fill out the form:
  - Description: "Large pothole on Main Street"
  - Location: Use default coordinates
  - Address: "Pune, Maharashtra"
- Submit and get tracking ID
- View AI categorization results

#### Feature 3: Public Transparency Portal
- Navigate to: http://localhost:3000/public
- View real-time metrics
- Check before/after comparisons
- Read impact stories
- Explore category breakdowns

### 3. Track a Request

- Navigate to: http://localhost:3000/track
- Enter a tracking ID (from submission)
- View status, timeline, and progress

---

## 🌐 Deployment to Google Cloud

### Prerequisites

1. Create Google Cloud Project
```powershell
gcloud projects create govsense-ai-mvp --name="GovSense AI MVP"
gcloud config set project govsense-ai-mvp
```

2. Enable Billing
- Visit: https://console.cloud.google.com/billing
- Link billing account to project

3. Enable Required APIs
```powershell
gcloud services enable run.googleapis.com
gcloud services enable cloudbuild.googleapis.com
gcloud services enable artifactregistry.googleapis.com
```

### Deploy Backend to Cloud Run (India Region)

```powershell
# Navigate to project root
cd "d:\Balaji Galaxies\Dev Universe\Dev Star\WorkSpace\Hack2Skills\New folder (2)\govsense-ai"

# Run deployment script
.\deploy.ps1
```

**OR manually:**

```powershell
cd backend

# Deploy to Cloud Run (Mumbai region)
gcloud run deploy govsense-api \
  --source . \
  --platform managed \
  --region asia-south1 \
  --allow-unauthenticated \
  --set-env-vars USE_MOCK_DATA=true \
  --memory 512Mi \
  --cpu 1
```

### Deploy Frontend to Firebase

```powershell
cd frontend

# Login to Firebase
firebase login

# Initialize Firebase (select Hosting)
firebase init hosting

# Configuration:
# - Public directory: build
# - Single-page app: Yes
# - Automatic builds: No

# Build production
npm run build

# Deploy
firebase deploy --only hosting
```

---

## 🔧 Configuration

### Environment Variables

#### Backend (.env)

```env
# Google Cloud
PROJECT_ID=govsense-ai-mvp
REGION=asia-south1

# API Configuration
API_HOST=0.0.0.0
API_PORT=8080
USE_MOCK_DATA=true

# Feature Flags (for local dev)
ENABLE_GEMINI=false
ENABLE_VERTEX_AI=false
ENABLE_BIGQUERY=false

# Optional: If you have Gemini API key
GEMINI_API_KEY=your-api-key-here
```

#### Frontend (.env)

```env
REACT_APP_API_URL=http://localhost:8080
```

For production:
```env
REACT_APP_API_URL=https://govsense-api-xxx.run.app
```

---

## 📊 API Documentation

### Interactive API Docs

Visit: **http://localhost:8080/docs**

### Key Endpoints

#### Predictions (Feature 1)
- `POST /api/predictions/forecast` - Get demand forecast
- `GET /api/predictions/categories` - List categories
- `GET /api/predictions/zones` - List zones
- `GET /api/predictions/accuracy` - Model accuracy metrics

#### Service Requests (Feature 2)
- `POST /api/requests/submit` - Submit new request
- `GET /api/requests/list` - List all requests
- `GET /api/requests/stats` - Request statistics
- `POST /api/requests/demo-data` - Generate demo data

#### Tracking
- `GET /api/tracking/{tracking_id}` - Track request status
- `POST /api/tracking/{tracking_id}/update` - Update status
- `POST /api/tracking/{tracking_id}/feedback` - Submit feedback

#### Public Portal (Feature 3)
- `GET /api/public/dashboard` - Public dashboard data
- `GET /api/public/metrics/current` - Current metrics
- `GET /api/public/metrics/comparison` - Before/after comparison
- `GET /api/public/open-data/requests` - Open data API
- `GET /api/public/data-catalog` - Data catalog

---

## 🐛 Troubleshooting

### Backend Issues

**Problem: Port 8080 already in use**
```powershell
# Find process using port 8080
netstat -ano | findstr :8080

# Kill the process (replace PID with actual process ID)
taskkill /PID <PID> /F
```

**Problem: Module not found**
```powershell
# Ensure virtual environment is activated
.\venv\Scripts\activate

# Reinstall dependencies
pip install -r requirements.txt
```

**Problem: Python version mismatch**
```powershell
# Check Python version
python --version

# Should be 3.11 or higher
# If not, install correct version and recreate venv
```

### Frontend Issues

**Problem: Port 3000 already in use**
```powershell
# Kill process on port 3000
netstat -ano | findstr :3000
taskkill /PID <PID> /F
```

**Problem: npm install fails**
```powershell
# Clear npm cache
npm cache clean --force

# Delete node_modules and package-lock.json
Remove-Item -Recurse -Force node_modules
Remove-Item package-lock.json

# Reinstall
npm install
```

**Problem: CORS errors**
- Ensure backend is running on port 8080
- Check proxy setting in `package.json`
- Clear browser cache

### Deployment Issues

**Problem: gcloud command not found**
- Install Google Cloud SDK
- Add to PATH: `C:\Program Files (x86)\Google\Cloud SDK\google-cloud-sdk\bin`

**Problem: Deployment fails**
```powershell
# Check project is set
gcloud config get-value project

# Check region is set
gcloud config get-value run/region

# Re-authenticate
gcloud auth login
```

---

## 📱 Testing on Mobile

### Local Network Testing

1. Find your local IP:
```powershell
ipconfig
# Look for IPv4 Address (e.g., 192.168.1.100)
```

2. Update frontend `.env`:
```env
REACT_APP_API_URL=http://192.168.1.100:8080
```

3. Access from mobile:
- Frontend: `http://192.168.1.100:3000`
- Backend: `http://192.168.1.100:8080`

---

## 🎯 Hackathon Demo Checklist

### Before Demo

- [ ] Backend running on port 8080
- [ ] Frontend running on port 3000
- [ ] Demo data generated (20+ requests)
- [ ] Browser tabs open:
  - [ ] Home page
  - [ ] Dashboard
  - [ ] Submit Request
  - [ ] Public Portal
  - [ ] API Docs
- [ ] Presentation slides ready
- [ ] Internet connection stable

### Demo Flow (10 minutes)

1. **Introduction** (1 min)
   - Show home page
   - Explain problem statement
   - Overview of 3 features

2. **Feature 1: Predictive Dashboard** (3 min)
   - Navigate to dashboard
   - Show 30-day forecast
   - Highlight AI insights
   - Explain Vertex AI integration

3. **Feature 2: Smart Prioritization** (3 min)
   - Submit a new request
   - Show AI categorization
   - Display priority score
   - Track the request

4. **Feature 3: Transparency Portal** (2 min)
   - Show public metrics
   - Before/after comparison
   - Impact stories
   - Open Data API

5. **Closing** (1 min)
   - Recap key features
   - Mention Google Cloud stack
   - Q&A

---

## 📞 Support & Resources

### Documentation
- Main README: `README.md`
- Implementation Plan: `../IMPLEMENTATION_PLAN.md`
- USPs: `../USP_LIST.md`
- MVP Details: `../MVP_PROTOTYPE.md`

### API Documentation
- Local: http://localhost:8080/docs
- Production: https://your-service-url.run.app/docs

### Logs
- Backend: Check terminal running `python main.py`
- Frontend: Check terminal running `npm start`
- Browser: Open Developer Tools (F12) → Console

### Common Commands

```powershell
# Backend
cd backend
.\venv\Scripts\activate
python main.py

# Frontend
cd frontend
npm start

# Build for production
npm run build

# Deploy to GCP
.\deploy.ps1
```

---

## ✅ Success Criteria

Your setup is successful if:

1. ✅ Backend health check returns 200: http://localhost:8080/health
2. ✅ Frontend loads without errors: http://localhost:3000
3. ✅ API docs accessible: http://localhost:8080/docs
4. ✅ Can generate demo data successfully
5. ✅ All 3 features work:
   - Predictive Dashboard shows charts
   - Can submit and track requests
   - Public portal displays metrics

---

## 🎓 Next Steps

1. **Customize**: Add your Gemini API key for real AI responses
2. **Enhance**: Connect to actual BigQuery and Vertex AI
3. **Deploy**: Push to Google Cloud for live demo
4. **Present**: Use this working prototype for hackathon
5. **Win**: Showcase the complete solution! 🏆

---

**Good luck with your hackathon! 🚀**
