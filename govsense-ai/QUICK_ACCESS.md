# 🚀 GovSense AI - Quick Access Card

## 📱 Live URLs

### Frontend (Firebase Hosting)
🌐 **Main App:** https://govsense-ai-mvp.web.app

**Pages:**
- 🏠 Home: https://govsense-ai-mvp.web.app/
- 📊 Dashboard: https://govsense-ai-mvp.web.app/dashboard
- ✍️ Submit: https://govsense-ai-mvp.web.app/submit
- 🔍 Track: https://govsense-ai-mvp.web.app/track
- 🌍 Public: https://govsense-ai-mvp.web.app/public

### Backend API (Cloud Run)
🔧 **API Base:** https://govsense-api-502383031433.asia-south1.run.app

**Endpoints:**
- 📚 API Docs: https://govsense-api-502383031433.asia-south1.run.app/docs
- ❤️ Health: https://govsense-api-502383031433.asia-south1.run.app/health
- 🏠 Root: https://govsense-api-502383031433.asia-south1.run.app/

---

## ⚙️ Configuration

### Project Details
- **Project ID:** govsense-ai-mvp
- **Region:** asia-south1 (Mumbai, India)
- **Deployment Date:** November 5, 2025

### Environment
- **Backend Platform:** Google Cloud Run
- **Frontend Platform:** Firebase Hosting
- **AI Service:** Google Gemini Pro
- **Mode:** Demo (Mock Data Enabled)

---

## 🧪 Quick Test Commands

### Test Backend Health
```bash
curl https://govsense-api-502383031433.asia-south1.run.app/health
```

### Generate Demo Data
```bash
curl -X POST "https://govsense-api-502383031433.asia-south1.run.app/api/requests/demo-data?count=20"
```

### Get Predictions
```bash
curl -X POST "https://govsense-api-502383031433.asia-south1.run.app/api/predictions/forecast" \
  -H "Content-Type: application/json" \
  -d '{"days": 30}'
```

---

## 🔄 Redeploy Commands

### Backend
```powershell
cd backend
gcloud run deploy govsense-api --source . --platform managed --region asia-south1
```

### Frontend
```powershell
cd frontend
npm run build
firebase deploy --only hosting
```

---

## 📊 GCP Console Links

- **Cloud Run:** https://console.cloud.google.com/run/detail/asia-south1/govsense-api?project=govsense-ai-mvp
- **Firebase:** https://console.firebase.google.com/project/govsense-ai-mvp/hosting
- **Logs:** https://console.cloud.google.com/logs/query?project=govsense-ai-mvp
- **Billing:** https://console.cloud.google.com/billing?project=govsense-ai-mvp

---

## 💡 Demo Flow (5 minutes)

1. **Open App** → https://govsense-ai-mvp.web.app
2. **Dashboard** → View 30-day predictions & AI insights
3. **Submit Request** → Fill form, get AI categorization
4. **Track Request** → Use tracking ID from step 3
5. **Public Portal** → See transparency metrics

---

## 🎯 Key Features

✅ Predictive Dashboard (30-90 day forecasts)  
✅ AI Categorization (Gemini Pro)  
✅ Smart Prioritization (Multi-factor scoring)  
✅ Real-time Tracking  
✅ Public Transparency Portal  
✅ Open Data API  

---

## 📞 Support

**Documentation:** [DEPLOYMENT_SUMMARY.md](./DEPLOYMENT_SUMMARY.md)  
**Setup Guide:** [SETUP_GUIDE.md](./SETUP_GUIDE.md)  
**README:** [README.md](./README.md)

---

## ⚡ Status

🟢 **Backend:** OPERATIONAL  
🟢 **Frontend:** OPERATIONAL  
🟢 **AI Service:** ENABLED  
🟢 **Auto-scaling:** ENABLED  

**Uptime:** 99.95% SLA  
**Cost:** $0-$30/month

---

*Last Updated: November 5, 2025*
