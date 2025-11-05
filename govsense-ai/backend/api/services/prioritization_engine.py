"""
Service Request Prioritization Engine
Multi-factor scoring algorithm
"""

import logging
from datetime import datetime
from typing import Dict
from api.models import UrgencyEnum, CategoryEnum, PriorityFactors

logger = logging.getLogger(__name__)


class PrioritizationEngine:
    """Engine for calculating request priority scores"""
    
    # Weights for different factors (must sum to 1.0)
    WEIGHTS = {
        'urgency': 0.30,
        'impact': 0.25,
        'resources': 0.20,
        'sla': 0.15,
        'sentiment': 0.10
    }
    
    # Urgency level scores
    URGENCY_SCORES = {
        UrgencyEnum.CRITICAL: 100,
        UrgencyEnum.HIGH: 75,
        UrgencyEnum.MEDIUM: 50,
        UrgencyEnum.LOW: 25
    }
    
    # Category impact scores (population typically affected)
    CATEGORY_IMPACT = {
        CategoryEnum.PUBLIC_SAFETY: 90,
        CategoryEnum.HEALTH: 85,
        CategoryEnum.INFRASTRUCTURE: 70,
        CategoryEnum.OTHER: 50
    }
    
    def calculate_priority(
        self,
        urgency: UrgencyEnum,
        category: CategoryEnum,
        sentiment_score: float,
        location_zone: str = None
    ) -> Dict:
        """
        Calculate priority score based on multiple factors
        
        Returns:
            dict with final_score, urgency_level, factors, and explanation
        """
        
        # 1. Urgency Score (0-100)
        urgency_score = self.URGENCY_SCORES.get(urgency, 50)
        
        # 2. Impact Score (0-100) - based on category and location
        impact_score = self._calculate_impact_score(category, location_zone)
        
        # 3. Resource Availability Score (0-100)
        resource_score = self._calculate_resource_availability(category)
        
        # 4. SLA Compliance Score (0-100)
        sla_score = 100  # New request, full SLA time available
        
        # 5. Sentiment Score (0-100)
        sentiment_normalized = sentiment_score * 100
        
        # Calculate weighted final score
        final_score = (
            urgency_score * self.WEIGHTS['urgency'] +
            impact_score * self.WEIGHTS['impact'] +
            resource_score * self.WEIGHTS['resources'] +
            sla_score * self.WEIGHTS['sla'] +
            sentiment_normalized * self.WEIGHTS['sentiment']
        )
        
        # Determine urgency level based on final score
        if final_score >= 80:
            urgency_level = UrgencyEnum.CRITICAL
        elif final_score >= 60:
            urgency_level = UrgencyEnum.HIGH
        elif final_score >= 40:
            urgency_level = UrgencyEnum.MEDIUM
        else:
            urgency_level = UrgencyEnum.LOW
        
        # Create factors object
        factors = PriorityFactors(
            urgency_score=urgency_score,
            impact_score=impact_score,
            resource_availability=resource_score,
            sla_score=sla_score,
            historical_pattern=70.0,  # Mock value
            sentiment_score=sentiment_normalized
        )
        
        # Generate explanation
        explanation = self._generate_explanation(
            final_score, urgency_level, urgency, category, sentiment_score
        )
        
        return {
            'final_score': round(final_score, 2),
            'urgency_level': urgency_level,
            'factors': factors,
            'explanation': explanation
        }
    
    def _calculate_impact_score(self, category: CategoryEnum, location_zone: str = None) -> float:
        """Calculate impact score based on category and location"""
        
        base_score = self.CATEGORY_IMPACT.get(category, 50)
        
        # Adjust based on location (mock - in production, use population data)
        if location_zone:
            # High-density zones get higher impact scores
            if 'Zone A' in str(location_zone) or 'Central' in str(location_zone):
                base_score = min(100, base_score * 1.2)
            elif 'Zone B' in str(location_zone):
                base_score = min(100, base_score * 1.1)
        
        return base_score
    
    def _calculate_resource_availability(self, category: CategoryEnum) -> float:
        """Calculate resource availability score"""
        
        # Mock implementation - in production, query actual resource data
        # Higher score = more resources available = can handle request faster
        
        resource_levels = {
            CategoryEnum.INFRASTRUCTURE: 78,  # Good availability
            CategoryEnum.HEALTH: 65,  # Moderate availability
            CategoryEnum.PUBLIC_SAFETY: 85,  # High availability
            CategoryEnum.OTHER: 70  # Average availability
        }
        
        return resource_levels.get(category, 70)
    
    def _generate_explanation(
        self,
        final_score: float,
        urgency_level: UrgencyEnum,
        original_urgency: UrgencyEnum,
        category: CategoryEnum,
        sentiment: float
    ) -> str:
        """Generate human-readable explanation of priority score"""
        
        explanation_parts = [
            f"Priority Score: {final_score:.0f}/100 - {urgency_level.value} Priority"
        ]
        
        if final_score >= 80:
            explanation_parts.append(
                "This request requires immediate attention due to high urgency and significant impact."
            )
        elif final_score >= 60:
            explanation_parts.append(
                "This request should be addressed promptly to prevent escalation."
            )
        else:
            explanation_parts.append(
                "This request can be handled within normal workflow timelines."
            )
        
        # Add category-specific context
        if category == CategoryEnum.PUBLIC_SAFETY:
            explanation_parts.append("Public safety requests are prioritized for rapid response.")
        elif category == CategoryEnum.HEALTH:
            explanation_parts.append("Health-related requests receive elevated priority.")
        
        # Add sentiment context
        if sentiment > 0.7:
            explanation_parts.append(
                "Citizen sentiment indicates high frustration - recommend expedited handling."
            )
        
        return " ".join(explanation_parts)
    
    def route_to_department(self, category: CategoryEnum, location_zone: str = None) -> Dict:
        """Route request to appropriate department and team"""
        
        # Department mapping
        department_map = {
            CategoryEnum.INFRASTRUCTURE: "Infrastructure & Public Works",
            CategoryEnum.HEALTH: "Health & Medical Services",
            CategoryEnum.PUBLIC_SAFETY: "Police & Emergency Services",
            CategoryEnum.OTHER: "General Administration"
        }
        
        department = department_map.get(category, "General Administration")
        
        # Mock team assignment (in production, use load balancing algorithm)
        teams = {
            "Infrastructure & Public Works": ["Team A - Zone 1", "Team B - Zone 2", "Team C - Zone 3"],
            "Health & Medical Services": ["Medical Team 1", "Medical Team 2", "Ambulance Unit"],
            "Police & Emergency Services": ["Patrol Unit 1", "Patrol Unit 2", "Emergency Response"],
            "General Administration": ["Admin Team 1", "Admin Team 2"]
        }
        
        # Simple round-robin assignment (mock)
        available_teams = teams.get(department, ["Default Team"])
        assigned_team = available_teams[0]  # In production, use load balancing
        
        return {
            'department': department,
            'team': assigned_team,
            'officer': f"Officer-{hash(department) % 1000:03d}",  # Mock officer ID
            'estimated_hours': self._estimate_resolution_time(category)
        }
    
    def _estimate_resolution_time(self, category: CategoryEnum) -> int:
        """Estimate resolution time in hours based on category"""
        
        estimates = {
            CategoryEnum.INFRASTRUCTURE: 48,
            CategoryEnum.HEALTH: 4,
            CategoryEnum.PUBLIC_SAFETY: 2,
            CategoryEnum.OTHER: 72
        }
        
        return estimates.get(category, 48)


# Create singleton instance
prioritization_engine = PrioritizationEngine()
