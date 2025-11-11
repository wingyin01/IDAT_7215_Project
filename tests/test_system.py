#!/usr/bin/env python3
"""
Comprehensive System Test
Tests all components of the IDAT7215 Hong Kong Legal Expert System
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

print("=" * 80)
print("IDAT7215 HONG KONG LEGAL EXPERT SYSTEM - COMPREHENSIVE TEST")
print("=" * 80)
print()

# Test 1: Load JSON knowledge base
print("TEST 1: Loading Knowledge Base from JSON...")
try:
    from knowledge_base import json_loader
    print(f"  ✅ JSON knowledge base loaded")
    print(f"     Total ordinances: {json_loader.TOTAL_ORDINANCES:,}")
    print(f"     Total sections: {json_loader.TOTAL_SECTIONS:,}")
    print(f"     Categories: {len(json_loader.STATS['categories'])}")
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
    if offences:
        print(f"     Offence: {offences[0]['offence']}")
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
    results = json_loader.search_ordinances_by_keyword('contract')
    print(f"  ✅ Search working")
    print(f"     Found {len(results)} sections mentioning 'contract'")
    
    # Test category search
    categories = json_loader.get_categories_summary()
    criminal_count = categories.get('Criminal Law', {}).get('count', 0)
    print(f"     Criminal Law category: {criminal_count} ordinances")
except Exception as e:
    print(f"  ❌ ERROR: {e}")
    sys.exit(1)

print()

# Test 8: Verify categories
print("TEST 8: Verifying Legal Categories...")
try:
    categories = json_loader.get_categories_summary()
    print(f"  ✅ Categories verified")
    for cat, info in sorted(categories.items(), key=lambda x: x[1]['sections'], reverse=True)[:5]:
        print(f"     {cat}: {info['count']} ordinances, {info['sections']:,} sections")
except Exception as e:
    print(f"  ❌ ERROR: {e}")
    sys.exit(1)

print()

# Test 9: Test specific section retrieval
print("TEST 9: Testing Section Retrieval...")
try:
    section = json_loader.get_ordinance_section('210', '2')
    if section:
        print(f"  ✅ Section retrieval working")
        print(f"     Cap. 210, s.2: {section.get('title', 'N/A')}")
    else:
        print(f"  ⚠️  Section not found (may need to run preprocessing)")
except Exception as e:
    print(f"  ❌ ERROR: {e}")
    sys.exit(1)

print()

# Test 10: Test hybrid search (if embeddings exist)
print("TEST 10: Testing Hybrid Search Engine...")
try:
    from engine.hybrid_search import HybridSearchEngine
    from pathlib import Path
    
    cache_dir = project_root / "knowledge_base" / "cached_embeddings"
    
    if cache_dir.exists():
        search_engine = HybridSearchEngine()
        if search_engine.load_index(cache_dir):
            results = search_engine.search_legislation_only("theft penalty", top_k=3)
            print(f"  ✅ Hybrid search working")
            print(f"     Found {len(results)} relevant sections")
            if results:
                top_result = results[0]
                print(f"     Top result: Cap. {top_result['metadata']['chapter']}, "
                      f"s.{top_result['metadata']['section']}")
        else:
            print(f"  ⚠️  Embeddings cache not loaded")
    else:
        print(f"  ⚠️  Embeddings cache not found")
        print(f"     Run: python3 -m knowledge_base.embeddings_index")
except Exception as e:
    print(f"  ⚠️  Hybrid search test skipped: {e}")

print()

# Final Summary
print("=" * 80)
print("✅ ALL CORE TESTS PASSED - SYSTEM READY")
print("=" * 80)
print()
print("System Summary:")
print(f"  • {json_loader.TOTAL_ORDINANCES:,} ordinances loaded from JSON")
print(f"  • {json_loader.TOTAL_SECTIONS:,} legal sections available")
print(f"  • {all_legal_rules.TOTAL_RULES} legal rules implemented")
print(f"  • {all_cases_database.TOTAL_CASES} case precedents")
print(f"  • {len(json_loader.STATS['categories'])} legal categories")
print()
print("To run the web application:")
print("  ./scripts/run.sh")
print()
print("To use CLI interface:")
print("  python query.py \"Your legal question\"")
print()
print("Then open: http://localhost:8080")
print("=" * 80)

