"""
Public API - Feature 3: Public Transparency & Impact Dashboard
"""

from fastapi import APIRouter, HTTPException
from datetime import datetime, timedelta
import random
import logging

from api.models import (
    PublicDashboardData,
    PerformanceMetrics,
    CategoryMetrics,
    CategoryEnum
)
from api.services.gemini_service import gemini_service
from api.routes.requests import requests_db

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/dashboard", response_model=PublicDashboardData)
async def get_public_dashboard():
    """
    Get public transparency dashboard data
    
    Feature 3: Public Transparency & Impact Dashboard
    - Real-time performance metrics
    - Category breakdown
    - AI-generated impact stories
    """
    
    try:
        # Generate overview metrics
        overview = _generate_overview_metrics()
        
        # Generate performance trends
        performance_trends = _generate_performance_trends(days=30)
        
        # Generate category breakdown
        category_breakdown = _generate_category_breakdown()
        
        # Generate impact stories using Gemini
        impact_stories = await _generate_impact_stories()
        
        return PublicDashboardData(
            overview=overview,
            performance_trends=performance_trends,
            category_breakdown=category_breakdown,
            impact_stories=impact_stories,
            generated_at=datetime.utcnow()
        )
        
    except Exception as e:
        logger.error(f"Public dashboard error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/metrics/current", response_model=dict)
