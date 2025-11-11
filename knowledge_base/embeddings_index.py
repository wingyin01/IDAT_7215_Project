"""
Embeddings Index Builder
Creates and caches embeddings for all legislation and case law
"""

import sys
from pathlib import Path
import time

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from engine.hybrid_search import HybridSearchEngine

# Import data loaders
try:
    from knowledge_base import json_loader
    from knowledge_base import all_cases_database
except ImportError:
    import json_loader
    import all_cases_database

# Cache directory
BASE_DIR = Path(__file__).parent.parent
CACHE_DIR = BASE_DIR / "knowledge_base" / "cached_embeddings"

def build_and_cache_embeddings(force_rebuild=False):
    """
    Build embeddings index and cache to disk
    
    Args:
        force_rebuild: If True, rebuild even if cache exists
    
    Returns:
        HybridSearchEngine: Initialized search engine
    """
    print("=" * 80)
    print("BUILDING EMBEDDINGS INDEX")
    print("=" * 80)
    print()
    
    # Initialize search engine
    search_engine = HybridSearchEngine()
    
    # Check if cache exists
    if not force_rebuild and CACHE_DIR.exists():
        print("Checking for existing cache...")
        if search_engine.load_index(CACHE_DIR):
            print("✅ Loaded from cache!")
            return search_engine
        else:
            print("Cache not found or corrupted, rebuilding...")
    
    print("Building new index (this will take 5-10 minutes)...")
    print()
    
    start_time = time.time()
    
    # Load legislation data
    print("Step 1: Loading legislation database...")
    if not hasattr(json_loader, 'ALL_ORDINANCES') or not json_loader.ALL_ORDINANCES:
        print("⚠️  No legislation data found. Please run preprocess_legislation.py first.")
        return None
    
    print(f"   Found {json_loader.TOTAL_ORDINANCES} ordinances with {json_loader.TOTAL_SECTIONS} sections")
    print()
    
    # Index legislation
    print("Step 2: Indexing legislation...")
    search_engine.index_legislation(json_loader.ALL_ORDINANCES)
    print()
    
    # Load and index cases
    print("Step 3: Loading case database...")
    cases = all_cases_database.ALL_LEGAL_CASES
    print(f"   Found {len(cases)} cases")
    print()
    
    if cases:
        print("Step 4: Indexing cases...")
        search_engine.index_cases(cases)
        print()
    
    # Save to cache
    print("Step 5: Caching embeddings...")
    search_engine.save_index(CACHE_DIR)
    print()
    
    elapsed_time = time.time() - start_time
    print("=" * 80)
    print(f"✅ INDEX BUILD COMPLETE")
    print(f"   Total time: {elapsed_time:.2f} seconds ({elapsed_time/60:.1f} minutes)")
    print("=" * 80)
    print()
    
    return search_engine

def test_search_engine(search_engine):
    """
    Test the search engine with sample queries
    
    Args:
        search_engine: Initialized HybridSearchEngine
    """
    print("=" * 80)
    print("TESTING SEARCH ENGINE")
    print("=" * 80)
    print()
    
    test_queries = [
        "What are the penalties for theft?",
        "Can I sue my employer for wrongful termination?",
        "What is the definition of assault?",
        "How do I register a company in Hong Kong?",
        "What are my rights as a tenant?"
    ]
    
    for query in test_queries:
        print(f"Query: \"{query}\"")
        print("-" * 80)
        
        try:
            # Search legislation
            results = search_engine.search_legislation_only(query, top_k=3)
            
            print(f"Found {len(results)} relevant legislation sections:\n")
            
            for i, result in enumerate(results, 1):
                metadata = result['metadata']
                print(f"{i}. Cap. {metadata['chapter']}, Section {metadata['section']}")
                print(f"   {metadata['title']}")
                print(f"   Category: {metadata['category']}")
                print(f"   Hybrid Score: {result['hybrid_score']:.3f} "
                      f"(Semantic: {result['semantic_score']:.3f}, "
                      f"TF-IDF: {result['tfidf_score']:.3f})")
                print(f"   Text: {metadata['text'][:150]}...")
                print()
            
            # Search cases
            case_results = search_engine.search_cases_only(query, top_k=2)
            
            if case_results:
                print(f"Found {len(case_results)} relevant cases:\n")
                
                for i, result in enumerate(case_results, 1):
                    metadata = result['metadata']
                    print(f"{i}. {metadata['case_name']} ({metadata['year']})")
                    print(f"   Outcome: {metadata['outcome']}")
                    print(f"   Hybrid Score: {result['hybrid_score']:.3f}")
                    print(f"   Facts: {metadata['facts'][:150]}...")
                    print()
            
        except Exception as e:
            print(f"❌ Error: {e}")
            print()
        
        print("=" * 80)
        print()

def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Build and cache embeddings index')
    parser.add_argument('--rebuild', action='store_true', 
                       help='Force rebuild even if cache exists')
    parser.add_argument('--no-test', action='store_true',
                       help='Skip testing after building')
    
    args = parser.parse_args()
    
    # Build/load index
    search_engine = build_and_cache_embeddings(force_rebuild=args.rebuild)
    
    if search_engine is None:
        print("❌ Failed to build search engine")
        return 1
    
    # Test if requested
    if not args.no_test:
        test_search_engine(search_engine)
    
    print("=" * 80)
    print("✅ ALL DONE!")
    print("=" * 80)
    print()
    print("The embeddings index is ready for use.")
    print("Next steps:")
    print("1. Run setup_rag.sh to install Ollama and LLaMA")
    print("2. Test the RAG engine with rag_engine.py")
    print()
    
    return 0

if __name__ == '__main__':
    sys.exit(main())

