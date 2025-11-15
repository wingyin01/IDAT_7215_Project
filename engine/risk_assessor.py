"""
Risk Assessment & Prediction Module
Provides accurate predictions based on real case data and legal rules
"""

import sys
from pathlib import Path
import re

sys.path.insert(0, str(Path(__file__).parent.parent))

from engine.case_analytics import get_analytics

class RiskAssessor:
    """Assesses legal risks and predicts outcomes based on case data and rules"""
    
    # Base prosecution rates by offense severity
    PROSECUTION_RATES = {
        # Regulatory offenses (fines only)
        'smoking': 25,          # Cap. 371: Fixed penalty
        'littering': 20,        # Fixed penalty
        'spitting': 15,         # Fixed penalty
        'noise': 10,            # Usually warning first
        
        # Animal offenses
        'animal_cruelty': 80,   # Cap. 169: Serious offense
        
        # Theft offenses
        'petty_theft': 30,      # <HK$100
        'minor_theft': 70,      # HK$100-5000
        'serious_theft': 95,    # >HK$5000
        'shoplifting': 60,      # Store theft
        'burglary': 95,         # Breaking + theft
        'robbery': 98,          # Force + theft
        
        # Assault offenses
        'assault_minor': 75,    # No serious injury
        'assault_serious': 95,  # GBH
        
        # Drug offenses
        'drug_possession': 85,  # Personal use amounts
        'drug_trafficking': 99, # Commercial amounts
        
        # Other serious crimes
        'fraud': 80,            # Dishonesty offenses
        'sexual': 95,           # Sexual offenses
        'murder': 99,           # Homicide
        'manslaughter': 98,     # Unlawful killing
    }
    
    # Statutory penalties (months, 0 = fine only)
    STATUTORY_PENALTIES = {
        # Regulatory offenses (FINES ONLY, NO PRISON)
        'smoking': {'max': 0, 'typical': 0, 'fine': '1,500-5,000', 'fine_only': True},
        'littering': {'max': 0, 'typical': 0, 'fine': '1,500-25,000', 'fine_only': True},
        'spitting': {'max': 0, 'typical': 0, 'fine': '1,500-10,000', 'fine_only': True},
        'noise': {'max': 0, 'typical': 0, 'fine': 'up to 10,000', 'fine_only': True},
        
        # Animal cruelty
        'animal_cruelty': {'max': 36, 'typical': 3-12, 'fine': 'up to 200,000'},  # Cap. 169: 3 years + fine
        
        # Theft offenses
        'theft': {'max': 120, 'typical': 6-24},  # Cap. 210: Max 10 years
        'petty_theft': {'max': 12, 'typical': 0-3},  # Usually fine/community service
        'minor_theft': {'max': 24, 'typical': 3-12},  # Probation to short sentence
        'serious_theft': {'max': 120, 'typical': 12-48},  # Prison likely
        'robbery': {'max': 168, 'typical': 36-84},  # Cap. 200: Max 14 years
        'burglary': {'max': 168, 'typical': 24-60},  # Cap. 211: Max 14 years
        
        # Assault offenses
        'assault_abh': {'max': 36, 'typical': 3-12},  # Cap. 212: Max 3 years
        'assault_gbh': {'max': 84, 'typical': 24-60},  # Cap. 212: Max 7 years
        
        # Drug offenses
        'drug_trafficking': {'max': 9999, 'typical': 60-180},  # Cap. 134: Life
        
        # Other serious crimes
        'fraud': {'max': 168, 'typical': 12-48},  # Cap. 210: Max 14 years
        'murder': {'max': 9999, 'mandatory': 9999},  # Life imprisonment
    }
    
    def __init__(self):
        self.analytics = get_analytics()
    
    def assess_prosecution_likelihood(self, offense_type, factors):
        """
        Calculate likelihood of prosecution
        
        Args:
            offense_type: Type of offense
            factors: Dict of relevant factors
        
        Returns:
            dict: Prosecution assessment
        """
        # Start with base rate
        base_rate = self.PROSECUTION_RATES.get(offense_type, 70)
        
        likelihood = base_rate
        adjustments = []
        
        # Evidence factors
        if factors.get('cctv_evidence'):
            likelihood += 15
            adjustments.append(('+15%', 'CCTV evidence available'))
        
        if factors.get('caught_red_handed'):
            likelihood += 20
            adjustments.append(('+20%', 'Caught in the act'))
        
        if factors.get('witness_testimony'):
            likelihood += 10
            adjustments.append(('+10%', 'Witness testimony'))
        
        if factors.get('confession'):
            likelihood += 5
            adjustments.append(('+5%', 'Confession obtained'))
        
        # Offender factors
        if factors.get('prior_conviction'):
            likelihood += 10
            adjustments.append(('+10%', 'Prior criminal conviction'))
        
        if factors.get('first_offense'):
            likelihood -= 10
            adjustments.append(('-10%', 'First offense'))
        
        # Victim factors
        if factors.get('victim_complaint'):
            likelihood += 15
            adjustments.append(('+15%', 'Victim filed complaint'))
        
        if factors.get('no_victim_complaint'):
            likelihood -= 20
            adjustments.append(('-20%', 'No victim complaint'))
        
        # Value/severity factors
        if factors.get('high_value'):
            likelihood += 15
            adjustments.append(('+15%', 'High value involved'))
        
        if factors.get('low_value'):
            likelihood -= 15
            adjustments.append(('-15%', 'Low value (petty offense)'))
        
        # Remorse/restitution
        if factors.get('restitution_made'):
            likelihood -= 10
            adjustments.append(('-10%', 'Restitution made to victim'))
        
        # Cap at 5-99%
        likelihood = max(5, min(99, likelihood))
        
        return {
            'likelihood': round(likelihood),
            'category': self._categorize_likelihood(likelihood),
            'base_rate': base_rate,
            'adjustments': adjustments
        }
    
    def predict_sentence(self, offense_type, factors, keywords=None):
        """
        Predict sentence range
        
        Args:
            offense_type: Type of offense
            factors: Relevant factors
            keywords: Keywords for case data lookup
        
        Returns:
            dict: Sentence prediction
        """
        # Try to get real case data first
        case_based = None
        if keywords:
            case_based = self.analytics.get_sentence_range(keywords)
        
        # Get statutory range
        statutory = self.STATUTORY_PENALTIES.get(offense_type, {'max': 120, 'typical': 6-36})
        
        # Check if this is a fine-only offense
        if statutory.get('fine_only', False):
            return {
                'low_months': 0,
                'typical_months': 0,
                'high_months': 0,
                'fine_range': statutory.get('fine', 'Unknown'),
                'confidence': 95,
                'basis': f"Fixed penalty offense under Hong Kong law (HK${statutory.get('fine', 'Unknown')})",
                'adjustments': ['Fine-only offense - no imprisonment'],
                'is_fine_only': True
            }
        
        # If we have real case data, use it
        if case_based and case_based['based_on_cases'] > 0:
            low = case_based['low_months']
            typical = case_based['typical_months']
            high = case_based['high_months']
            confidence = case_based['confidence']
            basis = f"Based on {case_based['based_on_cases']} real cases from our database"
        else:
            # Use statutory penalties and rules
            if isinstance(statutory.get('typical'), range):
                low = statutory['typical'].start
                high = statutory['typical'].stop
                typical = (low + high) / 2
            else:
                low = 6
                typical = 18
                high = statutory['max']
            
            confidence = 50
            basis = "Based on statutory penalties and general sentencing guidelines"
        
        # Apply aggravating factors
        multiplier = 1.0
        adjustments = []
        
        if factors.get('weapon'):
            multiplier *= 1.5
            adjustments.append('Weapon used (+50%)')
        
        if factors.get('violence'):
            multiplier *= 1.3
            adjustments.append('Violence involved (+30%)')
        
        if factors.get('prior_conviction'):
            multiplier *= 1.3
            adjustments.append('Prior conviction (+30%)')
        
        if factors.get('planning'):
            multiplier *= 1.2
            adjustments.append('Premeditation (+20%)')
        
        if factors.get('vulnerable_victim'):
            multiplier *= 1.3
            adjustments.append('Vulnerable victim (+30%)')
        
        # Apply mitigating factors
        if factors.get('guilty_plea'):
            multiplier *= 0.67
            adjustments.append('Guilty plea (-33% discount)')
        
        if factors.get('remorse'):
            multiplier *= 0.9
            adjustments.append('Genuine remorse (-10%)')
        
        if factors.get('first_offense'):
            multiplier *= 0.85
            adjustments.append('First offense (-15%)')
        
        if factors.get('restitution'):
            multiplier *= 0.85
            adjustments.append('Restitution made (-15%)')
        
        # Apply multiplier
        low = int(low * multiplier)
        typical = int(typical * multiplier)
        high = int(high * multiplier)
        
        return {
            'low_months': low,
            'typical_months': typical,
            'high_months': high,
            'confidence': confidence,
            'basis': basis,
            'adjustments': adjustments
        }
    
    def predict_outcomes(self, offense_type, factors):
        """
        Predict case outcomes
        
        Returns:
            dict: Probability of various outcomes
        """
        # Base conviction rates
        conviction_base = {
            # Regulatory offenses
            'smoking': 90,          # Usually fixed penalty, high conviction if prosecuted
            'littering': 85,        # Similar
            'spitting': 80,         # Similar
            'noise': 70,            # Lower - harder to prove
            'animal_cruelty': 75,   # Moderate conviction rate
            
            # Theft offenses
            'petty_theft': 60,
            'minor_theft': 75,
            'serious_theft': 85,
            'robbery': 90,
            'burglary': 85,
            
            # Other serious crimes
            'drug_trafficking': 95,
            'assault_minor': 70,
            'assault_serious': 85,
            'fraud': 80,
            'murder': 90,
        }
        
        conviction_rate = conviction_base.get(offense_type, 75)
        
        # Adjust based on evidence
        if factors.get('strong_evidence'):
            conviction_rate = min(95, conviction_rate + 15)
        if factors.get('weak_evidence'):
            conviction_rate = max(30, conviction_rate - 20)
        
        # Custodial sentence likelihood
        custodial_base = {
            # Regulatory offenses (NEVER prison for first offense)
            'smoking': 0,           # FINE ONLY
            'littering': 0,         # FINE ONLY
            'spitting': 0,          # FINE ONLY
            'noise': 0,             # FINE ONLY
            'animal_cruelty': 40,   # Prison possible for serious cases
            
            # Theft offenses
            'petty_theft': 10,
            'minor_theft': 30,
            'serious_theft': 70,
            'robbery': 90,
            'burglary': 75,
            
            # Other serious crimes
            'drug_trafficking': 95,
            'assault_minor': 40,
            'assault_serious': 80,
            'fraud': 50,
            'murder': 100,
        }
        
        custodial = custodial_base.get(offense_type, 50)
        
        # Adjust for factors
        if factors.get('prior_conviction'):
            custodial += 20
        if factors.get('first_offense'):
            custodial -= 15
        if factors.get('guilty_plea'):
            custodial -= 10
        
        custodial = max(5, min(99, custodial))
        
        # Appeal success rate from real data
        appeal_success = self.analytics.get_appeal_success_rate()
        
        return {
            'conviction_likelihood': round(conviction_rate),
            'custodial_sentence': round(custodial),
            'non_custodial': round(100 - custodial),
            'appeal_success_rate': round(appeal_success),
        }
    
    def comprehensive_risk_assessment(self, text, context_assessment, offense_type='theft'):
        """
        Complete risk assessment combining all factors
        
        Args:
            text: Original text
            context_assessment: From ContextAnalyzer
            offense_type: Type of offense
        
        Returns:
            dict: Complete risk assessment
        """
        # Extract factors from text and context
        factors = self._extract_factors(text, context_assessment)
        
        # Detect specific offense type from text
        specific_offense = self._detect_offense_type(text, offense_type)
        
        # If it's theft, further classify by severity
        if specific_offense == 'theft':
            if context_assessment['severity'] == 'petty':
                specific_offense = 'petty_theft'
            elif context_assessment['severity'] == 'minor':
                specific_offense = 'minor_theft'
            elif context_assessment['severity'] == 'serious':
                specific_offense = 'serious_theft'
        
        # Get keywords for case data lookup
        keywords = []
        if 'drug' in text.lower():
            keywords.append('drug')
        if 'trafficking' in text.lower() or 'distribute' in text.lower():
            keywords.append('trafficking')
        if 'robbery' in text.lower() or 'rob' in text.lower():
            keywords.append('robbery')
        
        # Calculate assessments
        prosecution = self.assess_prosecution_likelihood(specific_offense, factors)
        sentence_pred = self.predict_sentence(specific_offense, factors, keywords)
        outcomes = self.predict_outcomes(specific_offense, factors)
        
        return {
            'prosecution': prosecution,
            'sentence_prediction': sentence_pred,
            'outcome_probabilities': outcomes,
            'factors_detected': factors,
            'risk_level': self._calculate_overall_risk(prosecution, sentence_pred, outcomes)
        }
    
    def _extract_factors(self, text, context):
        """Extract relevant factors from text"""
        text_lower = text.lower()
        
        factors = {}
        
        # Evidence
        factors['cctv_evidence'] = 'cctv' in text_lower or 'camera' in text_lower
        factors['witness_testimony'] = 'witness' in text_lower or 'saw' in text_lower
        factors['confession'] = 'admit' in text_lower or 'confess' in text_lower
        
        # Offender history
        factors['prior_conviction'] = 'prior' in text_lower or 'previous' in text_lower or 'convicted before' in text_lower
        factors['first_offense'] = 'first time' in text_lower or 'first offense' in text_lower or 'no prior' in text_lower
        
        # Aggravating
        factors['weapon'] = bool(re.search(r'weapon|knife|gun|firearm', text_lower))
        factors['violence'] = bool(re.search(r'violence|assault|attack|injur|harm', text_lower))
        factors['planning'] = bool(re.search(r'plan|premeditat|calculat', text_lower))
        factors['vulnerable_victim'] = bool(re.search(r'elderly|child|vulnerable|disabled', text_lower))
        
        # Mitigating
        factors['remorse'] = 'remorse' in text_lower or 'sorry' in text_lower or 'regret' in text_lower
        factors['guilty_plea'] = 'plead guilty' in text_lower or 'guilty plea' in text_lower
        factors['restitution'] = 'return' in text_lower or 'restitution' in text_lower or 'compensat' in text_lower
        
        # Value
        if context.get('amount'):
            if context['amount'] > 5000:
                factors['high_value'] = True
            elif context['amount'] < 100:
                factors['low_value'] = True
        
        # Evidence strength
        evidence_count = sum([
            factors.get('cctv_evidence', False),
            factors.get('witness_testimony', False),
            factors.get('confession', False)
        ])
        
        factors['strong_evidence'] = evidence_count >= 2
        factors['weak_evidence'] = evidence_count == 0
        
        return factors
    
    def _calculate_overall_risk(self, prosecution, sentence, outcomes):
        """Calculate overall risk level"""
        # Weighted risk score
        risk_score = (
            prosecution['likelihood'] * 0.3 +
            outcomes['conviction_likelihood'] * 0.3 +
            outcomes['custodial_sentence'] * 0.4
        )
        
        if risk_score > 80:
            return {'level': 'VERY HIGH', 'score': round(risk_score), 'color': '#e74c3c'}
        elif risk_score > 60:
            return {'level': 'HIGH', 'score': round(risk_score), 'color': '#f39c12'}
        elif risk_score > 40:
            return {'level': 'MODERATE', 'score': round(risk_score), 'color': '#f1c40f'}
        else:
            return {'level': 'LOW', 'score': round(risk_score), 'color': '#27ae60'}
    
    def _categorize_likelihood(self, percentage):
        """Categorize likelihood percentage"""
        if percentage > 80:
            return 'Very Likely'
        elif percentage > 60:
            return 'Likely'
        elif percentage > 40:
            return 'Possible'
        elif percentage > 20:
            return 'Unlikely'
        else:
            return 'Very Unlikely'
    
    def _detect_offense_type(self, text, default='theft'):
        """Detect offense type from text"""
        text_lower = text.lower()
        
        # Regulatory offenses
        if any(word in text_lower for word in ['smok', 'cigarette', 'cigar', 'tobacco', 'vap']):
            return 'smoking'
        if any(word in text_lower for word in ['litter', 'throw trash', 'threw rubbish']):
            return 'littering'
        if 'spit' in text_lower:
            return 'spitting'
        if any(word in text_lower for word in ['noise', 'loud music', 'noisy']):
            return 'noise'
        
        # Animal offenses
        if any(word in text_lower for word in ['kill', 'harm', 'abuse', 'torture', 'hurt', 'beat']):
            if any(word in text_lower for word in ['cat', 'dog', 'animal', 'pet', 'puppy', 'kitten']):
                return 'animal_cruelty'
        
        # Serious crimes
        if 'murder' in text_lower or 'kill' in text_lower and any(w in text_lower for w in ['person', 'man', 'woman', 'someone', 'people']):
            return 'murder'
        if 'rob' in text_lower and ('force' in text_lower or 'threat' in text_lower or 'weapon' in text_lower):
            return 'robbery'
        if any(word in text_lower for word in ['burgl', 'break in', 'broke in']):
            return 'burglary'
        if 'drug' in text_lower and any(w in text_lower for w in ['trafficking', 'dealing', 'distribute', 'sell']):
            return 'drug_trafficking'
        
        return default
    
    def format_months_to_text(self, months):
        """Convert months to readable text"""
        if months == 0:
            return "Fine only (no prison)"
        elif months >= 12:
            years = months / 12
            if years == int(years):
                return f"{int(years)} year{'s' if years > 1 else ''}"
            else:
                return f"{years:.1f} years"
        else:
            return f"{months} months"

# Singleton
_risk_assessor = None

def get_risk_assessor():
    """Get or create risk assessor"""
    global _risk_assessor
    if _risk_assessor is None:
        _risk_assessor = RiskAssessor()
    return _risk_assessor
