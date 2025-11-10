"""
Explanation Module
Generates human-readable explanations of legal reasoning
Note: Main explanation functionality is integrated into InferenceEngine.explain()
This module provides additional formatting and explanation utilities
"""

def format_ordinance_reference(chapter, section):
    """Format an ordinance reference"""
    return f"Cap. {chapter}, s. {section}"

def format_offence_name(offence_code):
    """Format an offence code into readable name"""
    return offence_code.replace('guilty_of_', '').replace('_', ' ').title()

def format_fact(fact_code):
    """Format a fact code into readable text"""
    return fact_code.replace('_', ' ').capitalize()

def generate_legal_advice_disclaimer():
    """Generate standard legal advice disclaimer"""
    return """
IMPORTANT DISCLAIMER:
This system provides general information about Hong Kong criminal law based on 
legislative provisions and case precedents. It is NOT a substitute for professional 
legal advice. For specific legal issues, you should:

1. Consult a qualified Hong Kong solicitor or barrister
2. Contact the Duty Lawyer Service (Tel: 2537 7677)
3. Visit the Legal Aid Department if eligible

The analysis provided is based on the facts as presented and may change if 
additional information becomes available.
"""

def format_case_citation(case_name, year, court):
    """Format a case citation"""
    return f"{case_name} ({year}) {court}"

# Export from inference engine for convenience
from engine.rule_engine import InferenceEngine

__all__ = ['format_ordinance_reference', 'format_offence_name', 'format_fact', 
           'generate_legal_advice_disclaimer', 'format_case_citation', 'InferenceEngine']

