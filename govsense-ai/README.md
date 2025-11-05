# GovSense AI - MVP Implementation

AI-Powered Governance Platform for Maharashtra - Hackathon Submission

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Node.js 18+
- Google Cloud Account (for deployment)

### Local Development Setup

#### 1. Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Copy environment file
copy .env.example .env

# Run backend server
python main.py
```

Backend will run on: http://localhost:8080

#### 2. Frontend Setup

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Start development server
npm start
```

Frontend will run on: http://localhost:3000

### 3. Access the Application

- **Home Page**: http://localhost:3000
- **Predictive Dashboard**: http://localhost:3000/dashboard
- **Submit Request**: http://localhost:3000/submit
- **Public Portal**: http://localhost:3000/public
- **API Docs**: http://localhost:8080/docs

## 📋 Features

### Feature 1: Predictive Service Demand Dashboard
- 30-day demand forecasting using AI
- Interactive visualizations
- AI-generated insights
- Category and zone filtering

### Feature 2: Smart Service Request Prioritization
- AI categorization (Gemini Pro)
- Multi-factor priority scoring
- Intelligent routing
- Real-time tracking

### Feature 3: Public Transparency Portal
- Real-time performance metrics
- Before/after comparisons
- Open Data API
- AI-generated impact stories

## 🧪 Testing

### Generate Demo Data

```bash
# Using curl
curl -X POST "http://localhost:8080/api/requests/demo-data?count=20"

# Or visit API docs
http://localhost:8080/docs
```

### Test API Endpoints

```bash
# Health check
curl http://localhost:8080/health

# Get predictions
curl -X POST "http://localhost:8080/api/predictions/forecast" \
  -H "Content-Type: application/json" \
  -d '{"days": 30}'

# Get public dashboard
curl http://localhost:8080/api/public/dashboard
```

## 🌐 Deployment to Google Cloud (India Region)

### Prerequisites
- Google Cloud SDK installed
- Project created in GCP
- Billing enabled

### Deploy Backend to Cloud Run

```bash
# Set project
gcloud config set project govsense-ai-mvp

# Set region to India
gcloud config set run/region asia-south1

# Build and deploy
cd backend
gcloud run deploy govsense-api \
  --source . \
  --platform managed \
  --region asia-south1 \
  --allow-unauthenticated \
  --set-env-vars USE_MOCK_DATA=true
```

### Deploy Frontend to Firebase

```bash
# Install Firebase CLI
npm install -g firebase-tools

# Login to Firebase
firebase login

# Initialize Firebase
cd frontend
firebase init hosting

# Build production
npm run build

# Deploy
firebase deploy --only hosting
```

## 🔧 Configuration

### Environment Variables

Backend (.env):
```
PROJECT_ID=govsense-ai-mvp
REGION=asia-south1
GEMINI_API_KEY=your-api-key
USE_MOCK_DATA=true
```

Frontend (.env):
```
REACT_APP_API_URL=http://localhost:8080
```

## 📊 Architecture

```
Frontend (React) → Backend (FastAPI) → AI Services
                                      ├─ Gemini Pro
                                      ├─ Vertex AI (optional)
                                      └─ BigQuery (optional)
```

## 🎯 Hackathon Demo Flow

1. **Start Backend**: `python main.py`
2. **Start Frontend**: `npm start`
3. **Generate Demo Data**: Visit `/docs` and execute demo-data endpoint
4. **Show Feature 1**: Navigate to Dashboard
5. **Show Feature 2**: Submit a request
6. **Show Feature 3**: View Public Portal

## 📝 API Documentation

Interactive API docs available at: http://localhost:8080/docs

## 🏆 Winning Features

- ✅ Complete 3-feature MVP
- ✅ Google Cloud tech stack (Gemini Pro ready)
- ✅ Production-ready architecture
- ✅ Beautiful UI with TailwindCSS
- ✅ Real-time updates
- ✅ Comprehensive documentation

## 🐛 Troubleshooting

### Backend won't start
- Check Python version: `python --version` (should be 3.11+)
- Ensure virtual environment is activated
- Check port 8080 is not in use

### Frontend won't start
- Check Node version: `node --version` (should be 18+)
- Delete node_modules and reinstall: `rm -rf node_modules && npm install`
- Check port 3000 is not in use

### CORS errors
- Ensure backend is running
- Check proxy setting in frontend/package.json

## 📞 Support

For issues or questions:
- Check API docs: http://localhost:8080/docs
- Review logs in terminal
- Check browser console for frontend errors

## 🎓 Tech Stack

- **Backend**: FastAPI, Python 3.11
- **Frontend**: React 18, TailwindCSS
- **AI**: Gemini Pro (Google AI)
- **Deployment**: Cloud Run, Firebase Hosting
- **Region**: asia-south1 (Mumbai, India)

## 📄 License

Developed for GenAI Exchange Hackathon 2024

---

**Built with ❤️ for better governance**
