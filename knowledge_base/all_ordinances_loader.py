"""
Comprehensive Hong Kong Legislation Loader
Loads ALL ordinances from all chapter ranges (1-658+)
"""

import xml.etree.ElementTree as ET
from pathlib import Path
import re
import sys

# Handle imports for both module and standalone execution
try:
    from .xml_parser import parse_ordinance_xml, clean_text, extract_text_content
except ImportError:
    from xml_parser import parse_ordinance_xml, clean_text, extract_text_content

# Ordinance categories based on subject matter
ORDINANCE_CATEGORIES = {
    'Criminal Law': {
        'chapters': ['200', '201', '210', '221', '228', '245', '374'],
        'keywords': ['crime', 'offence', 'punishment', 'criminal', 'theft', 'assault', 'drug']
    },
    'Civil Law': {
        'chapters': ['26', '29', '35', '347'],
        'keywords': ['contract', 'tort', 'negligence', 'sale of goods', 'damages']
    },
    'Employment Law': {
        'chapters': ['57', '282', '608'],
        'keywords': ['employment', 'labour', 'employee', 'employer', 'wages', 'termination']
    },
    'Property & Land': {
        'chapters': ['1', '7', '28', '123', '124'],
        'keywords': ['land', 'property', 'landlord', 'tenant', 'lease', 'conveyancing']
    },
    'Commercial & Company': {
        'chapters': ['32', '333', '571', '622'],
        'keywords': ['company', 'business', 'commercial', 'securities', 'banking']
    },
    'Family Law': {
        'chapters': ['179', '181', '192'],
        'keywords': ['marriage', 'divorce', 'matrimonial', 'child', 'custody']
    },
    'Immigration': {
        'chapters': ['115'],
        'keywords': ['immigration', 'entry', 'deportation', 'visa']
    },
    'Tax & Revenue': {
        'chapters': ['112', '117'],
        'keywords': ['tax', 'revenue', 'duty', 'stamp', 'inland revenue']
    },
    'Constitutional & Administrative': {
        'chapters': ['1', '2', '382'],
        'keywords': ['constitution', 'basic law', 'administrative', 'judicial review']
    },
    'Intellectual Property': {
        'chapters': ['528', '559'],
        'keywords': ['copyright', 'trademark', 'patent', 'intellectual property']
    }
}

def parse_all_ordinances_from_folders(base_dir):
    """
    Parse ALL ordinances from all three legislation folders
    
    Args:
        base_dir: Base directory containing Legislation/ folder
    
    Returns:
        dict: All ordinances organized by chapter
    """
    base_path = Path(base_dir)
    legislation_path = base_path / "Legislation"
    
    all_ordinances = {}
    total_parsed = 0
    total_sections = 0
    
    # Three folders to process
    folders = [
        'hkel_c_leg_cap_1_cap_300_en',
        'hkel_c_leg_cap_301_cap_600_en',
        'hkel_c_leg_cap_601_cap_end_en'
    ]
    
    print("=" * 80)
    print("LOADING ALL HONG KONG LEGISLATION")
    print("=" * 80)
    print()
    
    for folder_name in folders:
        folder_path = legislation_path / folder_name
        
        if not folder_path.exists():
            print(f"⚠️  Folder not found: {folder_name}")
            continue
        
        print(f"📁 Processing {folder_name}...")
        
        # Find all XML files in subdirectories (recursively)
        xml_files = list(folder_path.rglob("cap_*_en_c.xml"))
        
        print(f"   Found {len(xml_files)} XML files to process...")
        
        for xml_file in xml_files:
            try:
                # Extract chapter number from filename
                match = re.search(r'cap_(\w+)_\d+_en_c\.xml', xml_file.name)
                if not match:
                    continue
                
                chapter = match.group(1)
                
                # Skip if already loaded (take most recent version)
                if f'cap_{chapter}' in all_ordinances:
                    continue
                
                # Parse the ordinance
                ordinance_data = parse_ordinance_xml(str(xml_file))
                
                if ordinance_data and ordinance_data.get('sections'):
                    cap_key = f'cap_{chapter}'
                    # Only add if not already present or if this has more sections
                    if cap_key not in all_ordinances or len(ordinance_data['sections']) > len(all_ordinances[cap_key].get('sections', {})):
                        all_ordinances[cap_key] = ordinance_data
                        all_ordinances[cap_key]['chapter_display'] = f"Cap. {chapter}"
                        all_ordinances[cap_key]['xml_file'] = xml_file.name
                        
                        if cap_key not in [k for k, v in all_ordinances.items() if k != cap_key]:
                            total_parsed += 1
                        total_sections = sum(len(ord.get('sections', {})) for ord in all_ordinances.values() if ord)
                
            except Exception as e:
                # Silently skip problematic files
                continue
        
        print(f"   ✅ Processed {folder_name}")
        print()
    
    print("=" * 80)
    print(f"✅ LOADING COMPLETE")
    print(f"   Total ordinances loaded: {total_parsed}")
    print(f"   Total sections loaded: {total_sections}")
    print("=" * 80)
    print()
    
    return all_ordinances

