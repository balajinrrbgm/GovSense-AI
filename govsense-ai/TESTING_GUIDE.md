# 🧪 GovSense AI - Testing Guide

## Pre-Testing Checklist

### 1. Install Prerequisites

#### Python 3.11+
```powershell
# Download from: https://www.python.org/downloads/
# During installation, CHECK "Add Python to PATH"

# Verify installation
python --version
# Should show: Python 3.11.x or higher
```

#### Node.js 18+
```powershell
# Download from: https://nodejs.org/
# Install LTS version

# Verify installation
node --version
npm --version
```

---

## Local Testing Steps

### Step 1: Start Backend

```powershell
# Navigate to backend directory
cd "d:\Balaji Galaxies\Dev Universe\Dev Star\WorkSpace\Hack2Skills\New folder (2)\govsense-ai\backend"

# Create virtual environment
python -m venv venv

# Activate virtual environment
.\venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt

# Create .env file from example
Copy-Item ..\.env.example .env

# Start backend server
python main.py
```

**Expected Output:**
```
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8080
```

**Test Backend:**
- Open browser: http://localhost:8080
- Should see: `{"status": "healthy", "service": "GovSense AI API", ...}`

### Step 2: Start Frontend

**Open a NEW PowerShell window:**

```powershell
# Navigate to frontend directory
cd "d:\Balaji Galaxies\Dev Universe\Dev Star\WorkSpace\Hack2Skills\New folder (2)\govsense-ai\frontend"

# Install dependencies (first time only)
npm install

# Start development server
npm start
```

**Expected Output:**
```
Compiled successfully!

You can now view govsense-ai-frontend in the browser.

  Local:            http://localhost:3000
  On Your Network:  http://192.168.x.x:3000
```

**Test Frontend:**
- Browser should auto-open to http://localhost:3000
- Should see GovSense AI home page

---

## Feature Testing

### Feature 1: Predictive Service Demand Dashboard

#### Test Steps:
1. Navigate to http://localhost:3000/dashboard
2. Select "30 Days" from dropdown
3. Wait for data to load

#### Expected Results:
- ✅ Chart displays with forecast line
- ✅ AI-generated insights appear in blue box
- ✅ Summary cards show:
  - Total Predicted Requests
  - Average Daily Demand
  - Model Confidence %
- ✅ No console errors

#### Test Different Time Ranges:
- 7 days
- 14 days
- 30 days
- 60 days
- 90 days

Each should show different forecast data.

---

### Feature 2: Smart Service Request Prioritization

#### Test Steps:

**A. Submit Request**
1. Navigate to http://localhost:3000/submit
2. Fill form:
   - **Description**: "Large pothole on Main Street causing traffic issues"
   - **Latitude**: 18.5204 (default)
   - **Longitude**: 73.8567 (default)
   - **Address**: "Pune, Maharashtra"
3. Click "Submit Request"

#### Expected Results:
- ✅ Form submits successfully
- ✅ Redirects to tracking page
- ✅ Shows tracking ID (format: TRK-XXXXXXXXXXXX)
- ✅ Displays:
  - Category (e.g., "Infrastructure")
  - Priority Score (0-100)
  - Estimated Resolution Time
  - Assigned Department

**B. List Requests**
1. Open API docs: http://localhost:8080/docs
2. Find: GET /api/requests/list
3. Click "Try it out" → Execute

#### Expected Results:
- ✅ Returns array of requests
- ✅ Each request has:
  - request_id
  - tracking_id
  - category
  - priority_score
  - status

**C. Generate Demo Data**
1. Open API docs: http://localhost:8080/docs
2. Find: POST /api/requests/demo-data
3. Click "Try it out"
4. Set count: 20
5. Execute

#### Expected Results:
- ✅ Response: `{"message": "Created 20 demo requests", "tracking_ids": [...]}`
- ✅ Returns 20 tracking IDs

---

### Feature 3: Public Transparency & Impact Dashboard

#### Test Steps:
1. Navigate to http://localhost:3000/public
2. Scroll through entire page

#### Expected Results:
- ✅ **Key Metrics Cards** display:
  - Completion Rate (%)
  - Avg Response Time (hours)
  - Citizen Satisfaction (x/5)
  - Requests This Month
- ✅ **Before/After Comparison** shows:
  - Traditional vs AI metrics
  - Improvement percentages
- ✅ **Charts Display**:
  - Pie chart: Requests by Category
  - Bar chart: Performance by Category
- ✅ **Impact Stories** section shows AI-generated stories
- ✅ **Open Data API** link present

---

## API Testing

### Using API Documentation

1. Open: http://localhost:8080/docs
2. Interactive Swagger UI should load

### Test Each Endpoint:

#### Health Check
```
GET /health
Expected: {"status": "healthy", ...}
```

#### Predictions
```
POST /api/predictions/forecast
Body: {"days": 30}
Expected: {"predictions": [...], "insights": "..."}
```

#### Submit Request
```
POST /api/requests/submit
Body: {
  "description": "Test request",
  "location_lat": 18.5204,
  "location_lng": 73.8567,
  "location_address": "Test Address"
}
Expected: {"request_id": "...", "tracking_id": "TRK-...", ...}
```

#### Track Request
```
GET /api/tracking/{tracking_id}
Expected: {"tracking_id": "...", "status": "...", "timeline": [...]}
```

