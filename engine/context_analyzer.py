"""
Context Analyzer - Proportionality and Severity Assessment
Provides realistic legal advice considering context, value, and circumstances
"""

import re

class ContextAnalyzer:
    """Analyzes context and provides proportionality assessment"""
    
    def __init__(self):
        pass
    
    def extract_amount(self, text):
        """Extract monetary amount from text"""
        # Look for HK$ or $ amounts
        patterns = [
            r'HK\$\s*([\d,]+)',
            r'\$\s*([\d,]+)',
            r'worth\s+HK\$\s*([\d,]+)',
            r'value.*?HK\$\s*([\d,]+)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.I)
            if match:
                amount_str = match.group(1).replace(',', '')
                try:
                    return int(amount_str)
                except:
                    return None
        
        # Look for small value items (candy, chocolate, etc.)
        small_items = ['candy', 'chocolate', 'snack', 'gum', 'drink']
        for item in small_items:
            if item in text.lower():
                return 10  # Estimate ~HK$10 for small items
        
        return None
    
    def assess_theft_severity(self, text, amount=None):
        """
        Assess severity of theft based on context
        
        Returns:
            dict: Severity assessment with advice
        """
        if amount is None:
            amount = self.extract_amount(text)
        
        assessment = {
            'amount': amount,
            'severity': 'unknown',
            'category': '',
            'considerations': [],
            'mitigation_factors': [],
            'practical_advice': []
        }
        
        # Determine severity based on value
        if amount is not None:
            if amount < 100:
                assessment['severity'] = 'petty'
                assessment['category'] = 'Petty Theft'
                assessment['considerations'].append(
                    f"Low value amount (HK${amount})"
                )
                assessment['considerations'].append(
                    "Prosecution may exercise discretion for trivial amounts"
                )
                assessment['mitigation_factors'].append("Minimal financial loss")
                assessment['practical_advice'].append(
                    "Return the item immediately if possible"
                )
                assessment['practical_advice'].append(
                    "First-time offenders may receive a caution instead of prosecution"
                )
            elif amount < 5000:
                assessment['severity'] = 'minor'
                assessment['category'] = 'Minor Theft'
                assessment['considerations'].append(
                    f"Moderate value amount (HK${amount})"
                )
                assessment['considerations'].append(
                    "Likely to result in prosecution if reported"
                )
                assessment['mitigation_factors'].append("Relatively low value")
                assessment['practical_advice'].append(
                    "Seek legal counsel immediately"
                )
                assessment['practical_advice'].append(
                    "Consider restitution as mitigation"
                )
            else:
                assessment['severity'] = 'serious'
                assessment['category'] = 'Serious Theft'
                assessment['considerations'].append(
                    f"High value amount (HK${amount:,})"
                )
                assessment['considerations'].append(
                    "Prosecution is highly likely"
                )
                assessment['considerations'].append(
                    "May face custodial sentence if convicted"
                )
                assessment['practical_advice'].append(
                    "Engage a qualified criminal defense lawyer immediately"
                )
                assessment['practical_advice'].append(
                    "Do not make any statements without legal representation"
                )
        
        # Check for aggravating factors
        aggravating = []
        if re.search(r'\bweapon|knife|gun|force|threat|violence\b', text, re.I):
            aggravating.append("Use of weapons/force (may constitute robbery, not theft)")
        if re.search(r'\bnight|darkness|evening\b', text, re.I):
            aggravating.append("Committed at night")
        if re.search(r'\bbreak|enter|trespass\b', text, re.I):
            aggravating.append("Involved breaking and entering (may constitute burglary)")
        
        if aggravating:
            assessment['aggravating_factors'] = aggravating
        
        # Check for mitigating factors
        if re.search(r'\badmit|confess|remorse|sorry\b', text, re.I):
            assessment['mitigation_factors'].append("Admission/confession")
        if re.search(r'\bfirst.{0,10}offence|no.{0,10}prior|clean record\b', text, re.I):
            assessment['mitigation_factors'].append("No prior criminal record")
        if re.search(r'\breturn|give.{0,10}back|restore\b', text, re.I):
            assessment['mitigation_factors'].append("Attempted to return items")
        
        return assessment
    
    def generate_contextual_advice(self, offense_type, text, assessment):
        """
        Generate contextual legal advice based on assessment
        
        Args:
            offense_type: Type of offense (e.g., 'theft')
            text: Original text
            assessment: Output from assess_theft_severity()
        
        Returns:
            str: Formatted advice
        """
        advice_parts = []
        
        # Header
        advice_parts.append(f"=== CONTEXTUAL LEGAL ANALYSIS ===\n")
        
        # Offense identification
        if offense_type == 'theft':
            advice_parts.append("**OFFENSE IDENTIFIED**: Theft under Cap. 210, Theft Ordinance\n")
            advice_parts.append("**LEGAL BASIS**: Cap. 210, Section 2 - Basic definition of theft\n")
            advice_parts.append("**MAXIMUM PENALTY**: 10 years imprisonment (Cap. 210, s.9)\n")
        
        # Severity assessment
        if assessment['severity'] != 'unknown':
            advice_parts.append(f"\n**SEVERITY ASSESSMENT**: {assessment['category']}\n")
            
            if assessment.get('amount'):
                advice_parts.append(f"- Stolen property value: HK${assessment['amount']}\n")
            
            for consideration in assessment['considerations']:
                advice_parts.append(f"- {consideration}\n")
        
        # Aggravating factors
        if assessment.get('aggravating_factors'):
            advice_parts.append("\n**⚠️ AGGRAVATING FACTORS**:\n")
            for factor in assessment['aggravating_factors']:
                advice_parts.append(f"- {factor}\n")
        
        # Mitigating factors
        if assessment.get('mitigation_factors'):
            advice_parts.append("\n**✓ MITIGATING FACTORS**:\n")
            for factor in assessment['mitigation_factors']:
                advice_parts.append(f"- {factor}\n")
        
        # Practical advice
        if assessment.get('practical_advice'):
            advice_parts.append("\n**PRACTICAL ADVICE**:\n")
            for advice in assessment['practical_advice']:
                advice_parts.append(f"- {advice}\n")
        
        # Important notes
        advice_parts.append("\n**IMPORTANT NOTES**:\n")
        advice_parts.append("- Theft is a criminal offense regardless of value\n")
        advice_parts.append("- A criminal conviction will result in a permanent record\n")
        advice_parts.append("- Even minor theft can affect employment, travel, and immigration status\n")
        
        return ''.join(advice_parts)

# Singleton instance
_context_analyzer = None

def get_context_analyzer():
    """Get or create context analyzer instance"""
    global _context_analyzer
    if _context_analyzer is None:
        _context_analyzer = ContextAnalyzer()
    return _context_analyzer

