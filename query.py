#!/usr/bin/env python3
"""
Hong Kong Legal Expert System - CLI Interface
Quick command-line consultation without starting the web server
"""

import sys
import argparse
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description='Hong Kong Legal Expert System - CLI Interface',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Quick legal query
  python query.py "What are the penalties for theft?"
  
  # Rule-based analysis
  python query.py --mode rule "Person stole property worth HK$5000"
  
  # RAG-powered consultation (requires Ollama)
  python query.py --mode rag "How do I register a company in Hong Kong?"
  
  # Search case law
  python query.py --mode cases "theft from store"
        """
    )
    
    parser.add_argument('query', nargs='?', help='Your legal question or query')
    parser.add_argument('--mode', choices=['rag', 'rule', 'cases', 'stats'], 
                       default='rag',
                       help='Consultation mode (default: rag)')
    parser.add_argument('--top-k', type=int, default=5,
                       help='Number of results for case search (default: 5)')
    parser.add_argument('--use-auto-rules', action='store_true',
                       help='Enable auto-generated rules from legislation (experimental)')
    parser.add_argument('--enhanced', action='store_true',
                       help='Use enhanced rule engine with auto-rules + fallback')
    
    args = parser.parse_args()
    
    # Show stats if no query provided or stats mode
    if not args.query or args.mode == 'stats':
        show_stats()
        if not args.query:
            return
    
    # Process query based on mode
    if args.mode == 'rag':
        run_rag_consultation(args.query)
    elif args.mode == 'rule':
        run_rule_analysis(args.query, use_enhanced=args.enhanced, use_auto_rules=args.use_auto_rules)
    elif args.mode == 'cases':
        search_cases(args.query, args.top_k)

def show_stats():
    """Display system statistics"""
    try:
        from knowledge_base import json_loader
        from knowledge_base import all_cases_database
        
        print("=" * 80)
        print("HONG KONG LEGAL EXPERT SYSTEM")
        print("=" * 80)
        print()
        print(f"📚 Legislation Database:")
        print(f"   Total Ordinances: {json_loader.TOTAL_ORDINANCES:,}")
        print(f"   Total Sections: {json_loader.TOTAL_SECTIONS:,}")
        print()
        print(f"📂 Categories:")
        categories = json_loader.get_categories_summary()
        for cat, info in sorted(categories.items(), key=lambda x: x[1]['sections'], reverse=True)[:5]:
            print(f"   {cat}: {info['count']} ordinances, {info['sections']:,} sections")
        print()
        print(f"⚖️  Case Database: {all_cases_database.TOTAL_CASES} cases")
        print()
        print("=" * 80)
        print()
        
    except Exception as e:
        print(f"❌ Error loading system: {e}")
        print("   Make sure you've run: ./scripts/preprocess_data.sh")
        sys.exit(1)

def run_rag_consultation(query):
    """Run RAG-powered consultation"""
    print("=" * 80)
    print("RAG CONSULTATION")
    print("=" * 80)
    print()
    print(f"Query: {query}")
    print()
    
    try:
        from engine.rag_engine import RAGLegalEngine
        
        print("Initializing RAG engine...")
        engine = RAGLegalEngine()
        print()
        
        print("Consulting...")
        result = engine.consult(query, stream=False)
        
        print("=" * 80)
        print("LEGAL ADVICE")
        print("=" * 80)
        print()
        print(result['advice'])
        print()
        
        print("=" * 80)
        print("SOURCES")
        print("=" * 80)
        print()
        print(f"📖 Legislation sections cited: {result['legislation_count']}")
        print(f"⚖️  Case precedents cited: {result['cases_count']}")
        print()
        
        # Show top citations
        citations = engine.get_source_citations(result['sources'])
        
        if citations['legislation']:
            print("Top Legislation:")
            for i, cite in enumerate(citations['legislation'][:3], 1):
                print(f"  {i}. {cite['reference']}: {cite['title']}")
        
        if citations['cases']:
            print()
            print("Relevant Cases:")
            for i, cite in enumerate(citations['cases'][:3], 1):
                print(f"  {i}. {cite['case_name']} ({cite['year']})")
        
        print()
        print("=" * 80)
        print()
        print("⚠️  DISCLAIMER: This is general legal information, not legal advice.")
        print("   Consult a qualified Hong Kong solicitor for specific legal matters.")
        print("=" * 80)
        print()
        
    except ImportError:
        print("❌ RAG engine not available")
        print("   Please ensure:")
        print("   1. Ollama is installed and running")
        print("   2. Embeddings are generated: python3 -m knowledge_base.embeddings_index")
        print("   3. Required packages installed: pip install -r requirements.txt")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

def run_rule_analysis(document_text, use_enhanced=False, use_auto_rules=False):
    """Run rule-based document analysis"""
    print("=" * 80)
    if use_enhanced:
        print("ENHANCED RULE-BASED ANALYSIS (with auto-rules + fallback)")
    else:
        print("RULE-BASED ANALYSIS (manual rules only)")
    print("=" * 80)
    print()
    
    try:
        from engine.document_analyzer import DocumentAnalyzer
        
        analyzer = DocumentAnalyzer()
        
        print("Analyzing document...")
        analysis = analyzer.analyze_document(document_text)
        
        print()
        print("Summary:", analysis['summary'])
        print()
        
        if analysis['facts']:
            print("Extracted Facts:")
            for fact in analysis['facts']:
                print(f"  • {fact}")
            print()
        
        # Try inference
        extracted_facts = analyzer.extract_for_inference(document_text)
        
        if use_enhanced:
            # Use enhanced engine with auto-rules
            from engine.enhanced_rule_engine import EnhancedRuleEngine
            from knowledge_base.json_loader import ALL_ORDINANCES
            
            print("Initializing enhanced rule engine...")
            engine = EnhancedRuleEngine(ALL_ORDINANCES, use_auto_rules=use_auto_rules)
            print()
            
            print("Running enhanced analysis...")
            results = engine.analyze(set(extracted_facts), document_text)
            explanation = engine.explain_analysis(results)
            print(explanation)
            
        else:
            # Use original rule engine
            from engine.rule_engine import analyze_case
            
            if extracted_facts:
                print("Running inference engine...")
                rule_engine = analyze_case(extracted_facts)
                offences = rule_engine.get_offences()
                
                if offences:
                    print()
                    print("Identified Offences:")
                    for offence in offences:
                        print(f"  • {offence['offence']} ({offence['ordinance_ref']})")
                        print(f"    Penalty: {offence['penalty']}")
                    print()
                    
                    print("Reasoning:")
                    print(rule_engine.explain())
                else:
                    print("⚠️  No matching rules found.")
                    print("   Try: python query.py --mode rule --enhanced \"your query\"")
        
        print()
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

def search_cases(query, top_k):
    """Search case law"""
    print("=" * 80)
    print("CASE SEARCH")
    print("=" * 80)
    print()
    print(f"Query: {query}")
    print()
    
    try:
        from engine.case_matcher import CaseMatcher
        
        matcher = CaseMatcher()
        results = matcher.find_similar_cases(query, top_k)
        
        if not results:
            print("No matching cases found.")
            return
        
        print(f"Found {len(results)} similar cases:")
        print()
        
        for i, (case, similarity) in enumerate(results, 1):
            print(f"{i}. {case.case_name} ({case.year})")
            print(f"   Court: {case.court}")
            print(f"   Similarity: {similarity:.1%}")
            print(f"   Outcome: {case.outcome}")
            print(f"   Facts: {case.facts[:200]}...")
            print()
        
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()

