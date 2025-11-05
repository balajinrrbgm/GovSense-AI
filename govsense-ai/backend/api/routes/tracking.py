"""
Tracking API - Track service request status
"""

from fastapi import APIRouter, HTTPException
from datetime import datetime, timedelta
import logging

from api.models import TrackingResponse, StatusEnum
from api.routes.requests import requests_db

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/{tracking_id}", response_model=TrackingResponse)
async def track_request(tracking_id: str):
    """
    Track service request status by tracking ID
    
    Returns current status, timeline, and estimated completion
    """
    
    try:
        # Get request from database
        if tracking_id not in requests_db:
            raise HTTPException(status_code=404, detail=f"Request not found: {tracking_id}")
        
        request = requests_db[tracking_id]
        
        # Calculate progress percentage
        progress_map = {
            StatusEnum.RECEIVED: 20,
            StatusEnum.ASSIGNED: 40,
            StatusEnum.IN_PROGRESS: 70,
            StatusEnum.RESOLVED: 100,
            StatusEnum.CLOSED: 100
        }
        progress = progress_map.get(request.status, 0)
        
        # Calculate estimated completion
        if request.status in [StatusEnum.RESOLVED, StatusEnum.CLOSED]:
            estimated_completion = None
        else:
            estimated_completion = request.created_at + timedelta(hours=request.estimated_resolution_hours)
        
        # Build timeline
        timeline = _build_timeline(request)
        
        # Current stage description
        stage_descriptions = {
            StatusEnum.RECEIVED: "Request received and being processed",
            StatusEnum.ASSIGNED: f"Assigned to {request.assigned_department}",
            StatusEnum.IN_PROGRESS: f"Being handled by {request.assigned_officer}",
            StatusEnum.RESOLVED: "Request has been resolved",
            StatusEnum.CLOSED: "Request closed"
        }
        current_stage = stage_descriptions.get(request.status, "Processing")
        
        return TrackingResponse(
            tracking_id=tracking_id,
            status=request.status,
            current_stage=current_stage,
            progress_percentage=progress,
            estimated_completion=estimated_completion,
            timeline=timeline,
            last_updated=request.updated_at
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Tracking error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/{tracking_id}/update", response_model=dict)
async def update_request_status(tracking_id: str, new_status: StatusEnum):
    """
    Update request status (for demo purposes)
    In production, this would be restricted to authorized officials
    """
    
    try:
        if tracking_id not in requests_db:
            raise HTTPException(status_code=404, detail=f"Request not found: {tracking_id}")
        
        request = requests_db[tracking_id]
        old_status = request.status
        request.status = new_status
        request.updated_at = datetime.utcnow()
        
        # If resolved, set actual resolution time
        if new_status == StatusEnum.RESOLVED:
            time_diff = datetime.utcnow() - request.created_at
            request.actual_resolution_hours = int(time_diff.total_seconds() / 3600)
        
        return {
            'message': f'Status updated from {old_status.value} to {new_status.value}',
            'tracking_id': tracking_id,
            'new_status': new_status.value,
            'updated_at': request.updated_at.isoformat()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Status update error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/{tracking_id}/feedback", response_model=dict)
async def submit_feedback(
    tracking_id: str,
    satisfaction: int,
    feedback_text: str = None
):
    """
    Submit citizen feedback for resolved request
    
    Args:
        tracking_id: Request tracking ID
        satisfaction: Rating 1-5
        feedback_text: Optional feedback text
    """
    
    try:
        if tracking_id not in requests_db:
            raise HTTPException(status_code=404, detail=f"Request not found: {tracking_id}")
        
        if not 1 <= satisfaction <= 5:
            raise HTTPException(status_code=400, detail="Satisfaction must be between 1 and 5")
        
        request = requests_db[tracking_id]
        
        if request.status not in [StatusEnum.RESOLVED, StatusEnum.CLOSED]:
            raise HTTPException(
                status_code=400,
                detail="Feedback can only be submitted for resolved requests"
            )
        
        request.citizen_satisfaction = satisfaction
        request.feedback_text = feedback_text
        request.updated_at = datetime.utcnow()
        
        # Close the request after feedback
        if request.status == StatusEnum.RESOLVED:
            request.status = StatusEnum.CLOSED
        
        return {
            'message': 'Thank you for your feedback!',
            'tracking_id': tracking_id,
            'satisfaction': satisfaction,
            'status': request.status.value
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Feedback submission error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


def _build_timeline(request) -> list:
    """Build timeline of request events"""
    
    timeline = [
        {
            'stage': 'Received',
            'status': StatusEnum.RECEIVED.value,
            'timestamp': request.created_at.isoformat(),
            'description': 'Request received and categorized',
            'completed': True
        }
    ]
    
    # Add assigned stage if applicable
    if request.status in [StatusEnum.ASSIGNED, StatusEnum.IN_PROGRESS, StatusEnum.RESOLVED, StatusEnum.CLOSED]:
        timeline.append({
            'stage': 'Assigned',
            'status': StatusEnum.ASSIGNED.value,
            'timestamp': (request.created_at + timedelta(minutes=15)).isoformat(),
            'description': f'Assigned to {request.assigned_department}',
            'completed': True
        })
    
    # Add in-progress stage if applicable
    if request.status in [StatusEnum.IN_PROGRESS, StatusEnum.RESOLVED, StatusEnum.CLOSED]:
        timeline.append({
            'stage': 'In Progress',
            'status': StatusEnum.IN_PROGRESS.value,
            'timestamp': (request.created_at + timedelta(hours=2)).isoformat(),
            'description': f'Being handled by {request.assigned_officer}',
            'completed': True
        })
    
    # Add resolved stage if applicable
    if request.status in [StatusEnum.RESOLVED, StatusEnum.CLOSED]:
        resolution_time = request.created_at + timedelta(hours=request.actual_resolution_hours or request.estimated_resolution_hours)
        timeline.append({
            'stage': 'Resolved',
            'status': StatusEnum.RESOLVED.value,
            'timestamp': resolution_time.isoformat(),
            'description': 'Request has been resolved',
            'completed': True
        })
    
    # Add closed stage if applicable
    if request.status == StatusEnum.CLOSED:
        timeline.append({
            'stage': 'Closed',
            'status': StatusEnum.CLOSED.value,
            'timestamp': request.updated_at.isoformat(),
            'description': 'Request closed with citizen feedback',
            'completed': True
        })
    
    return timeline
