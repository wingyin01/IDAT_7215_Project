#!/usr/bin/env python3
"""
Test the Enhanced Rule Engine
Shows how it handles scenarios with manual rules, auto rules, and fallback
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from engine.enhanced_rule_engine import EnhancedRuleEngine
from engine.document_analyzer import DocumentAnalyzer
from knowledge_base.json_loader import ALL_ORDINANCES

def test_scenario(engine, analyzer, description, query_text):
    """Test a single scenario"""
    print("\n" + "=" * 80)
    print(f"TEST: {description}")
    print("=" * 80)
    print(f"Query: {query_text}")
    print()
    
    # Analyze document to extract facts
    analysis = analyzer.analyze_document(query_text)
    facts = set(analysis['facts'])
    
    print(f"Extracted Facts: {facts}")
    print()
    
    # Run enhanced rule engine
    results = engine.analyze(facts, query_text)
    
    # Explain results
    explanation = engine.explain_analysis(results)
    print(explanation)
    print()

def main():
    """Run comprehensive tests"""
    
    print("\n" + "=" * 80)
    print("ENHANCED RULE ENGINE TEST SUITE")
    print("=" * 80)
    
    # Initialize components
    print("\n🔄 Initializing Enhanced Rule Engine...")
    engine = EnhancedRuleEngine(ALL_ORDINANCES, use_auto_rules=True)
    
    print("🔄 Initializing Document Analyzer...")
    analyzer = DocumentAnalyzer()
    print()
    
    # Test scenarios
    test_cases = [
        {
            'description': '1. Theft (Manual Rule Should Match)',
            'query': 'Person dishonestly stole a laptop worth HK$5,000 from an office. '
                     'The laptop belonged to the company. He kept it and never returned it.'
        },
        {
            'description': '2. Assault (Manual Rule Should Match)',
            'query': 'Person punched another person in the face causing a black eye and bleeding. '
                     'The victim did not consent to being hit.'
        },
        {
            'description': '3. Smoking in Public (Manual Rule Should Match)',
            'query': 'Person was smoking a cigarette in a public park where smoking is prohibited.'
        },
        {
            'description': '4. Drug Possession (Manual Rule Should Match)',
            'query': 'Person was found with 10 grams of heroin in his pocket. '
                     'He admitted to possessing the dangerous drug.'
        },
        {
            'description': '5. Employment Dispute (Auto Rule or Fallback)',
            'query': 'Employer dismissed employee without notice after 3 years of employment. '
                     'Employee had no serious misconduct. Is employee entitled to severance pay?'
        },
        {
            'description': '6. Property/Landlord Issue (Auto Rule or Fallback)',
            'query': 'Landlord is refusing to return security deposit after tenant moved out. '
                     'Apartment had no damage and was left clean.'
        },
        {
            'description': '7. Company Registration (Likely Fallback)',
            'query': 'Can a person on a work visa register a company in Hong Kong? '
                     'What are the requirements and restrictions?'
        },
        {
            'description': '8. Tax Question (Likely Fallback)',
            'query': 'What are the tax obligations for a freelancer earning income from '
                     'overseas clients while residing in Hong Kong?'
        },
        {
            'description': '9. Complex Multi-Issue Scenario',
            'query': 'Person broke into a building at night, stole computers worth HK$50,000, '
                     'and when confronted by security guard, he punched the guard causing injury. '
                     'He had a prior conviction for theft in 2019.'
        },
        {
            'description': '10. Completely Out of Scope',
            'query': 'What is the best recipe for Hong Kong style milk tea?'
        }
    ]
    
    # Run all tests
    for test_case in test_cases:
        test_scenario(
            engine, 
            analyzer, 
            test_case['description'], 
            test_case['query']
        )
    
    # Print final statistics
    print("\n" + "=" * 80)
    print("TEST SUITE COMPLETE")
    print("=" * 80)
    engine.print_statistics()
    
    # Analysis
    stats = engine.get_statistics()
    print("\n" + "=" * 80)
    print("COVERAGE ANALYSIS")
    print("=" * 80)
    print(f"Manual Rules Handled: {stats['manual_rule_matches']} queries "
          f"({stats['manual_coverage']:.1f}%)")
    print(f"Auto Rules Handled: {stats['auto_rule_matches']} queries "
          f"({stats['auto_coverage']:.1f}%)")
    print(f"Fallback Required: {stats['fallback_searches']} queries "
          f"({stats['fallback_rate']:.1f}%)")
    print()
    
    # Recommendations
    print("=" * 80)
    print("RECOMMENDATIONS")
    print("=" * 80)
    
    if stats['manual_coverage'] < 50:
        print("⚠️  Manual rules cover <50% of queries.")
        print("   → Add more manual rules for common scenarios")
    else:
        print("✅ Manual rules provide good coverage")
    
    if stats['auto_coverage'] > 0:
        print(f"✅ Auto-generated rules successfully handled {stats['auto_rule_matches']} queries")
    else:
        print("⚠️  Auto-generated rules not being used")
        print("   → Check if auto rule generation is enabled")
    
    if stats['fallback_rate'] > 30:
        print(f"⚠️  High fallback rate ({stats['fallback_rate']:.1f}%)")
        print("   → Consider generating more auto rules")
        print("   → Or recommend RAG mode for uncovered scenarios")
    else:
        print("✅ Fallback rate is acceptable")
    
    print("=" * 80)
    print()


if __name__ == '__main__':
    main()
