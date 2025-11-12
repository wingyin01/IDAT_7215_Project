#!/usr/bin/env python3
"""
Parse Real Hong Kong Court Cases from Word Documents
Extracts case information and converts to structured CSV format
"""

import os
import re
import sys
from pathlib import Path
import pandas as pd

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

try:
    from docx import Document
except ImportError:
    print("❌ python-docx not installed. Installing...")
    os.system("pip3 install python-docx")
    from docx import Document

def extract_text_from_docx(file_path):
    """Extract text from .docx file"""
    try:
        doc = Document(file_path)
        full_text = []
        for para in doc.paragraphs:
            if para.text.strip():
                full_text.append(para.text.strip())
        return '\n'.join(full_text)
    except Exception as e:
        print(f"  ⚠️  Error reading {file_path}: {e}")
        return None

def extract_text_from_doc(file_path):
    """Extract text from .doc file using antiword or textutil"""
    try:
        # Try textutil (macOS)
        import subprocess
        result = subprocess.run(
            ['textutil', '-convert', 'txt', '-stdout', str(file_path)],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            return result.stdout
        
        # Fallback: try antiword (if installed)
        result = subprocess.run(
            ['antiword', str(file_path)],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            return result.stdout
        
        print(f"  ⚠️  Could not extract text from .doc file: {file_path}")
        return None
    except Exception as e:
        print(f"  ⚠️  Error reading {file_path}: {e}")
        return None

def parse_case_info(text, filename):
    """
    Parse case information from judgment text
    
    Args:
        text: Full judgment text
        filename: Original filename
    
    Returns:
        dict: Extracted case information
    """
    if not text:
        return None
    
    # Extract case number from filename (e.g., CACC000001_2020.doc)
    match = re.search(r'(CACC\d+[AB]?)_(\d{4})', filename)
    if match:
        case_number = match.group(1)
        year = match.group(2)
    else:
        case_number = filename.split('.')[0]
        year = "Unknown"
    
    # Initialize case data
    case_data = {
        'case_id': case_number,
        'case_number': case_number,
        'year': year,
        'court': 'Court of Appeal',
        'case_type': 'Criminal Appeal',
        'case_name': '',
        'appellant': '',
        'respondent': '',
        'facts': '',
        'charges': '',
        'ordinance_refs': '',
        'outcome': '',
        'sentence': '',
        'legal_principles': '',
        'keywords': '',
        'full_text': text[:5000]  # First 5000 chars
    }
    
    # Extract case name (usually in first few lines)
    lines = text.split('\n')
    for i, line in enumerate(lines[:20]):
        # Look for pattern like "HKSAR v. NAME" or "BETWEEN ... AND"
        if re.search(r'(?:HKSAR|The Secretary for Justice|SJ)\s+v\.?\s+', line, re.I):
            case_data['case_name'] = line.strip()
            # Extract respondent/appellant names
            parts = re.split(r'\s+v\.?\s+', line, flags=re.I)
            if len(parts) == 2:
                case_data['appellant'] = parts[0].strip()
                case_data['respondent'] = parts[1].strip()
            break
        elif 'BETWEEN' in line.upper() and i < 15:
            # Look for the actual parties in next few lines
            for j in range(i, min(i+5, len(lines))):
                if re.search(r'v\.?|versus', lines[j], re.I):
                    case_data['case_name'] = ' '.join(lines[i:j+1])
                    break
    
    # Extract charges/offences
    charges_section = extract_section(text, ['charge', 'offence', 'conviction'])
    if charges_section:
        case_data['charges'] = charges_section[:500]
    
    # Extract facts/background
    facts_section = extract_section(text, ['background', 'facts', 'the facts', 'factual background'])
    if facts_section:
        case_data['facts'] = facts_section[:1000]
    
    # Extract outcome/judgment
    outcome_section = extract_section(text, ['judgment', 'conclusion', 'order', 'disposition', 'appeal'])
    if outcome_section:
        case_data['outcome'] = outcome_section[:500]
        # Determine if appeal allowed/dismissed
        if re.search(r'appeal.*dismissed', outcome_section, re.I):
            case_data['outcome'] = 'Appeal Dismissed'
        elif re.search(r'appeal.*allowed', outcome_section, re.I):
            case_data['outcome'] = 'Appeal Allowed'
        elif re.search(r'conviction.*quashed', outcome_section, re.I):
            case_data['outcome'] = 'Conviction Quashed'
        elif re.search(r'sentence.*reduced', outcome_section, re.I):
            case_data['outcome'] = 'Sentence Reduced'
    
    # Extract sentence
    sentence_matches = re.findall(r'(\d+)\s+years?\s+imprisonment', text, re.I)
    if sentence_matches:
        case_data['sentence'] = f"{sentence_matches[0]} years imprisonment"
    else:
        sentence_matches = re.findall(r'(\d+)\s+months?\s+imprisonment', text, re.I)
        if sentence_matches:
            case_data['sentence'] = f"{sentence_matches[0]} months imprisonment"
    
    # Extract ordinance references (e.g., Cap. 200, s.10)
    ordinance_refs = set(re.findall(r'Cap\.?\s+\d+[A-Z]?,?\s+s\.?\s*\d+[A-Z]?', text, re.I))
    if ordinance_refs:
        case_data['ordinance_refs'] = '; '.join(sorted(ordinance_refs)[:10])
    
    # Generate keywords
    keywords = []
    keyword_patterns = {
        'theft': r'\btheft\b',
        'robbery': r'\brobb(?:ery|ed)\b',
        'assault': r'\bassault',
        'drug': r'\bdrug|dangerous\s+drug|narcotic',
        'fraud': r'\bfraud|dishonest',
        'murder': r'\bmurder|manslaughter',
        'sexual': r'\bsexual|rape|indecent',
        'possession': r'\bpossess(?:ion|ing)',
        'trafficking': r'\btraffick(?:ing|ed)',
        'firearm': r'\bfirearm|weapon',
    }
    
    text_lower = text.lower()
    for keyword, pattern in keyword_patterns.items():
        if re.search(pattern, text_lower):
            keywords.append(keyword)
    
    case_data['keywords'] = ', '.join(keywords[:8])
    
    return case_data

def extract_section(text, keywords):
    """
    Extract a section of text that follows certain keywords
    
    Args:
        text: Full text
        keywords: List of keywords to search for
    
    Returns:
        str: Extracted section text
    """
    lines = text.split('\n')
    
    for i, line in enumerate(lines):
        line_lower = line.lower()
        for keyword in keywords:
            if keyword.lower() in line_lower:
                # Found a section header, extract next ~10 paragraphs
                section_lines = []
                for j in range(i+1, min(i+20, len(lines))):
                    if lines[j].strip():
                        section_lines.append(lines[j].strip())
                    # Stop if we hit another major section
                    if len(section_lines) > 5 and re.match(r'^[A-Z\s]{10,}$', lines[j]):
                        break
                
                return ' '.join(section_lines)
    
    return ''

def parse_all_cases(cases_dir):
    """
    Parse all case files in directory
    
    Args:
        cases_dir: Path to directory containing case files
    
    Returns:
        list: List of parsed case dictionaries
    """
    cases_path = Path(cases_dir)
    
    if not cases_path.exists():
        print(f"❌ Directory not found: {cases_dir}")
        return []
    
    # Find all .doc and .docx files
    case_files = list(cases_path.glob('*.doc')) + list(cases_path.glob('*.docx'))
    
    print(f"Found {len(case_files)} case files")
    print("=" * 80)
    
    parsed_cases = []
    
    for i, file_path in enumerate(sorted(case_files), 1):
        print(f"{i}/{len(case_files)}: Processing {file_path.name}...")
        
        # Extract text based on file type
        if file_path.suffix == '.docx':
            text = extract_text_from_docx(file_path)
        else:  # .doc
            text = extract_text_from_doc(file_path)
        
        if text:
            case_data = parse_case_info(text, file_path.name)
            if case_data:
                parsed_cases.append(case_data)
                print(f"  ✅ Extracted: {case_data['case_name'][:60] if case_data['case_name'] else case_data['case_id']}")
            else:
                print(f"  ⚠️  Could not parse case data")
        
    print("=" * 80)
    print(f"✅ Successfully parsed {len(parsed_cases)} out of {len(case_files)} cases")
    
    return parsed_cases

def main():
    """Main entry point"""
    print("=" * 80)
    print("HONG KONG COURT CASES PARSER")
    print("=" * 80)
    print()
    
    # Path to cases directory
    cases_dir = project_root / "Past_case"
    
    # Parse all cases
    cases = parse_all_cases(cases_dir)
    
    if not cases:
        print("❌ No cases parsed successfully")
        return 1
    
    # Convert to DataFrame
    df = pd.DataFrame(cases)
    
    # Save to CSV
    output_csv = project_root / "knowledge_base" / "real_cases.csv"
    df.to_csv(output_csv, index=False, encoding='utf-8')
    
    print()
    print(f"💾 Saved to: {output_csv}")
    print()
    
    # Print summary
    print("=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print(f"Total cases: {len(cases)}")
    print(f"Years range: {df['year'].min()} - {df['year'].max()}")
    print(f"Cases with names: {df['case_name'].notna().sum()}")
    print(f"Cases with charges: {df['charges'].str.len().gt(10).sum()}")
    print(f"Cases with facts: {df['facts'].str.len().gt(10).sum()}")
    print(f"Cases with outcome: {df['outcome'].str.len().gt(5).sum()}")
    print()
    
    # Show sample cases
    print("Sample cases:")
    for i, row in df.head(3).iterrows():
        print(f"\n{i+1}. {row['case_id']} ({row['year']})")
        print(f"   Name: {row['case_name'][:70] if row['case_name'] else 'N/A'}")
        print(f"   Outcome: {row['outcome'][:50] if row['outcome'] else 'N/A'}")
        print(f"   Keywords: {row['keywords']}")
    
    print()
    print("=" * 80)
    print("✅ PARSING COMPLETE!")
    print("=" * 80)
    print()
    print("Next steps:")
    print("1. Review real_cases.csv")
    print("2. Run: python scripts/csv_to_cases.py to convert to Python format")
    print("3. Update case database with real cases")
    print()
    
    return 0

if __name__ == '__main__':
    sys.exit(main())

