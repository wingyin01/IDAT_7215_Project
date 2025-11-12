"""
Case Analytics - Extract Patterns from Real Criminal Cases
Analyzes 29 real Court of Appeal cases to derive sentencing patterns
"""

import sys
from pathlib import Path
import re

sys.path.insert(0, str(Path(__file__).parent.parent))

from knowledge_base import all_cases_database

class CaseAnalytics:
    """Analyzes real case data to derive patterns for risk assessment"""
    
    def __init__(self):
        self.cases = all_cases_database.ALL_CASES
        self.patterns = self._analyze_patterns()
    
    def _analyze_patterns(self):
        """Analyze all cases to extract patterns"""
        patterns = {
            'total_cases': len(self.cases),
            'by_keyword': {},
            'sentencing_ranges': {},
            'appeal_outcomes': {
                'dismissed': 0,
                'allowed': 0,
                'reduced': 0,
                'total': 0
            }
        }
        
        for case in self.cases:
            # Categorize by keywords
            for keyword in case.keywords:
                if keyword not in patterns['by_keyword']:
                    patterns['by_keyword'][keyword] = []
                patterns['by_keyword'][keyword].append(case)
            
            # Analyze outcomes
            outcome_lower = case.outcome.lower()
            patterns['appeal_outcomes']['total'] += 1
            
            if 'dismissed' in outcome_lower:
                patterns['appeal_outcomes']['dismissed'] += 1
            elif 'allowed' in outcome_lower:
                patterns['appeal_outcomes']['allowed'] += 1
            elif 'reduced' in outcome_lower:
                patterns['appeal_outcomes']['reduced'] += 1
            
            # Extract sentence patterns
            sentence_years = self._extract_years(case.sentence)
            sentence_months = self._extract_months(case.sentence)
            
            if sentence_years or sentence_months:
                total_months = (sentence_years or 0) * 12 + (sentence_months or 0)
                for keyword in case.keywords:
                    if keyword not in patterns['sentencing_ranges']:
                        patterns['sentencing_ranges'][keyword] = []
                    if total_months > 0:
                        patterns['sentencing_ranges'][keyword].append(total_months)
        
        # Calculate averages
        for keyword in patterns['sentencing_ranges']:
            sentences = patterns['sentencing_ranges'][keyword]
            if sentences:
                patterns['sentencing_ranges'][keyword] = {
                    'min': min(sentences),
                    'avg': sum(sentences) / len(sentences),
                    'max': max(sentences),
                    'count': len(sentences)
                }
        
        return patterns
    
    def _extract_years(self, text):
        """Extract years from sentence text"""
        if not text:
            return None
        match = re.search(r'(\d+)\s*years?', text, re.I)
        return int(match.group(1)) if match else None
    
    def _extract_months(self, text):
        """Extract months from sentence text"""
        if not text:
            return None
        match = re.search(r'(\d+)\s*months?', text, re.I)
        return int(match.group(1)) if match else None
    
    def get_sentence_range(self, offense_keywords):
        """
        Get typical sentence range for offense type
        
        Args:
            offense_keywords: List of keywords (e.g., ['drug', 'trafficking'])
        
        Returns:
            dict: Sentence range with confidence
        """
        ranges = []
        
        for keyword in offense_keywords:
            if keyword in self.patterns['sentencing_ranges']:
                ranges.append(self.patterns['sentencing_ranges'][keyword])
        
        if not ranges:
            return None
        
        # Combine ranges
        all_mins = [r['min'] for r in ranges]
        all_avgs = [r['avg'] for r in ranges]
        all_maxs = [r['max'] for r in ranges]
        total_cases = sum(r['count'] for r in ranges)
        
        return {
            'low_months': min(all_mins),
            'typical_months': sum(all_avgs) / len(all_avgs),
            'high_months': max(all_maxs),
            'based_on_cases': total_cases,
            'confidence': min(total_cases * 20, 80)  # More cases = higher confidence
        }
    
    def get_appeal_success_rate(self):
        """Calculate appeal success rate from real data"""
        outcomes = self.patterns['appeal_outcomes']
        if outcomes['total'] == 0:
            return 0
        
        # Appeals allowed or sentence reduced = success
        successes = outcomes['allowed'] + outcomes['reduced']
        return (successes / outcomes['total']) * 100
    
    def get_statistics(self):
        """Get overall statistics"""
        return {
            'total_cases': self.patterns['total_cases'],
            'offense_types': len(self.patterns['by_keyword']),
            'appeal_success_rate': self.get_appeal_success_rate(),
            'sentencing_data_available': len(self.patterns['sentencing_ranges'])
        }

# Singleton instance
_analytics = None

def get_analytics():
    """Get or create analytics instance"""
    global _analytics
    if _analytics is None:
        _analytics = CaseAnalytics()
    return _analytics

if __name__ == '__main__':
    analytics = get_analytics()
    stats = analytics.get_statistics()
    
    print("=" * 80)
    print("CASE ANALYTICS - REAL DATA ANALYSIS")
    print("=" * 80)
    print()
    print(f"Total cases analyzed: {stats['total_cases']}")
    print(f"Offense types with data: {stats['offense_types']}")
    print(f"Appeal success rate: {stats['appeal_success_rate']:.1f}%")
    print()
    
    print("Sentencing Ranges by Offense Type:")
    print("-" * 80)
    for keyword, data in analytics.patterns['sentencing_ranges'].items():
        print(f"\n{keyword.upper()}:")
        print(f"  Range: {data['min']}-{data['max']} months")
        print(f"  Typical: {data['avg']:.1f} months")
        print(f"  Based on: {data['count']} cases")
    print()
    print("=" * 80)
