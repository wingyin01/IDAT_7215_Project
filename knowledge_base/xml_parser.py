"""
XML Parser for Hong Kong e-Legislation
Parses official XML files from Hong Kong e-Legislation database
"""

import xml.etree.ElementTree as ET
import re
from pathlib import Path

# Define XML namespace
NS = {'hklm': 'http://www.xml.gov.hk/schemas/hklm/1.0'}

def clean_text(text):
    """Remove extra whitespace and clean text"""
    if not text:
        return ""
    # Remove XML tags if any remain
    text = re.sub(r'<[^>]+>', '', text)
    # Normalize whitespace
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def extract_text_content(element):
    """Recursively extract all text from an element and its children"""
    text_parts = []
    
    if element.text:
        text_parts.append(element.text)
    
    for child in element:
        # Skip sourceNote elements
        if 'sourceNote' in child.tag or 'referenceNote' in child.tag:
            continue
        text_parts.append(extract_text_content(child))
        if child.tail:
            text_parts.append(child.tail)
    
    return ' '.join(text_parts)

def parse_section(section_elem):
    """Parse a section element to extract section info"""
    section_data = {}
    
    # Get section number
    num_elem = section_elem.find('.//{*}num')
    if num_elem is not None:
        section_data['number'] = clean_text(num_elem.get('value', ''))
    
    # Get heading
    heading_elem = section_elem.find('.//{*}heading')
    if heading_elem is not None:
        section_data['title'] = clean_text(extract_text_content(heading_elem))
    
    # Get content - try multiple paths
    content_parts = []
    
    # Check for direct content
    content_elems = section_elem.findall('.//{*}content')
    for content_elem in content_elems:
        content_text = extract_text_content(content_elem)
        if content_text:
            content_parts.append(content_text)
    
    # Check for leadIn
    leadin_elems = section_elem.findall('.//{*}leadIn')
    for leadin in leadin_elems:
        leadin_text = extract_text_content(leadin)
        if leadin_text:
            content_parts.append(leadin_text)
    
    # Check for paragraphs
    para_elems = section_elem.findall('.//{*}paragraph')
    for para in para_elems:
        para_num = para.find('.//{*}num')
        para_content = para.find('.//{*}content')
        if para_num is not None and para_content is not None:
            num_text = clean_text(extract_text_content(para_num))
            content_text = clean_text(extract_text_content(para_content))
            if content_text:
                content_parts.append(f"{num_text} {content_text}")
    
    section_data['text'] = clean_text(' '.join(content_parts))
    
    # Try to extract penalty information from text
    text_lower = section_data.get('text', '').lower()
    if 'liable' in text_lower and 'imprisonment' in text_lower:
        # Extract penalty pattern
        penalty_match = re.search(r'imprisonment for (\d+|life) (years?|imprisonment)', section_data['text'], re.IGNORECASE)
        if penalty_match:
            section_data['penalty'] = penalty_match.group(0)
    
    # Get section status
    section_data['status'] = section_elem.get('status', 'operational')
    
    return section_data

def parse_ordinance_xml(xml_path):
    """Parse an ordinance XML file"""
    try:
        tree = ET.parse(xml_path)
        root = tree.getroot()
        
        ordinance_data = {
            'chapter': None,
            'title': None,
            'sections': {}
        }
        
        # Get metadata
        meta = root.find('.//{*}meta')
        if meta is not None:
            doc_name = meta.find('.//{*}docName')
            if doc_name is not None:
                ordinance_data['chapter'] = clean_text(doc_name.text).replace('Cap. ', '')
        
        # Get long title
        long_title = root.find('.//{*}longTitle')
        if long_title is not None:
            content = long_title.find('.//{*}content')
            if content is not None:
                ordinance_data['title'] = clean_text(extract_text_content(content))
        
        # Find all sections
        sections = root.findall('.//{*}section')
        for section in sections:
            # Skip repealed sections
            if section.get('status') == 'repealed':
                continue
                
            section_data = parse_section(section)
            if section_data.get('number') and section_data.get('text'):
                ordinance_data['sections'][section_data['number']] = section_data
        
        return ordinance_data
        
    except Exception as e:
        print(f"Error parsing {xml_path}: {e}")
        return None

def parse_criminal_ordinances(legislation_dir):
    """Parse all criminal law ordinances from the legislation directory"""
    legislation_path = Path(legislation_dir)
    
    criminal_ordinances = {}
    
    # Target files
    target_files = {
        'cap_200': ('cap_200_en_c\\cap_200_20240323000000_en_c.xml', 'Crimes Ordinance'),
        'cap_201': ('cap_201_en_c\\cap_201_20250620000000_en_c.xml', 'Offences Against the Person Ordinance'),
        'cap_210': ('cap_210_en_c\\cap_210_20210624000000_en_c.xml', 'Theft Ordinance'),
        'cap_221': ('cap_221_en_c\\cap_221_20250414000000_en_c.xml', 'Dangerous Drugs Ordinance'),
        'cap_245': ('cap_245_en_c\\cap_245_20240323000000_en_c.xml', 'Public Order Ordinance'),
    }
    
    for cap_key, (file_path, title) in target_files.items():
        full_path = legislation_path / file_path
        if full_path.exists():
            print(f"Parsing {title}...")
            ordinance_data = parse_ordinance_xml(full_path)
            if ordinance_data:
                ordinance_data['full_title'] = title
                criminal_ordinances[cap_key] = ordinance_data
                print(f"  Extracted {len(ordinance_data['sections'])} sections")
        else:
            print(f"Warning: {full_path} not found")
    
    return criminal_ordinances

def get_section_by_number(ordinances_dict, chapter, section_num):
    """Retrieve a specific section from parsed ordinances"""
    cap_key = f'cap_{chapter}'
    if cap_key in ordinances_dict:
        return ordinances_dict[cap_key]['sections'].get(str(section_num))
    return None

def search_sections_by_keyword(ordinances_dict, keyword):
    """Search for sections containing a keyword"""
    results = []
    keyword_lower = keyword.lower()
    
    for cap_key, ordinance in ordinances_dict.items():
        for section_num, section_data in ordinance['sections'].items():
            title_match = keyword_lower in section_data.get('title', '').lower()
            text_match = keyword_lower in section_data.get('text', '').lower()
            
            if title_match or text_match:
                results.append({
                    'chapter': ordinance['chapter'],
                    'title': ordinance['full_title'],
                    'section': section_num,
                    'section_title': section_data.get('title', ''),
                    'section_data': section_data
                })
    
    return results

if __name__ == '__main__':
    # Test the parser
    import sys
    if len(sys.argv) > 1:
        legislation_dir = sys.argv[1]
    else:
        legislation_dir = '/Users/wingyin/Documents/Expert system/hkel_c_leg_cap_1_cap_300_en'
    
    print("Parsing Hong Kong Criminal Law Ordinances...")
    ordinances = parse_criminal_ordinances(legislation_dir)
    
    print(f"\nSuccessfully parsed {len(ordinances)} ordinances:")
    for cap_key, ordinance in ordinances.items():
        print(f"  {ordinance['full_title']} (Cap. {ordinance['chapter']}): {len(ordinance['sections'])} sections")

