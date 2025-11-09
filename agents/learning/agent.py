"""
Learning Agent - Processes feedback and improves system performance
"""
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
from collections import defaultdict

logger = logging.getLogger(__name__)


class LearningAgent:
    """Agent responsible for learning from feedback and improving system"""
    
    def __init__(self):
        self.name = "LearningAgent"
        self.version = "1.0.0"
        
        # In-memory storage (in production, use database)
        self.feedback_history = []
        self.performance_metrics = defaultdict(list)
        
        logger.info(f"{self.name} v{self.version} initialized")
    
    def process_feedback(
        self,
        rfp_id: str,
        feedback_type: str,
        rating: int,
        comments: str = None,
        match_accuracy: float = None,
        pricing_accuracy: float = None,
        response_time: float = None
    ) -> Dict[str, Any]:
        """
        Process user feedback and update metrics
        
        Args:
            rfp_id: RFP identifier
            feedback_type: Type of feedback (win/loss/accuracy)
            rating: Rating score (1-5)
            comments: Optional feedback comments
            match_accuracy: Product match accuracy (0-1)
            pricing_accuracy: Pricing accuracy (0-1)
            response_time: Response time in seconds
            
        Returns:
            Processing result with insights
        """
        try:
            logger.info(f"Processing feedback for RFP: {rfp_id}")
            
            feedback_entry = {
                'rfp_id': rfp_id,
                'feedback_type': feedback_type,
                'rating': rating,
                'comments': comments,
                'match_accuracy': match_accuracy,
                'pricing_accuracy': pricing_accuracy,
                'response_time': response_time,
                'timestamp': datetime.now()
            }
            
            # Store feedback
            self.feedback_history.append(feedback_entry)
            
            # Update metrics
            self._update_metrics(feedback_entry)
            
            # Generate insights
            insights = self._generate_insights(feedback_entry)
            
            return {
                'status': 'processed',
                'rfp_id': rfp_id,
                'insights': insights,
                'recommendations': self._get_recommendations(feedback_type, rating)
            }
            
        except Exception as e:
            logger.error(f"Error processing feedback: {str(e)}")
            return {
                'status': 'error',
                'error': str(e)
            }
    
    def _update_metrics(self, feedback: Dict[str, Any]):
        """Update performance metrics"""
        
        # Update rating metrics
        self.performance_metrics['ratings'].append({
            'rating': feedback['rating'],
            'timestamp': feedback['timestamp']
        })
        
        # Update accuracy metrics
        if feedback['match_accuracy'] is not None:
            self.performance_metrics['match_accuracy'].append({
                'accuracy': feedback['match_accuracy'],
                'timestamp': feedback['timestamp']
            })
        
        if feedback['pricing_accuracy'] is not None:
            self.performance_metrics['pricing_accuracy'].append({
                'accuracy': feedback['pricing_accuracy'],
                'timestamp': feedback['timestamp']
            })
        
        # Update response time metrics
        if feedback['response_time'] is not None:
            self.performance_metrics['response_time'].append({
                'time': feedback['response_time'],
                'timestamp': feedback['timestamp']
            })
        
        # Update feedback type distribution
        self.performance_metrics['feedback_types'].append({
            'type': feedback['feedback_type'],
            'timestamp': feedback['timestamp']
        })
    
    def _generate_insights(self, feedback: Dict[str, Any]) -> List[str]:
        """Generate insights from feedback"""
        insights = []
        
        # Rating insights
        if feedback['rating'] <= 2:
            insights.append("Low rating detected. Review RFP processing pipeline.")
        elif feedback['rating'] >= 4:
            insights.append("High rating. Current approach is effective.")
        
        # Match accuracy insights
        if feedback['match_accuracy'] is not None:
            if feedback['match_accuracy'] < 0.7:
                insights.append(
                    "Product matching accuracy is low. "
                    "Consider updating matching algorithms."
                )
            elif feedback['match_accuracy'] >= 0.9:
                insights.append("Excellent product matching performance.")
        
        # Pricing accuracy insights
        if feedback['pricing_accuracy'] is not None:
            if feedback['pricing_accuracy'] < 0.8:
                insights.append(
                    "Pricing estimates need improvement. "
                    "Review cost calculation logic."
                )
        
        # Response time insights
        if feedback['response_time'] is not None:
            if feedback['response_time'] > 300:  # 5 minutes
                insights.append(
                    "Response time is high. "
                    "Optimize agent execution pipeline."
                )
        
        # Comments analysis
        if feedback['comments']:
            insights.extend(self._analyze_comments(feedback['comments']))
        
        return insights
    
    def _analyze_comments(self, comments: str) -> List[str]:
        """Analyze feedback comments for insights"""
        insights = []
        comments_lower = comments.lower()
        
        # Keyword-based analysis (in production, use NLP)
        if any(word in comments_lower for word in ['slow', 'delayed', 'late']):
            insights.append("User mentioned speed issues. Investigate processing time.")
        
        if any(word in comments_lower for word in ['wrong', 'incorrect', 'inaccurate']):
            insights.append("Accuracy issues mentioned. Review matching/pricing logic.")
        
        if any(word in comments_lower for word in ['expensive', 'costly', 'price']):
            insights.append("Pricing concerns raised. Review cost calculations.")
        
        if any(word in comments_lower for word in ['good', 'great', 'excellent']):
            insights.append("Positive feedback received. Maintain current approach.")
        
        return insights
    
    def _get_recommendations(
        self,
        feedback_type: str,
        rating: int
    ) -> List[str]:
        """Get recommendations based on feedback"""
        recommendations = []
        
        if feedback_type == 'loss' or rating <= 2:
            recommendations.extend([
                "Review product matching criteria",
                "Analyze pricing competitiveness",
                "Investigate response time",
                "Check specification extraction accuracy"
            ])
        
        if feedback_type == 'win' and rating >= 4:
            recommendations.extend([
                "Document successful approach",
                "Use as training example",
                "Maintain current pricing strategy"
            ])
        
        return recommendations
    
    def get_performance_report(
        self,
        days: int = 30
    ) -> Dict[str, Any]:
        """
        Generate performance report
        
        Args:
            days: Number of days to include in report
            
        Returns:
            Performance report with metrics
        """
        cutoff_date = datetime.now() - timedelta(days=days)
        
        # Filter recent feedback
        recent_feedback = [
            f for f in self.feedback_history
            if f['timestamp'] >= cutoff_date
        ]
        
        if not recent_feedback:
            return {
                'period': f'Last {days} days',
                'total_feedback': 0,
                'message': 'No feedback data available'
            }
        
        # Calculate metrics
        total_feedback = len(recent_feedback)
        avg_rating = sum(f['rating'] for f in recent_feedback) / total_feedback
        
        # Match accuracy
        match_accuracies = [
            f['match_accuracy'] for f in recent_feedback
            if f['match_accuracy'] is not None
        ]
        avg_match_accuracy = (
            sum(match_accuracies) / len(match_accuracies)
            if match_accuracies else None
        )
        
        # Pricing accuracy
        pricing_accuracies = [
            f['pricing_accuracy'] for f in recent_feedback
            if f['pricing_accuracy'] is not None
        ]
        avg_pricing_accuracy = (
            sum(pricing_accuracies) / len(pricing_accuracies)
            if pricing_accuracies else None
        )
        
        # Response times
        response_times = [
            f['response_time'] for f in recent_feedback
            if f['response_time'] is not None
        ]
        avg_response_time = (
            sum(response_times) / len(response_times)
            if response_times else None
        )
        
        # Feedback type distribution
        feedback_types = defaultdict(int)
        for f in recent_feedback:
            feedback_types[f['feedback_type']] += 1
        
        # Win rate
        total_outcomes = (
            feedback_types.get('win', 0) + 
            feedback_types.get('loss', 0)
        )
        win_rate = (
            (feedback_types.get('win', 0) / total_outcomes * 100)
            if total_outcomes > 0 else None
        )
        
        return {
            'period': f'Last {days} days',
            'total_feedback': total_feedback,
            'average_rating': round(avg_rating, 2),
            'win_rate': round(win_rate, 2) if win_rate else None,
            'metrics': {
                'match_accuracy': (
                    round(avg_match_accuracy, 2)
                    if avg_match_accuracy else None
                ),
                'pricing_accuracy': (
                    round(avg_pricing_accuracy, 2)
                    if avg_pricing_accuracy else None
                ),
                'response_time': (
                    round(avg_response_time, 2)
                    if avg_response_time else None
                )
            },
            'feedback_distribution': dict(feedback_types),
            'trends': self._calculate_trends(recent_feedback)
        }
    
    def _calculate_trends(self, feedback_list: List[Dict]) -> Dict[str, str]:
        """Calculate performance trends"""
        if len(feedback_list) < 2:
            return {'status': 'insufficient_data'}
        
        # Split into first and second half
        mid = len(feedback_list) // 2
        first_half = feedback_list[:mid]
        second_half = feedback_list[mid:]
        
        # Compare average ratings
        avg_first = sum(f['rating'] for f in first_half) / len(first_half)
        avg_second = sum(f['rating'] for f in second_half) / len(second_half)
        
        rating_change = avg_second - avg_first
        
        if rating_change > 0.5:
            rating_trend = 'improving'
        elif rating_change < -0.5:
            rating_trend = 'declining'
        else:
            rating_trend = 'stable'
        
        return {
            'rating_trend': rating_trend,
            'rating_change': round(rating_change, 2),
            'interpretation': self._interpret_trend(rating_trend, rating_change)
        }
    
    def _interpret_trend(self, trend: str, change: float) -> str:
        """Interpret trend for recommendations"""
        if trend == 'improving':
            return f"Performance improving (+{change:.2f}). Continue current approach."
        elif trend == 'declining':
            return f"Performance declining ({change:.2f}). Immediate review needed."
        else:
            return "Performance stable. Monitor for changes."
    
    def get_common_issues(self, limit: int = 5) -> List[Dict[str, Any]]:
        """
        Get most common issues from feedback
        
        Args:
            limit: Maximum number of issues to return
            
        Returns:
            List of common issues with frequency
        """
        issue_keywords = defaultdict(int)
        
        for feedback in self.feedback_history:
            if feedback['comments']:
                comments_lower = feedback['comments'].lower()
                
                # Track issues
                if 'slow' in comments_lower or 'delayed' in comments_lower:
                    issue_keywords['slow_response'] += 1
                
                if 'wrong' in comments_lower or 'incorrect' in comments_lower:
                    issue_keywords['accuracy_issues'] += 1
                
                if 'expensive' in comments_lower or 'price' in comments_lower:
                    issue_keywords['pricing_concerns'] += 1
                
                if 'missing' in comments_lower or 'incomplete' in comments_lower:
                    issue_keywords['incomplete_data'] += 1
        
        # Sort by frequency
        sorted_issues = sorted(
            issue_keywords.items(),
            key=lambda x: x[1],
            reverse=True
        )[:limit]
        
        return [
            {
                'issue': issue,
                'frequency': count,
                'percentage': round(
                    (count / len(self.feedback_history)) * 100, 2
                )
            }
            for issue, count in sorted_issues
        ]
    
    def suggest_improvements(self) -> List[Dict[str, Any]]:
        """Suggest improvements based on accumulated feedback"""
        suggestions = []
        
        # Get performance report
        report = self.get_performance_report(days=30)
        
        if report['total_feedback'] == 0:
            return [{'suggestion': 'Collect more feedback for analysis'}]
        
        # Check average rating
        if report['average_rating'] < 3.5:
            suggestions.append({
                'area': 'Overall Performance',
                'issue': 'Low average rating',
                'suggestion': 'Comprehensive review of all components needed',
                'priority': 'high'
            })
        
        # Check match accuracy
        if report['metrics']['match_accuracy']:
            if report['metrics']['match_accuracy'] < 0.75:
                suggestions.append({
                    'area': 'Product Matching',
                    'issue': 'Low match accuracy',
                    'suggestion': 'Improve matching algorithms and product database',
                    'priority': 'high'
                })
        
        # Check pricing accuracy
        if report['metrics']['pricing_accuracy']:
            if report['metrics']['pricing_accuracy'] < 0.80:
                suggestions.append({
                    'area': 'Pricing',
                    'issue': 'Pricing accuracy below target',
                    'suggestion': 'Review cost calculation formulas and market data',
                    'priority': 'medium'
                })
        
        # Check response time
        if report['metrics']['response_time']:
            if report['metrics']['response_time'] > 180:  # 3 minutes
                suggestions.append({
                    'area': 'Performance',
                    'issue': 'Slow response time',
                    'suggestion': 'Optimize agent execution and caching strategies',
                    'priority': 'medium'
                })
        
        # Check win rate
        if report['win_rate'] and report['win_rate'] < 50:
            suggestions.append({
                'area': 'Business Performance',
                'issue': 'Low win rate',
                'suggestion': 'Analyze lost bids and adjust pricing strategy',
                'priority': 'high'
            })
        
        return suggestions if suggestions else [
            {'suggestion': 'Performance metrics are healthy. Continue monitoring.'}
        ]