def categorize_ordinances(all_ordinances):
    """
    Categorize ordinances by subject matter
    
    Args:
        all_ordinances: Dict of all ordinances
    
    Returns:
        dict: Ordinances organized by category
    """
    categorized = {}
    uncategorized = []
    
    for cap_key, ordinance in all_ordinances.items():
        if ordinance is None:
            continue
        
        chapter = ordinance.get('chapter', '')
        title = (ordinance.get('full_title') or '').lower()
        description = (ordinance.get('title') or '').lower()
        
        found_category = False
        
        # Try to match to category by chapter number
        for category, info in ORDINANCE_CATEGORIES.items():
            if chapter in info['chapters']:
                if category not in categorized:
                    categorized[category] = []
                categorized[category].append(ordinance)
                found_category = True
                break
        
        # Try to match by keywords if not found by chapter
        if not found_category:
            for category, info in ORDINANCE_CATEGORIES.items():
                for keyword in info['keywords']:
                    if keyword in title or keyword in description:
                        if category not in categorized:
                            categorized[category] = []
                        categorized[category].append(ordinance)
                        found_category = True
                        break
                if found_category:
                    break
        
        # Mark as uncategorized if still not found
        if not found_category:
            uncategorized.append(ordinance)
    
    # Add uncategorized to results
    if uncategorized:
        categorized['Other'] = uncategorized
    
    return categorized

def get_ordinance_statistics(all_ordinances):
    """Get statistics about loaded ordinances"""
    total_ordinances = len(all_ordinances)
    total_sections = sum(len(ord.get('sections', {})) for ord in all_ordinances.values())
    
    # Categorize
    categorized = categorize_ordinances(all_ordinances)
    
    stats = {
        'total_ordinances': total_ordinances,
        'total_sections': total_sections,
        'categories': {}
    }
    
    for category, ordinances in categorized.items():
        stats['categories'][category] = {
            'count': len(ordinances),
            'sections': sum(len(ord.get('sections', {})) for ord in ordinances)
        }
    
    return stats

if __name__ == '__main__':
    import sys
    
    if len(sys.argv) > 1:
        base_dir = sys.argv[1]
    else:
        base_dir = '/Users/wingyin/Documents/Expert system'
    
    print("Testing Comprehensive Ordinance Loader...")
    print()
    
    all_ordinances = parse_all_ordinances_from_folders(base_dir)
    
    # Get statistics
    stats = get_ordinance_statistics(all_ordinances)
    
    print("\n" + "=" * 80)
    print("STATISTICS")
    print("=" * 80)
    print(f"Total Ordinances: {stats['total_ordinances']}")
    print(f"Total Sections: {stats['total_sections']}")
    print()
    print("By Category:")
    for category, info in sorted(stats['categories'].items()):
        print(f"  {category}: {info['count']} ordinances, {info['sections']} sections")
    
    print("\n" + "=" * 80)

