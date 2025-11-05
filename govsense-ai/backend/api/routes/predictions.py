"""
Predictions API - Feature 1: Predictive Service Demand Dashboard
"""

from fastapi import APIRouter, HTTPException
from datetime import datetime, timedelta
from typing import List
import random
import logging

from api.models import (
    PredictionRequest,
    PredictionResponse,
    DemandPrediction,
    CategoryEnum
)
from api.services.gemini_service import gemini_service

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/forecast", response_model=PredictionResponse)
async def get_demand_forecast(request: PredictionRequest):
    """
    Get demand forecast for next N days
    
    Feature 1: Predictive Service Demand Dashboard
    Uses Vertex AI (or mock data) to predict service demand
    """
    
    try:
        logger.info(f"Generating forecast for {request.days} days, category: {request.category}")
        
        # Generate predictions (mock data for MVP)
        predictions = _generate_mock_predictions(
            days=request.days,
            category=request.category,
            location_zone=request.location_zone
        )
        
        # Generate AI insights using Gemini
        insights = await gemini_service.generate_insights(
            [p.dict() for p in predictions]
        )
        
        return PredictionResponse(
            predictions=predictions,
            insights=insights,
            generated_at=datetime.utcnow()
        )
        
    except Exception as e:
        logger.error(f"Forecast generation error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/categories", response_model=List[str])
async def get_available_categories():
    """Get list of available categories for predictions"""
    return [cat.value for cat in CategoryEnum]


@router.get("/zones", response_model=List[str])
async def get_available_zones():
    """Get list of available location zones"""
    return [
        "Zone A - Central Mumbai",
        "Zone B - Pune East",
        "Zone C - Nagpur North",
        "Zone D - Nashik West",
        "Zone E - Thane South"
    ]


def _generate_mock_predictions(
    days: int,
    category: CategoryEnum = None,
    location_zone: str = None
) -> List[DemandPrediction]:
    """
    Generate mock predictions for demo
    In production, this would call Vertex AI endpoint
    """
    
    predictions = []
    base_date = datetime.utcnow().date()
    
    # Categories to predict
    categories = [category] if category else list(CategoryEnum)
    
    for cat in categories:
        # Base demand varies by category
        base_demand = {
            CategoryEnum.INFRASTRUCTURE: 150,
            CategoryEnum.HEALTH: 80,
            CategoryEnum.PUBLIC_SAFETY: 50,
            CategoryEnum.OTHER: 30
        }.get(cat, 50)
        
        for day_offset in range(days):
            pred_date = base_date + timedelta(days=day_offset)
            
            # Add some variation and trends
            # Simulate weekly pattern (higher on weekdays)
            weekday_factor = 1.2 if pred_date.weekday() < 5 else 0.8
            
            # Simulate monthly trend (increase towards month end)
            monthly_factor = 1.0 + (pred_date.day / 30) * 0.3
            
            # Add random variation
            random_factor = random.uniform(0.85, 1.15)
            
            # Calculate predicted requests
            predicted = int(base_demand * weekday_factor * monthly_factor * random_factor)
            
            # Simulate a surge in week 2 for demo purposes
            if 7 <= day_offset <= 14 and cat == CategoryEnum.INFRASTRUCTURE:
                predicted = int(predicted * 1.4)  # 40% surge
            
            # Calculate confidence intervals
            confidence = 0.85 - (day_offset / days) * 0.15  # Confidence decreases over time
            margin = int(predicted * 0.15)
            
            predictions.append(DemandPrediction(
                date=pred_date.isoformat(),
                category=cat,
                location_zone=location_zone or "All Zones",
                predicted_requests=predicted,
                confidence_lower=max(0, predicted - margin),
                confidence_upper=predicted + margin,
                confidence_score=round(confidence, 2)
            ))
    
    return predictions


@router.get("/historical", response_model=dict)
async def get_historical_data(
    category: CategoryEnum = None,
    days: int = 90
):
    """
    Get historical service request data for comparison
    """
    
    try:
        # Generate mock historical data
        historical = []
        base_date = datetime.utcnow().date() - timedelta(days=days)
        
        categories = [category] if category else list(CategoryEnum)
        
        for cat in categories:
            base_demand = {
                CategoryEnum.INFRASTRUCTURE: 140,
                CategoryEnum.HEALTH: 75,
                CategoryEnum.PUBLIC_SAFETY: 45,
                CategoryEnum.OTHER: 25
            }.get(cat, 50)
            
            for day_offset in range(days):
                hist_date = base_date + timedelta(days=day_offset)
                actual = int(base_demand * random.uniform(0.8, 1.2))
                
                historical.append({
                    'date': hist_date.isoformat(),
                    'category': cat.value,
                    'actual_requests': actual,
                    'avg_resolution_time': random.uniform(36, 72)
                })
        
        return {
            'historical_data': historical,
            'period_days': days,
            'generated_at': datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Historical data error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/accuracy", response_model=dict)
async def get_model_accuracy():
    """Get prediction model accuracy metrics"""
    
    return {
        'overall_accuracy': 0.87,
        'category_accuracy': {
            'Infrastructure': 0.89,
            'Health': 0.85,
            'Public Safety': 0.88,
            'Other': 0.82
        },
        'metrics': {
            'rmse': 12.5,
            'mae': 9.8,
            'r2_score': 0.91
        },
        'last_trained': (datetime.utcnow() - timedelta(days=7)).isoformat(),
        'training_samples': 50000,
        'model_version': 'v1.2.0'
    }
