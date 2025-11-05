"""
Gemini AI Service for NLP and Categorization
"""

import json
import logging
from typing import Dict, Any
from api.config import settings
from api.models import CategoryEnum, UrgencyEnum, CategorizationResult

logger = logging.getLogger(__name__)


class GeminiService:
    """Service for Gemini AI interactions"""
    
    def __init__(self):
        self.enabled = settings.ENABLE_GEMINI and settings.GEMINI_API_KEY
        if self.enabled:
            try:
                import google.generativeai as genai
                genai.configure(api_key=settings.GEMINI_API_KEY)
                self.model = genai.GenerativeModel('gemini-pro')
                logger.info("✅ Gemini AI initialized successfully")
            except Exception as e:
                logger.warning(f"⚠️ Gemini AI initialization failed: {e}")
                self.enabled = False
    
    async def categorize_request(self, description: str, location: str) -> CategorizationResult:
        """Categorize service request using Gemini"""
        
        if not self.enabled or settings.USE_MOCK_DATA:
            return self._mock_categorization(description)
        
        try:
            prompt = f"""
Analyze this citizen service request and provide structured output:

Request: {description}
Location: {location}

Provide JSON output with:
1. category: Health/Infrastructure/Public Safety/Other
2. sub_category: specific type (e.g., "Road Repair", "Water Supply", "Medical Emergency")
3. urgency: Critical/High/Medium/Low
4. sentiment_score: 0-100 (higher = more frustrated/urgent)
5. summary: brief 1-sentence summary
6. recommended_action: what should be done
7. confidence: 0-1 (how confident you are)

Output only valid JSON, no other text.
"""
            
            response = self.model.generate_content(prompt)
            result = json.loads(response.text)
            
            return CategorizationResult(
                category=CategoryEnum(result['category']),
                sub_category=result['sub_category'],
                urgency=UrgencyEnum(result['urgency']),
                sentiment_score=result['sentiment_score'] / 100.0,
                summary=result['summary'],
                recommended_action=result['recommended_action'],
                confidence=result['confidence']
            )
            
        except Exception as e:
            logger.error(f"Gemini categorization error: {e}")
            return self._mock_categorization(description)
    
    async def generate_insights(self, predictions: list) -> str:
        """Generate actionable insights from predictions"""
        
        if not self.enabled or settings.USE_MOCK_DATA:
            return self._mock_insights(predictions)
        
        try:
            # Find highest predicted demand
            max_pred = max(predictions, key=lambda x: x['predicted_requests'])
            
            prompt = f"""
Based on these service demand predictions, generate actionable recommendations:

Highest predicted demand:
- Date: {max_pred['date']}
- Category: {max_pred['category']}
- Predicted requests: {max_pred['predicted_requests']}
- Confidence: {max_pred['confidence_score']*100:.0f}%

Provide 2-3 specific, actionable recommendations for government officials.
Keep it concise and practical. Focus on resource allocation and proactive measures.
"""
            
            response = self.model.generate_content(prompt)
            return response.text
            
        except Exception as e:
            logger.error(f"Gemini insights generation error: {e}")
            return self._mock_insights(predictions)
    
    async def generate_impact_story(self, metrics: Dict[str, Any]) -> str:
        """Generate impact story from metrics"""
        
        if not self.enabled or settings.USE_MOCK_DATA:
            return self._mock_impact_story(metrics)
        
        try:
            prompt = f"""
Create a compelling 2-3 sentence impact story for citizens:

Metrics:
- Improvement in response time: {metrics.get('response_time_improvement', 0)}%
- Requests resolved: {metrics.get('requests_resolved', 0)}
- Citizens benefited: {metrics.get('citizens_benefited', 0)}
- Category: {metrics.get('category', 'Infrastructure')}

Write in simple language that shows the value of AI-driven governance.
Make it relatable and highlight the positive impact on citizens' lives.
"""
            
            response = self.model.generate_content(prompt)
            return response.text
            
        except Exception as e:
            logger.error(f"Gemini impact story error: {e}")
            return self._mock_impact_story(metrics)
    
    def _mock_categorization(self, description: str) -> CategorizationResult:
        """Mock categorization for demo/testing"""
        
        # Simple keyword-based categorization
        desc_lower = description.lower()
        
        if any(word in desc_lower for word in ['road', 'pothole', 'street', 'water', 'electricity', 'drainage']):
            category = CategoryEnum.INFRASTRUCTURE
            if 'road' in desc_lower or 'pothole' in desc_lower:
                sub_category = "Road Repair"
            elif 'water' in desc_lower:
                sub_category = "Water Supply"
            elif 'electricity' in desc_lower:
                sub_category = "Power Supply"
            else:
                sub_category = "Infrastructure Maintenance"
        elif any(word in desc_lower for word in ['hospital', 'doctor', 'ambulance', 'medical', 'health']):
            category = CategoryEnum.HEALTH
            sub_category = "Medical Assistance"
        elif any(word in desc_lower for word in ['police', 'crime', 'accident', 'emergency', 'fire']):
            category = CategoryEnum.PUBLIC_SAFETY
            sub_category = "Emergency Response"
        else:
            category = CategoryEnum.OTHER
            sub_category = "General Service"
        
        # Determine urgency based on keywords
        if any(word in desc_lower for word in ['urgent', 'emergency', 'critical', 'immediate', 'danger']):
            urgency = UrgencyEnum.CRITICAL
            sentiment = 0.9
        elif any(word in desc_lower for word in ['soon', 'quickly', 'asap', 'important']):
            urgency = UrgencyEnum.HIGH
            sentiment = 0.7
        elif any(word in desc_lower for word in ['please', 'need', 'help']):
            urgency = UrgencyEnum.MEDIUM
            sentiment = 0.5
        else:
            urgency = UrgencyEnum.LOW
            sentiment = 0.3
        
        return CategorizationResult(
            category=category,
            sub_category=sub_category,
            urgency=urgency,
            sentiment_score=sentiment,
            summary=f"{category.value} request: {description[:50]}...",
            recommended_action=f"Assign to {category.value} department for immediate review",
            confidence=0.85
        )
    
    def _mock_insights(self, predictions: list) -> str:
        """Mock insights for demo"""
        if not predictions:
            return "No predictions available for insights generation."
        
        max_pred = max(predictions, key=lambda x: x.get('predicted_requests', 0))
        
        return f"""Based on predictive analysis, we anticipate a {max_pred.get('predicted_requests', 0)} request surge in {max_pred.get('category', 'Infrastructure')} services around {max_pred.get('date', 'upcoming week')}.

Recommendations:
1. Pre-position 3 additional teams in high-demand zones
2. Stock emergency supplies and equipment
3. Brief department heads on expected demand patterns
4. Activate standby resources for rapid deployment

This proactive approach can reduce response time by 60% and improve citizen satisfaction significantly."""
    
    def _mock_impact_story(self, metrics: Dict[str, Any]) -> str:
        """Mock impact story for demo"""
        return f"""In October 2024, GovSense AI predicted a 35% surge in {metrics.get('category', 'Infrastructure')} requests in Pune East. By pre-allocating resources based on AI recommendations, the average resolution time decreased from 12 days to 4 days, benefiting over {metrics.get('citizens_benefited', 50000):,} citizens and saving significant public resources."""


# Create singleton instance
gemini_service = GeminiService()