#### Public Dashboard
```
GET /api/public/dashboard
Expected: {"overview": {...}, "performance_trends": [...], ...}
```

---

## Integration Testing

### End-to-End Flow Test

1. **Generate Demo Data**
   - Visit: http://localhost:8080/docs
   - Execute: POST /api/requests/demo-data?count=20
   - Verify: 20 tracking IDs returned

2. **View Dashboard**
   - Navigate: http://localhost:3000/dashboard
   - Verify: Charts display data
   - Verify: AI insights appear

3. **Submit New Request**
   - Navigate: http://localhost:3000/submit
   - Fill form with test data
   - Submit
   - Verify: Redirects to tracking page

4. **Track Request**
   - Use tracking ID from step 3
   - Navigate: http://localhost:3000/track
   - Enter tracking ID
   - Verify: Status and timeline display

5. **View Public Portal**
   - Navigate: http://localhost:3000/public
   - Verify: All metrics display
   - Verify: Charts render correctly

---

## Performance Testing

### Load Test (Optional)

```powershell
# Install Apache Bench (if available)
# Test API endpoint
ab -n 100 -c 10 http://localhost:8080/health

# Expected: All requests should succeed
```

### Browser Performance

1. Open DevTools (F12)
2. Go to Performance tab
3. Record page load
4. Check:
   - ✅ Page loads in < 3 seconds
   - ✅ No memory leaks
   - ✅ Smooth animations

---

## Error Testing

### Test Error Handling

1. **Invalid Tracking ID**
   - Navigate: http://localhost:3000/track
   - Enter: "INVALID-ID"
   - Expected: Error message displays

2. **Empty Form Submission**
   - Navigate: http://localhost:3000/submit
   - Click submit without filling
   - Expected: Validation errors

3. **Backend Offline**
   - Stop backend server
   - Try to load dashboard
   - Expected: Error message displays

---

## Browser Compatibility

Test in multiple browsers:
- ✅ Chrome (latest)
- ✅ Firefox (latest)
- ✅ Edge (latest)
- ✅ Safari (if available)

---

## Mobile Testing

### Responsive Design Test

1. Open DevTools (F12)
2. Toggle device toolbar (Ctrl+Shift+M)
3. Test different screen sizes:
   - Mobile: 375x667 (iPhone SE)
   - Tablet: 768x1024 (iPad)
   - Desktop: 1920x1080

#### Expected Results:
- ✅ Layout adjusts properly
- ✅ All buttons clickable
- ✅ Text readable
- ✅ Charts responsive

---

## Common Issues & Solutions

### Issue: Backend won't start

**Error**: `ModuleNotFoundError: No module named 'fastapi'`

**Solution**:
```powershell
# Ensure venv is activated
.\venv\Scripts\Activate.ps1

# Reinstall dependencies
pip install -r requirements.txt
```

### Issue: Frontend won't start

**Error**: `Cannot find module 'react'`

**Solution**:
```powershell
# Delete node_modules
Remove-Item -Recurse -Force node_modules

# Reinstall
npm install
```

### Issue: CORS errors

**Error**: `Access to fetch at 'http://localhost:8080' blocked by CORS`

**Solution**:
1. Ensure backend is running
2. Check proxy in `frontend/package.json`:
   ```json
   "proxy": "http://localhost:8080"
   ```
3. Restart frontend

### Issue: Port already in use

**Error**: `Address already in use`

**Solution**:
```powershell
# Find process on port 8080
netstat -ano | findstr :8080

# Kill process (replace PID)
taskkill /PID <PID> /F
```

---

## Test Results Checklist

### Backend Tests
- [ ] Health endpoint returns 200
- [ ] API docs accessible at /docs
- [ ] All prediction endpoints work
- [ ] Request submission works
- [ ] Tracking works
- [ ] Public dashboard works
- [ ] Demo data generation works

### Frontend Tests
- [ ] Home page loads
- [ ] Dashboard displays charts
- [ ] Can submit requests
- [ ] Can track requests
- [ ] Public portal displays
- [ ] Navigation works
- [ ] Responsive on mobile

### Integration Tests
- [ ] End-to-end flow works
- [ ] Data persists correctly
- [ ] AI insights generate
- [ ] Charts update dynamically

### Performance Tests
- [ ] Page load < 3 seconds
- [ ] API response < 1 second
- [ ] No console errors
- [ ] No memory leaks

---

## Success Criteria

Your MVP is ready for hackathon if:

1. ✅ All 3 features work independently
2. ✅ End-to-end flow completes successfully
3. ✅ No critical errors in console
4. ✅ Responsive on desktop and mobile
5. ✅ Demo data generates correctly
6. ✅ API documentation accessible
7. ✅ Performance is acceptable
8. ✅ UI is polished and professional

---

## Next Steps After Testing

1. **Document Issues**: Note any bugs found
2. **Fix Critical Bugs**: Address showstoppers
3. **Optimize Performance**: If needed
4. **Prepare Demo**: Practice presentation
5. **Deploy to GCP**: Use `deploy.ps1`
6. **Final Testing**: Test deployed version

---

## Support

If you encounter issues:
1. Check logs in terminal
2. Check browser console (F12)
3. Review SETUP_GUIDE.md
4. Check API docs at /docs

---

**Happy Testing! 🧪**
