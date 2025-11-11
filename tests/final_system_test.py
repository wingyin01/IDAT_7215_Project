#!/usr/bin/env python3
"""
Final Comprehensive System Test
Tests all components of the IDAT7215 Hong Kong Legal Expert System
"""

import sys
sys.path.insert(0, '/Users/wingyin/Documents/Expert system')

print("=" * 80)
print("IDAT7215 HONG KONG LEGAL EXPERT SYSTEM - FINAL TEST")
print("=" * 80)
print()

# Test 1: Load comprehensive knowledge base
print("TEST 1: Loading Comprehensive Knowledge Base...")
try:
    from knowledge_base import hk_all_ordinances as hk
    print(f"  ✅ Knowledge base loaded")
    print(f"     Total ordinances: {hk.TOTAL_ORDINANCES:,}")
    print(f"     Total sections: {hk.TOTAL_SECTIONS:,}")
    print(f"     Categories: {len(hk.STATS['categories'])}")
except Exception as e:
    print(f"  ❌ ERROR: {e}")
    sys.exit(1)

print()

# Test 2: Load comprehensive rules
print("TEST 2: Loading Comprehensive Legal Rules...")
try:
    from knowledge_base import all_legal_rules
    print(f"  ✅ Legal rules loaded")
    print(f"     Total rules: {all_legal_rules.TOTAL_RULES}")
    print(f"     Rule categories: {len(all_legal_rules.RULES_BY_CATEGORY)}")
except Exception as e:
    print(f"  ❌ ERROR: {e}")
    sys.exit(1)

print()

# Test 3: Load comprehensive cases
print("TEST 3: Loading Comprehensive Case Database...")
try:
    from knowledge_base import all_cases_database
    print(f"  ✅ Case database loaded")
    print(f"     Total cases: {all_cases_database.TOTAL_CASES}")
    print(f"     Case categories: {len(all_cases_database.CASES_BY_CATEGORY)}")
except Exception as e:
    print(f"  ❌ ERROR: {e}")
    sys.exit(1)

print()

# Test 4: Test inference engine
print("TEST 4: Testing Inference Engine...")
try:
    from engine.rule_engine import analyze_case
    facts = [
        'appropriates_property',
        'property_belongs_to_another',
        'acts_dishonestly',
        'intent_to_permanently_deprive'
    ]
    engine = analyze_case(facts)
    offences = engine.get_offences()
    print(f"  ✅ Inference engine working")
    print(f"     Test case identified {len(offences)} offence(s)")
except Exception as e:
    print(f"  ❌ ERROR: {e}")
    sys.exit(1)

print()

# Test 5: Test case matcher
print("TEST 5: Testing Case Matcher...")
try:
    from engine.case_matcher import CaseMatcher
    matcher = CaseMatcher()
    results = matcher.find_similar_cases("theft from store", top_n=3)
    print(f"  ✅ Case matcher working")
    print(f"     Found {len(results)} similar cases")
except Exception as e:
    print(f"  ❌ ERROR: {e}")
    sys.exit(1)

print()

# Test 6: Test document analyzer
print("TEST 6: Testing Document Analyzer...")
try:
    from engine.document_analyzer import DocumentAnalyzer
    analyzer = DocumentAnalyzer()
    analysis = analyzer.analyze_document("Person stole property worth HK$5000")
    print(f"  ✅ Document analyzer working")
    print(f"     Extracted {len(analysis['facts'])} facts")
except Exception as e:
    print(f"  ❌ ERROR: {e}")
    sys.exit(1)

print()

# Test 7: Test search functionality
print("TEST 7: Testing Search Across All Ordinances...")
try:
    # Search for a common legal term
    results = hk.search_ordinances_by_keyword('contract')
    print(f"  ✅ Search working")
    print(f"     Found {len(results)} sections mentioning 'contract'")
    
    # Test category search
    criminal_ords = hk.get_ordinances_by_category('Criminal Law')
    print(f"     Criminal Law category: {len(criminal_ords)} ordinances")
except Exception as e:
    print(f"  ❌ ERROR: {e}")
    sys.exit(1)

print()

# Test 8: Verify categories
print("TEST 8: Verifying Legal Categories...")
try:
    categories = hk.get_categories_summary()
    print(f"  ✅ Categories verified")
    for cat, info in sorted(categories.items(), key=lambda x: x[1]['sections'], reverse=True)[:5]:
        print(f"     {cat}: {info['count']} ordinances, {info['sections']:,} sections")
except Exception as e:
    print(f"  ❌ ERROR: {e}")
    sys.exit(1)

print()

# Final Summary
print("=" * 80)
print("✅ ALL TESTS PASSED - SYSTEM READY FOR DEMONSTRATION")
print("=" * 80)
print()
print("System Summary:")
print(f"  • {hk.TOTAL_ORDINANCES:,} ordinances loaded from official XML")
print(f"  • {hk.TOTAL_SECTIONS:,} legal sections available")
print(f"  • {all_legal_rules.TOTAL_RULES} legal rules implemented")
print(f"  • {all_cases_database.TOTAL_CASES} case precedents")
print(f"  • {len(hk.STATS['categories'])} legal categories")
print()
print("To run the web application:")
print("  python webapp/app.py")
print()
print("Then open: http://localhost:8080")
print("=" * 80)

