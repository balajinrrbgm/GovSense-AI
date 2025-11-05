"""
Service Requests API - Feature 2: Smart Service Request Prioritization
"""

from fastapi import APIRouter, HTTPException
from datetime import datetime, timedelta
import uuid
import logging

from api.models import (
    ServiceRequestCreate,
    ServiceRequestResponse,
    ServiceRequestDetail,
    StatusEnum
)
from api.services.gemini_service import gemini_service
from api.services.prioritization_engine import prioritization_engine

logger = logging.getLogger(__name__)

router = APIRouter()

# In-memory storage for demo (in production, use BigQuery/database)
requests_db = {}


@router.post("/submit", response_model=ServiceRequestResponse)
async def submit_request(request: ServiceRequestCreate):
    """
    Submit a new service request
    
    Feature 2: Smart Service Request Prioritization
    - AI categorization with Gemini
    - Multi-factor priority scoring
    - Intelligent routing
    """
    
    try:
        # Generate unique IDs
        request_id = f"REQ-{datetime.utcnow().strftime('%Y%m%d')}-{uuid.uuid4().hex[:8].upper()}"
        tracking_id = f"TRK-{uuid.uuid4().hex[:12].upper()}"
        
        logger.info(f"Processing new request: {request_id}")
        
        # Step 1: AI Categorization using Gemini
        categorization = await gemini_service.categorize_request(
            description=request.description,
            location=f"{request.location_lat}, {request.location_lng}"
        )
        
        logger.info(f"Categorized as: {categorization.category.value} - {categorization.sub_category}")
        
        # Step 2: Calculate Priority Score
        priority_calc = prioritization_engine.calculate_priority(
            urgency=categorization.urgency,
            category=categorization.category,
            sentiment_score=categorization.sentiment_score,
            location_zone="Zone A"  # Mock - in production, derive from coordinates
        )
        
        logger.info(f"Priority score: {priority_calc['final_score']}")
        
        # Step 3: Route to Department
        routing = prioritization_engine.route_to_department(
            category=categorization.category,
            location_zone="Zone A"
        )
        
        logger.info(f"Routed to: {routing['department']} - {routing['team']}")
        
        # Step 4: Store request
        request_detail = ServiceRequestDetail(
            request_id=request_id,
            tracking_id=tracking_id,
            timestamp=datetime.utcnow(),
            description=request.description,
            category=categorization.category,
            sub_category=categorization.sub_category,
            urgency=categorization.urgency,
            priority_score=priority_calc['final_score'],
            status=StatusEnum.RECEIVED,
            location_lat=request.location_lat,
            location_lng=request.location_lng,
            location_address=request.location_address,
            location_zone="Zone A - Central Mumbai",
            assigned_department=routing['department'],
            assigned_officer=routing['officer'],
            estimated_resolution_hours=routing['estimated_hours'],
            actual_resolution_hours=None,
            citizen_satisfaction=None,
            feedback_text=None,
            sentiment_score=categorization.sentiment_score,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        
        requests_db[tracking_id] = request_detail
        
        # Return response
        return ServiceRequestResponse(
            request_id=request_id,
            tracking_id=tracking_id,
            timestamp=datetime.utcnow(),
            category=categorization.category,
            sub_category=categorization.sub_category,
            urgency=categorization.urgency,
            priority_score=priority_calc['final_score'],
            status=StatusEnum.RECEIVED,
            estimated_resolution_hours=routing['estimated_hours'],
            assigned_department=routing['department'],
            message=f"Request submitted successfully. Your tracking ID is {tracking_id}. Estimated resolution time: {routing['estimated_hours']} hours."
        )
        
    except Exception as e:
        logger.error(f"Request submission error: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to submit request: {str(e)}")


@router.get("/list", response_model=list)
async def list_requests(
    category: str = None,
    status: str = None,
    limit: int = 50
):
    """Get list of service requests"""
    
    try:
        requests_list = list(requests_db.values())
        
        # Filter by category
        if category:
            requests_list = [r for r in requests_list if r.category.value == category]
        
        # Filter by status
        if status:
            requests_list = [r for r in requests_list if r.status.value == status]
        
        # Sort by priority score (descending)
        requests_list.sort(key=lambda x: x.priority_score, reverse=True)
        
        # Limit results
        requests_list = requests_list[:limit]
        
        return [r.dict() for r in requests_list]
        
    except Exception as e:
        logger.error(f"List requests error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/stats", response_model=dict)
async def get_request_stats():
    """Get request statistics"""
    
    try:
        total = len(requests_db)
        
        if total == 0:
            return {
                'total_requests': 0,
                'by_category': {},
                'by_status': {},
                'by_urgency': {},
                'avg_priority_score': 0
            }
        
        requests_list = list(requests_db.values())
        
        # Count by category
        by_category = {}
        for req in requests_list:
            cat = req.category.value
            by_category[cat] = by_category.get(cat, 0) + 1
        
        # Count by status
        by_status = {}
        for req in requests_list:
            status = req.status.value
            by_status[status] = by_status.get(status, 0) + 1
        
        # Count by urgency
        by_urgency = {}
        for req in requests_list:
            urg = req.urgency.value
            by_urgency[urg] = by_urgency.get(urg, 0) + 1
        
        # Average priority score
        avg_priority = sum(r.priority_score for r in requests_list) / total
        
        return {
            'total_requests': total,
            'by_category': by_category,
            'by_status': by_status,
            'by_urgency': by_urgency,
            'avg_priority_score': round(avg_priority, 2)
        }
        
    except Exception as e:
        logger.error(f"Stats error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/demo-data", response_model=dict)
async def generate_demo_data(count: int = 20):
    """Generate demo service requests for testing"""
    
    try:
        demo_requests = [
            {
                "description": "Large pothole on Main Street near school causing traffic issues",
                "location_lat": 18.5204,
                "location_lng": 73.8567,
                "location_address": "Main Street, Pune"
            },
            {
                "description": "Water supply disruption in residential area for 3 days",
                "location_lat": 19.0760,
                "location_lng": 72.8777,
                "location_address": "Andheri West, Mumbai"
            },
            {
                "description": "Street lights not working in neighborhood, safety concern",
                "location_lat": 21.1458,
                "location_lng": 79.0882,
                "location_address": "Civil Lines, Nagpur"
            },
            {
                "description": "Urgent need for ambulance service, medical emergency",
                "location_lat": 19.9975,
                "location_lng": 73.7898,
                "location_address": "Nashik Road"
            },
            {
                "description": "Drainage overflow causing flooding in street",
                "location_lat": 19.2183,
                "location_lng": 72.9781,
                "location_address": "Thane West"
            }
        ]
        
        created_ids = []
        
        for i in range(min(count, len(demo_requests))):
            demo = demo_requests[i % len(demo_requests)]
            req = ServiceRequestCreate(**demo)
            response = await submit_request(req)
            created_ids.append(response.tracking_id)
        
        return {
            'message': f'Created {len(created_ids)} demo requests',
            'tracking_ids': created_ids
        }
        
    except Exception as e:
        logger.error(f"Demo data generation error: {e}")
        raise HTTPException(status_code=500, detail=str(e))
