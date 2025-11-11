"""
Preprocess Hong Kong Legislation from XML to JSON
One-time conversion script to create fast-loading knowledge base
"""

import json
from pathlib import Path
import sys
from datetime import datetime

# Import existing XML parser
try:
    from .xml_parser import parse_ordinance_xml, clean_text
except ImportError:
    from xml_parser import parse_ordinance_xml, clean_text

# Ordinance categories for classification
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

def create_embedding_text(section_data, chapter_title):
    """
    Create optimized text for embedding that includes context
    
    Args:
        section_data: Section dictionary with number, title, text
        chapter_title: Title of the ordinance
    
    Returns:
        str: Combined text optimized for semantic search
    """
    parts = []
    
    # Add ordinance context
    if chapter_title:
        parts.append(f"From {chapter_title}:")
    
    # Add section number and title
    if section_data.get('number'):
        parts.append(f"Section {section_data['number']}")
    
    if section_data.get('title'):
        parts.append(f"{section_data['title']}")
    
    # Add main text content
    if section_data.get('text'):
        parts.append(section_data['text'])
    
    # Add penalty if available (important for criminal law)
    if section_data.get('penalty'):
        parts.append(f"Penalty: {section_data['penalty']}")
    
    return ' '.join(parts)

def categorize_ordinance(chapter, title, sections):
    """
    Categorize ordinance based on chapter number and keywords
    
    Args:
        chapter: Chapter number
        title: Ordinance title
        sections: Dictionary of sections
    
    Returns:
        str: Category name
    """
    title_lower = title.lower() if title else ""
    
    # Check chapter-based categories first
    for category, info in ORDINANCE_CATEGORIES.items():
        if chapter in info.get('chapters', []):
            return category
    
    # Check keyword-based categories
    for category, info in ORDINANCE_CATEGORIES.items():
        keywords = info.get('keywords', [])
        for keyword in keywords:
            if keyword in title_lower:
                return category
            
            # Also check section texts
            for section_data in sections.values():
                section_text = section_data.get('text', '').lower()
                if keyword in section_text[:500]:  # Check first 500 chars
                    return category
    
    return 'Other'

def preprocess_all_legislation(base_dir, output_path=None):
    """
    Parse all XML files and convert to JSON
    
    Args:
        base_dir: Base directory containing Legislation/ folder
        output_path: Path to save JSON file (default: knowledge_base/legislation_database.json)
    
    Returns:
        dict: Statistics about the processing
    """
    base_path = Path(base_dir)
    legislation_path = base_path / "Legislation"
    
    if output_path is None:
        output_path = base_path / "knowledge_base" / "legislation_database.json"
    
    all_ordinances = {}
    stats = {
        'total_ordinances': 0,
        'total_sections': 0,
        'categories': {},
        'processing_time': None,
        'created_at': datetime.now().isoformat()
    }
    
    # Three folders to process
    folders = [
        'hkel_c_leg_cap_1_cap_300_en',
        'hkel_c_leg_cap_301_cap_600_en',
        'hkel_c_leg_cap_601_cap_end_en'
    ]
    
    print("=" * 80)
    print("PREPROCESSING HONG KONG LEGISLATION: XML → JSON")
    print("=" * 80)
    print()
    
    start_time = datetime.now()
    
    for folder_name in folders:
        folder_path = legislation_path / folder_name
        
        if not folder_path.exists():
            print(f"⚠️  Folder not found: {folder_name}")
            continue
        
        print(f"📁 Processing {folder_name}...")
        
        # Find all XML files
        import re
        xml_files = list(folder_path.rglob("cap_*_en_c.xml"))
        
        print(f"   Found {len(xml_files)} XML files")
        
        processed_count = 0
        for xml_file in xml_files:
            try:
                # Extract chapter number from filename
                match = re.search(r'cap_(\w+)_\d+_en_c\.xml', xml_file.name)
                if not match:
                    continue
                
                chapter = match.group(1)
                cap_key = f'cap_{chapter}'
                
                # Skip if already loaded (keep first version found)
                if cap_key in all_ordinances:
                    continue
                
                # Parse the ordinance
                ordinance_data = parse_ordinance_xml(str(xml_file))
                
                if ordinance_data and ordinance_data.get('sections'):
                    # Add metadata
                    ordinance_data['chapter'] = chapter
                    ordinance_data['cap_key'] = cap_key
                    
                    # Categorize
                    category = categorize_ordinance(
                        chapter, 
                        ordinance_data.get('title', ''),
                        ordinance_data['sections']
                    )
                    ordinance_data['category'] = category
                    
                    # Create embedding text for each section
                    chapter_title = ordinance_data.get('title', '')
                    for section_num, section_data in ordinance_data['sections'].items():
                        section_data['embedding_text'] = create_embedding_text(
                            section_data, 
                            chapter_title
                        )
                    
                    # Add to collection
                    all_ordinances[cap_key] = ordinance_data
                    processed_count += 1
                    
                    # Update stats
                    stats['total_sections'] += len(ordinance_data['sections'])
                    stats['categories'][category] = stats['categories'].get(category, 0) + 1
                    
            except Exception as e:
                print(f"   ⚠️  Error processing {xml_file.name}: {e}")
                continue
        
        print(f"   ✅ Processed {processed_count} ordinances from {folder_name}")
        print()
    
    stats['total_ordinances'] = len(all_ordinances)
    end_time = datetime.now()
    stats['processing_time'] = str(end_time - start_time)
    
    print("=" * 80)
    print(f"✅ PREPROCESSING COMPLETE")
    print(f"   Total ordinances: {stats['total_ordinances']}")
    print(f"   Total sections: {stats['total_sections']}")
    print(f"   Processing time: {stats['processing_time']}")
    print()
    print("📊 Categories:")
    for category, count in sorted(stats['categories'].items(), key=lambda x: x[1], reverse=True):
        sections_in_category = sum(
            len(ord['sections']) 
            for ord in all_ordinances.values() 
            if ord.get('category') == category
        )
        print(f"   {category}: {count} ordinances, {sections_in_category} sections")
    print("=" * 80)
    print()
    
    # Save to JSON
    print(f"💾 Saving to {output_path}...")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Create final data structure
    final_data = {
        'metadata': stats,
        'ordinances': all_ordinances
    }
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(final_data, f, ensure_ascii=False, indent=2)
    
    file_size = output_path.stat().st_size / (1024 * 1024)  # Convert to MB
    print(f"✅ Saved: {file_size:.2f} MB")
    print()
    
    return stats

def main():
    """Main entry point for preprocessing"""
    if len(sys.argv) > 1:
        base_dir = sys.argv[1]
    else:
        # Default to script's parent directory
        base_dir = Path(__file__).parent.parent
    
    output_path = None
    if len(sys.argv) > 2:
        output_path = Path(sys.argv[2])
    
    print("🚀 Starting XML to JSON preprocessing...")
    print(f"📂 Base directory: {base_dir}")
    print()
    
    stats = preprocess_all_legislation(base_dir, output_path)
    
    print("=" * 80)
    print("✅ ALL DONE!")
    print("=" * 80)
    print()
    print("Next steps:")
    print("1. Run json_loader.py to test loading speed")
    print("2. Run embeddings_index.py to generate embeddings")
    print()

if __name__ == '__main__':
    main()

