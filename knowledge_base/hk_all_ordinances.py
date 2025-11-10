"""
IDAT7215 Hong Kong Legal Expert System - ALL Ordinances
Comprehensive knowledge base with ALL Hong Kong legislation
Data source: Official Hong Kong e-Legislation Portal
Total: 2,234 ordinances with 52,269 sections
"""

from pathlib import Path
import sys

# Handle imports
try:
    from .all_ordinances_loader import parse_all_ordinances_from_folders, categorize_ordinances, get_ordinance_statistics
except ImportError:
    from all_ordinances_loader import parse_all_ordinances_from_folders, categorize_ordinances, get_ordinance_statistics

# Path to base directory
BASE_DIR = Path(__file__).parent.parent

# Load ALL ordinances from all three folders
print("="*80)
print("IDAT7215 Hong Kong Legal Expert System - Loading ALL Legislation")
print("="*80)
print("This may take 30-60 seconds...")
print()

ALL_ORDINANCES = parse_all_ordinances_from_folders(str(BASE_DIR))

# Get statistics
STATS = get_ordinance_statistics(ALL_ORDINANCES)
TOTAL_ORDINANCES = STATS['total_ordinances']
TOTAL_SECTIONS = STATS['total_sections']

# Categorize ordinances
CATEGORIZED_ORDINANCES = categorize_ordinances(ALL_ORDINANCES)

print(f"✅ System ready with {TOTAL_ORDINANCES} ordinances and {TOTAL_SECTIONS} sections")
print("="*80)
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
        search_ordinances = {f"cap_{ord.get('chapter')}": ord 
                            for ord in CATEGORIZED_ORDINANCES[category]}
    else:
        search_ordinances = ALL_ORDINANCES
    
    for cap_key, ordinance_data in search_ordinances.items():
        if ordinance_data is None:
            continue
            
        for section_num, section_data in ordinance_data.get('sections', {}).items():
            # Search in title and text
            title_match = keyword_lower in section_data.get('title', '').lower()
            text_match = keyword_lower in section_data.get('text', '').lower()
            
            if title_match or text_match:
                results.append({
                    "ordinance": ordinance_data.get('full_title', ''),
                    "chapter": ordinance_data.get('chapter', ''),
                    "section": section_num,
                    "title": section_data.get('title', ''),
                    "text": section_data.get('text', ''),
                    "penalty": section_data.get('penalty', ''),
                    "data": section_data
                })
    
    return results

def get_ordinances_by_category(category):
    """Get all ordinances in a specific category"""
    if category in CATEGORIZED_ORDINANCES:
        return CATEGORIZED_ORDINANCES[category]
    return []

def list_all_ordinances():
    """List all loaded ordinances with summary"""
    ordinance_list = []
    for cap_key, ordinance in ALL_ORDINANCES.items():
        if ordinance is None:
            continue
        ordinance_list.append({
            'chapter': ordinance.get('chapter', ''),
            'title': ordinance.get('full_title', ''),
            'num_sections': len(ordinance.get('sections', {}))
        })
    return sorted(ordinance_list, key=lambda x: x.get('chapter', ''))

def get_categories_summary():
    """Get summary of all categories"""
    return STATS.get('categories', {})

# Export key statistics
__all__ = [
    'ALL_ORDINANCES',
    'CATEGORIZED_ORDINANCES',
    'TOTAL_ORDINANCES',
    'TOTAL_SECTIONS',
    'STATS',
    'get_ordinance_section',
    'search_ordinances_by_keyword',
    'get_ordinances_by_category',
    'list_all_ordinances',
    'get_categories_summary'
]

if __name__ == '__main__':
    print("\n" + "=" * 80)
    print("IDAT7215 HONG KONG LEGAL EXPERT SYSTEM - KNOWLEDGE BASE")
    print("=" * 80)
    print(f"\nTotal Ordinances: {TOTAL_ORDINANCES}")
    print(f"Total Sections: {TOTAL_SECTIONS}")
    print(f"\nCategories: {len(STATS['categories'])}")
    
    print("\nBreakdown by Category:")
    for category, info in sorted(STATS['categories'].items(), key=lambda x: x[1]['sections'], reverse=True):
        print(f"  {category}: {info['count']} ordinances, {info['sections']} sections")
    
    # Test search
    print("\n" + "=" * 80)
    print("TEST SEARCH: 'employment'")
    results = search_ordinances_by_keyword('employment')
    print(f"Found {len(results)} matching sections")
    for r in results[:5]:
        print(f"  Cap. {r['chapter']}, s. {r['section']}: {r['title']}")
    print("=" * 80)

