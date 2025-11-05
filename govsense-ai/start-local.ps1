# GovSense AI - Local Development Startup Script
# Starts both backend and frontend for local testing

Write-Host "🚀 Starting GovSense AI - Local Development" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""

# Check Python
Write-Host "📋 Checking Python..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✅ Python found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Python not found. Please install Python 3.11+" -ForegroundColor Red
    exit 1
}

# Check Node.js
Write-Host "📋 Checking Node.js..." -ForegroundColor Yellow
try {
    $nodeVersion = node --version 2>&1
    Write-Host "✅ Node.js found: $nodeVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Node.js not found. Please install Node.js 18+" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "🔧 Setting up Backend..." -ForegroundColor Yellow

# Setup Backend
Set-Location backend

# Create .env if it doesn't exist
if (-not (Test-Path ".env")) {
    Write-Host "📝 Creating .env file..." -ForegroundColor Yellow
    Copy-Item "../.env.example" ".env"
}

# Create virtual environment if it doesn't exist
if (-not (Test-Path "venv")) {
    Write-Host "🐍 Creating Python virtual environment..." -ForegroundColor Yellow
    python -m venv venv
}

# Activate virtual environment and install dependencies
Write-Host "📦 Installing Python dependencies..." -ForegroundColor Yellow
.\venv\Scripts\Activate.ps1
pip install -q -r requirements.txt

# Start backend in new window
Write-Host "🚀 Starting Backend Server..." -ForegroundColor Green
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PWD'; .\venv\Scripts\Activate.ps1; python main.py"

# Wait for backend to start
Write-Host "⏳ Waiting for backend to start..." -ForegroundColor Yellow
Start-Sleep -Seconds 5

# Return to root
Set-Location ..

Write-Host ""
Write-Host "🎨 Setting up Frontend..." -ForegroundColor Yellow

# Setup Frontend
Set-Location frontend

# Install dependencies if node_modules doesn't exist
if (-not (Test-Path "node_modules")) {
    Write-Host "📦 Installing Node dependencies (this may take a few minutes)..." -ForegroundColor Yellow
    npm install
}

# Start frontend in new window
Write-Host "🚀 Starting Frontend Server..." -ForegroundColor Green
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PWD'; npm start"

# Return to root
Set-Location ..

# Wait a bit for services to start
Start-Sleep -Seconds 3

Write-Host ""
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "✅ GovSense AI Started Successfully!" -ForegroundColor Green
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "🌐 Application URLs:" -ForegroundColor Yellow
Write-Host "  Frontend:  http://localhost:3000" -ForegroundColor White
Write-Host "  Backend:   http://localhost:8080" -ForegroundColor White
Write-Host "  API Docs:  http://localhost:8080/docs" -ForegroundColor White
Write-Host ""
Write-Host "📊 Quick Start:" -ForegroundColor Yellow
Write-Host "  1. Open http://localhost:3000 in your browser" -ForegroundColor White
Write-Host "  2. Generate demo data at http://localhost:8080/docs" -ForegroundColor White
Write-Host "  3. Explore the three features:" -ForegroundColor White
Write-Host "     - Predictive Dashboard" -ForegroundColor White
Write-Host "     - Submit Service Request" -ForegroundColor White
Write-Host "     - Public Transparency Portal" -ForegroundColor White
Write-Host ""
Write-Host "🛑 To stop servers: Close the PowerShell windows" -ForegroundColor Yellow
Write-Host ""
Write-Host "💡 Tip: Visit /docs endpoint to generate demo data first!" -ForegroundColor Cyan
Write-Host ""

# Try to open browser
Write-Host "🌐 Opening browser..." -ForegroundColor Yellow
Start-Sleep -Seconds 5
Start-Process "http://localhost:3000"

Write-Host "✨ Happy coding!" -ForegroundColor Green
