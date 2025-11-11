"""
Fast JSON Loader for Hong Kong Legislation
Loads preprocessed legislation_database.json in 2-5 seconds
Provides same interface as hk_all_ordinances.py for backward compatibility
"""

import json
from pathlib import Path
import time

# Path to the JSON database
BASE_DIR = Path(__file__).parent.parent
JSON_DB_PATH = BASE_DIR / "knowledge_base" / "legislation_database.json"

# Global variables (matching hk_all_ordinances.py interface)
ALL_ORDINANCES = {}
STATS = {}
TOTAL_ORDINANCES = 0
TOTAL_SECTIONS = 0
CATEGORIZED_ORDINANCES = {}

def load_legislation_database(json_path=None):
    """
    Load legislation from JSON file
    
    Args:
        json_path: Path to JSON file (default: legislation_database.json)
    
    Returns:
        tuple: (all_ordinances, stats)
    """
    if json_path is None:
        json_path = JSON_DB_PATH
    
    json_path = Path(json_path)
    
    if not json_path.exists():
        raise FileNotFoundError(
            f"Legislation database not found at {json_path}\n"
            f"Please run preprocess_legislation.py first to create it."
        )
    
    print("=" * 80)
    print("Loading Hong Kong Legislation from JSON...")
    print("=" * 80)
    
    start_time = time.time()
    
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    all_ordinances = data.get('ordinances', {})
    metadata = data.get('metadata', {})
    
    # Calculate stats
    total_ordinances = len(all_ordinances)
    total_sections = sum(len(ord.get('sections', {})) for ord in all_ordinances.values())
    
    # Organize by category
    categorized = {}
    for cap_key, ordinance in all_ordinances.items():
        category = ordinance.get('category', 'Other')
        if category not in categorized:
            categorized[category] = []
        categorized[category].append(ordinance)
    
    # Build stats
    stats = {
        'total_ordinances': total_ordinances,
        'total_sections': total_sections,
        'categories': {}
    }
    
    for category, ordinances in categorized.items():
        sections_count = sum(len(ord.get('sections', {})) for ord in ordinances)
        stats['categories'][category] = {
            'count': len(ordinances),
            'sections': sections_count
        }
    
    elapsed_time = time.time() - start_time
    
    print(f"✅ Loaded {total_ordinances} ordinances with {total_sections} sections")
    print(f"⚡ Loading time: {elapsed_time:.2f} seconds")
    print("=" * 80)
    print()
    
    return all_ordinances, stats, categorized

# Load on module import
try:
    ALL_ORDINANCES, STATS, CATEGORIZED_ORDINANCES = load_legislation_database()
    TOTAL_ORDINANCES = STATS['total_ordinances']
    TOTAL_SECTIONS = STATS['total_sections']
except FileNotFoundError as e:
    print(f"⚠️  Warning: {e}")
    print("    Run 'python -m knowledge_base.preprocess_legislation' to create the database.")
    print()

def get_ordinance_section(chapter, section):
    """
    Retrieve a specific section from any ordinance
    
    Args:
        chapter: Chapter number (e.g., "200", "57", "622")
        section: Section number (e.g., "9", "19", "118")
    
    Returns:
        dict: Section data including title, text, penalty if found
    """
    cap_key = f'cap_{chapter}'
    if cap_key in ALL_ORDINANCES:
        sections = ALL_ORDINANCES[cap_key].get('sections', {})
        return sections.get(str(section))
    return None

def search_ordinances_by_keyword(keyword, category=None):
    """
    Search ordinances for sections containing keyword
    
    Args:
        keyword: Search term
        category: Optional category to limit search
    
    Returns:
        list: List of matching sections
    """
    results = []
    keyword_lower = keyword.lower()
    
    # Determine which ordinances to search
    if category and category in CATEGORIZED_ORDINANCES:
        search_ordinances = {
            f"cap_{ord.get('chapter')}": ord 
            for ord in CATEGORIZED_ORDINANCES[category]
        }
    else:
        search_ordinances = ALL_ORDINANCES
    
    for cap_key, ordinance_data in search_ordinances.items():
        if ordinance_data is None:
            continue
            
        for section_num, section_data in ordinance_data.get('sections', {}).items():
            # Search in title, text, and embedding_text
            title_match = keyword_lower in section_data.get('title', '').lower()
            text_match = keyword_lower in section_data.get('text', '').lower()
            embedding_match = keyword_lower in section_data.get('embedding_text', '').lower()
            
            if title_match or text_match or embedding_match:
                results.append({
                    "ordinance": ordinance_data.get('title', ''),
                    "chapter": ordinance_data.get('chapter', ''),
                    "section": section_num,
                    "title": section_data.get('title', ''),
                    "text": section_data.get('text', ''),
                    "penalty": section_data.get('penalty', ''),
                    "category": ordinance_data.get('category', ''),
                    "data": section_data
                })
    
    return results

def list_all_ordinances():
    """
    Get list of all ordinances
    
    Returns:
        list: List of ordinance summaries
    """
    ordinances = []
    for cap_key, ordinance in ALL_ORDINANCES.items():
        ordinances.append({
            'chapter': ordinance.get('chapter', ''),
            'title': ordinance.get('title', ''),
            'category': ordinance.get('category', ''),
            'num_sections': len(ordinance.get('sections', {}))
        })
    return ordinances

def get_categories_summary():
    """
    Get summary of all categories
    
    Returns:
        dict: Category statistics
    """
    return STATS.get('categories', {})

def get_ordinance_statistics():
    """
    Get overall statistics
    
    Returns:
        dict: Statistics dictionary
    """
    return STATS

def reload_database(json_path=None):
    """
    Reload the database (useful for development)
    
    Args:
        json_path: Path to JSON file
    """
    global ALL_ORDINANCES, STATS, CATEGORIZED_ORDINANCES, TOTAL_ORDINANCES, TOTAL_SECTIONS
    
    ALL_ORDINANCES, STATS, CATEGORIZED_ORDINANCES = load_legislation_database(json_path)
    TOTAL_ORDINANCES = STATS['total_ordinances']
    TOTAL_SECTIONS = STATS['total_sections']

if __name__ == '__main__':
    print("=" * 80)
    print("JSON Loader Test")
    print("=" * 80)
    print()
    
    print(f"Total Ordinances: {TOTAL_ORDINANCES}")
    print(f"Total Sections: {TOTAL_SECTIONS}")
    print()
    
    print("Categories:")
    for category, info in sorted(
        STATS['categories'].items(), 
        key=lambda x: x[1]['sections'], 
        reverse=True
    ):
        print(f"  {category}: {info['count']} ordinances, {info['sections']} sections")
    print()
    
    # Test search
    print("=" * 80)
    print("Testing keyword search: 'theft'")
    print("=" * 80)
    results = search_ordinances_by_keyword('theft')
    print(f"Found {len(results)} matching sections")
    if results:
        for i, result in enumerate(results[:3], 1):
            print(f"\n{i}. Cap. {result['chapter']}, Section {result['section']}")
            print(f"   {result['title']}")
            print(f"   Text: {result['text'][:100]}...")
    print()
    
    # Test section retrieval
    print("=" * 80)
    print("Testing section retrieval: Cap. 210, Section 2")
    print("=" * 80)
    section = get_ordinance_section('210', '2')
    if section:
        print(f"Title: {section.get('title')}")
        print(f"Text: {section.get('text')[:200]}...")
    else:
        print("Section not found")
    print()

