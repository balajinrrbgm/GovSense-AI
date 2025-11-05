"""
Data models for GovSense AI
"""

from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum


class CategoryEnum(str, Enum):
    """Service request categories"""
    HEALTH = "Health"
    INFRASTRUCTURE = "Infrastructure"
    PUBLIC_SAFETY = "Public Safety"
    OTHER = "Other"


class UrgencyEnum(str, Enum):
    """Urgency levels"""
    CRITICAL = "Critical"
    HIGH = "High"
    MEDIUM = "Medium"
    LOW = "Low"


class StatusEnum(str, Enum):
    """Request status"""
    RECEIVED = "Received"
    ASSIGNED = "Assigned"
    IN_PROGRESS = "In Progress"
    RESOLVED = "Resolved"
    CLOSED = "Closed"


# Service Request Models
class ServiceRequestCreate(BaseModel):
    """Model for creating a new service request"""
    description: str = Field(..., min_length=10, max_length=1000)
    location_lat: float = Field(..., ge=-90, le=90)
    location_lng: float = Field(..., ge=-180, le=180)
    location_address: Optional[str] = None
    citizen_name: Optional[str] = None
    citizen_phone: Optional[str] = None
    citizen_email: Optional[str] = None
    photo_url: Optional[str] = None


class ServiceRequestResponse(BaseModel):
    """Model for service request response"""
    request_id: str
    tracking_id: str
    timestamp: datetime
    category: CategoryEnum
    sub_category: Optional[str]
    urgency: UrgencyEnum
    priority_score: float
    status: StatusEnum
    estimated_resolution_hours: int
    assigned_department: Optional[str]
    message: str


class ServiceRequestDetail(BaseModel):
    """Detailed service request information"""
    request_id: str
    tracking_id: str
    timestamp: datetime
    description: str
    category: CategoryEnum
    sub_category: Optional[str]
    urgency: UrgencyEnum
    priority_score: float
    status: StatusEnum
    location_lat: float
    location_lng: float
    location_address: Optional[str]
    location_zone: Optional[str]
    assigned_department: Optional[str]
    assigned_officer: Optional[str]
    estimated_resolution_hours: int
    actual_resolution_hours: Optional[int]
    citizen_satisfaction: Optional[int]
    feedback_text: Optional[str]
    sentiment_score: Optional[float]
    created_at: datetime
    updated_at: datetime


# Prediction Models
class DemandPrediction(BaseModel):
    """Model for demand prediction"""
    date: str
    category: CategoryEnum
    location_zone: Optional[str]
    predicted_requests: int
    confidence_lower: int
    confidence_upper: int
    confidence_score: float


class PredictionRequest(BaseModel):
    """Request for predictions"""
    category: Optional[CategoryEnum] = None
    location_zone: Optional[str] = None
    days: int = Field(default=30, ge=1, le=90)


class PredictionResponse(BaseModel):
    """Response with predictions"""
    predictions: List[DemandPrediction]
    insights: Optional[str]
    generated_at: datetime


# AI Categorization Models
class CategorizationResult(BaseModel):
    """Result from AI categorization"""
    category: CategoryEnum
    sub_category: str
    urgency: UrgencyEnum
    sentiment_score: float
    summary: str
    recommended_action: str
    confidence: float


# Public Metrics Models
class PerformanceMetrics(BaseModel):
    """Performance metrics for public dashboard"""
    date: str
    total_requests: int
    resolved_requests: int
    completion_rate: float
    avg_resolution_time_hours: float
    avg_satisfaction: float
    sla_compliance: float


class CategoryMetrics(BaseModel):
    """Metrics by category"""
    category: CategoryEnum
    total_requests: int
    avg_resolution_time: float
    satisfaction_score: float
    completion_rate: float


class PublicDashboardData(BaseModel):
    """Data for public transparency dashboard"""
    overview: dict
    performance_trends: List[PerformanceMetrics]
    category_breakdown: List[CategoryMetrics]
    impact_stories: List[str]
    generated_at: datetime


# Tracking Models
class TrackingResponse(BaseModel):
    """Response for request tracking"""
    tracking_id: str
    status: StatusEnum
    current_stage: str
    progress_percentage: int
    estimated_completion: Optional[datetime]
    timeline: List[dict]
    last_updated: datetime


# Priority Scoring Models
class PriorityFactors(BaseModel):
    """Factors used in priority calculation"""
    urgency_score: float
    impact_score: float
    resource_availability: float
    sla_score: float
    historical_pattern: float
    sentiment_score: float


class PriorityCalculation(BaseModel):
    """Detailed priority calculation"""
    final_score: float
    urgency_level: UrgencyEnum
    factors: PriorityFactors
    explanation: str