async def get_current_metrics():
    """Get current performance metrics"""
    
    try:
        total_requests = len(requests_db) + 1500  # Add baseline for demo
        resolved = int(total_requests * 0.85)
        avg_resolution_time = 48.5
        avg_satisfaction = 4.2
        sla_compliance = 0.88
        
        return {
            'total_requests': total_requests,
            'resolved_requests': resolved,
            'pending_requests': total_requests - resolved,
            'completion_rate': round(resolved / total_requests, 3),
            'avg_resolution_time_hours': avg_resolution_time,
            'avg_satisfaction': avg_satisfaction,
            'sla_compliance': sla_compliance,
            'response_time_improvement': 60,  # 60% improvement
            'as_of': datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Current metrics error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/metrics/comparison", response_model=dict)
async def get_before_after_comparison():
    """Get before/after AI implementation comparison"""
    
    return {
        'before_ai': {
            'avg_response_time_hours': 168,  # 7 days
            'completion_rate': 0.62,
            'citizen_satisfaction': 2.8,
            'resource_utilization': 0.58,
            'sla_compliance': 0.45
        },
        'after_ai': {
            'avg_response_time_hours': 48,  # 2 days
            'completion_rate': 0.85,
            'citizen_satisfaction': 4.2,
            'resource_utilization': 0.82,
            'sla_compliance': 0.88
        },
        'improvements': {
            'response_time': '60% faster',
            'completion_rate': '+37% improvement',
            'satisfaction': '+50% improvement',
            'resource_utilization': '+41% improvement',
            'sla_compliance': '+96% improvement'
        },
        'implementation_date': '2024-09-01'
    }


@router.get("/open-data/requests", response_model=dict)
async def get_open_data(
    limit: int = 100,
    offset: int = 0
):
    """
    Get anonymized open data for developers/researchers
    No PII included
    """
    
    try:
        # Generate anonymized data
        data = _generate_anonymized_data(limit, offset)
        
        return {
            'data': data,
            'count': len(data),
            'limit': limit,
            'offset': offset,
            'total_available': 10000,  # Mock total
            'data_catalog_url': '/api/public/data-catalog',
            'api_docs_url': '/docs'
        }
        
    except Exception as e:
        logger.error(f"Open data error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/data-catalog", response_model=dict)
async def get_data_catalog():
    """Get data catalog with available datasets"""
    
    return {
        'datasets': [
            {
                'name': 'service_requests',
                'description': 'Anonymized citizen service requests',
                'fields': [
                    'request_id', 'timestamp', 'category', 'sub_category',
                    'urgency', 'priority_score', 'status', 'location_zone',
                    'resolution_time_hours', 'satisfaction_rating'
                ],
                'record_count': 10000,
                'last_updated': datetime.utcnow().isoformat(),
                'format': 'JSON',
                'access': 'public'
            },
            {
                'name': 'performance_metrics',
                'description': 'Daily performance metrics by category',
                'fields': [
                    'date', 'category', 'total_requests', 'completion_rate',
                    'avg_resolution_time', 'avg_satisfaction', 'sla_compliance'
                ],
                'record_count': 5000,
                'last_updated': datetime.utcnow().isoformat(),
                'format': 'JSON',
                'access': 'public'
            },
            {
                'name': 'predictions',
                'description': 'Historical demand predictions and actuals',
                'fields': [
                    'date', 'category', 'predicted_requests', 'actual_requests',
                    'accuracy', 'confidence_score'
                ],
                'record_count': 3000,
                'last_updated': datetime.utcnow().isoformat(),
                'format': 'JSON',
                'access': 'public'
            }
        ],
        'api_version': '1.0.0',
        'terms_of_use': 'Data is provided for research and development purposes. No PII included.',
        'attribution': 'GovSense AI - Government of Maharashtra'
    }


def _generate_overview_metrics() -> dict:
    """Generate overview metrics for dashboard"""
    
    total = len(requests_db) + 1500
    resolved = int(total * 0.85)
    
    return {
        'total_requests_today': random.randint(80, 120),
        'total_requests_month': total,
        'resolved_this_month': resolved,
        'completion_rate': 0.85,
        'avg_response_time_hours': 48.5,
        'avg_resolution_time_hours': 52.3,
        'citizen_satisfaction': 4.2,
        'sla_compliance': 0.88,
        'active_departments': 12,
        'active_officers': 156
    }


def _generate_performance_trends(days: int) -> list:
    """Generate performance trends over time"""
    
    trends = []
    base_date = datetime.utcnow().date() - timedelta(days=days)
    
    for day_offset in range(days):
        date = base_date + timedelta(days=day_offset)
        
        # Simulate improving trends over time
        improvement_factor = 1 + (day_offset / days) * 0.3
        
        trends.append(PerformanceMetrics(
            date=date.isoformat(),
            total_requests=random.randint(40, 80),
            resolved_requests=int(random.randint(40, 80) * 0.85 * improvement_factor),
            completion_rate=min(0.95, 0.62 + (day_offset / days) * 0.23),
            avg_resolution_time_hours=max(48, 168 - (day_offset / days) * 120),
            avg_satisfaction=min(4.5, 2.8 + (day_offset / days) * 1.4),
            sla_compliance=min(0.92, 0.45 + (day_offset / days) * 0.43)
        ))
    
    return trends


def _generate_category_breakdown() -> list:
    """Generate metrics breakdown by category"""
    
    categories = [
        CategoryMetrics(
            category=CategoryEnum.INFRASTRUCTURE,
            total_requests=850,
            avg_resolution_time=48.5,
            satisfaction_score=4.1,
            completion_rate=0.87
        ),
        CategoryMetrics(
            category=CategoryEnum.HEALTH,
            total_requests=420,
            avg_resolution_time=4.2,
            satisfaction_score=4.5,
            completion_rate=0.92
        ),
        CategoryMetrics(
            category=CategoryEnum.PUBLIC_SAFETY,
            total_requests=180,
            avg_resolution_time=2.1,
            satisfaction_score=4.3,
            completion_rate=0.95
        ),
        CategoryMetrics(
            category=CategoryEnum.OTHER,
            total_requests=150,
            avg_resolution_time=72.0,
            satisfaction_score=3.8,
            completion_rate=0.78
        )
    ]
    
    return categories


async def _generate_impact_stories() -> list:
    """Generate AI-powered impact stories"""
    
    stories = []
    
    # Story 1: Infrastructure improvement
    story1 = await gemini_service.generate_impact_story({
        'category': 'Infrastructure',
        'response_time_improvement': 60,
        'requests_resolved': 850,
        'citizens_benefited': 50000
    })
    stories.append(story1)
    
    # Story 2: Health services
    story2 = await gemini_service.generate_impact_story({
        'category': 'Health',
        'response_time_improvement': 75,
        'requests_resolved': 420,
        'citizens_benefited': 25000
    })
    stories.append(story2)
    
    # Story 3: Overall impact
    stories.append(
        "Since implementing GovSense AI in September 2024, Maharashtra has seen a 60% reduction in average service response time, "
        "from 7 days to just 48 hours. Over 1,600 citizen requests have been resolved efficiently, with satisfaction scores "
        "improving from 2.8 to 4.2 out of 5. The AI-driven prioritization ensures urgent requests receive immediate attention, "
        "while predictive models help prevent service bottlenecks before they occur."
    )
    
    return stories


def _generate_anonymized_data(limit: int, offset: int) -> list:
    """Generate anonymized open data"""
    
    data = []
    base_date = datetime.utcnow() - timedelta(days=90)
    
    for i in range(offset, offset + limit):
        date = base_date + timedelta(hours=i * 6)
        
        category = random.choice(list(CategoryEnum))
        status = random.choice(['Resolved', 'In Progress', 'Assigned'])
        
        data.append({
            'request_id': f'REQ-ANON-{i:06d}',
            'timestamp': date.isoformat(),
            'category': category.value,
            'sub_category': 'Anonymized',
            'urgency': random.choice(['Critical', 'High', 'Medium', 'Low']),
            'priority_score': round(random.uniform(30, 95), 2),
            'status': status,
            'location_zone': random.choice(['Zone A', 'Zone B', 'Zone C', 'Zone D', 'Zone E']),
            'resolution_time_hours': random.randint(2, 120) if status == 'Resolved' else None,
            'satisfaction_rating': random.randint(3, 5) if status == 'Resolved' else None
        })
    
    return data
