#!/usr/bin/env python3
"""
Convert CSV of real cases to Python format for all_cases_database.py
"""

import sys
import pandas as pd
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

def csv_to_python_cases(csv_path, output_path):
    """
    Convert CSV to Python case database format
    
    Args:
        csv_path: Path to CSV file
        output_path: Path to output Python file
    """
    # Read CSV
    df = pd.read_csv(csv_path)
    
    print(f"Loaded {len(df)} cases from CSV")
    print()
    
    # Generate Python code
    python_code = '''"""
Real Hong Kong Criminal Appeal Cases Database
Cases from Court of Appeal of the High Court (Criminal Appeals)
Source: Official HK Judiciary Database (legalref.judiciary.hk)
Manually downloaded and processed for educational purposes

⚠️ Copyright Notice:
These cases are from official Hong Kong Judiciary sources.
Data is used for educational/research purposes under fair use.
For official case law research, visit: https://legalref.judiciary.hk/
"""

class CriminalCase:
    """Represents a criminal appeal case"""
    def __init__(self, case_id, case_name, year, court, facts, charges, 
                 ordinance_refs, outcome, sentence, legal_principles, keywords):
        self.case_id = case_id
        self.case_name = case_name
        self.year = year
        self.court = court
        self.facts = facts
        self.charges = charges
        self.ordinance_refs = ordinance_refs
        self.outcome = outcome
        self.sentence = sentence
        self.legal_principles = legal_principles
        self.keywords = keywords
    
    def to_dict(self):
        return {
            "case_id": self.case_id,
            "case_name": self.case_name,
            "year": self.year,
            "court": self.court,
            "facts": self.facts,
            "charges": self.charges,
            "ordinance_refs": self.ordinance_refs,
            "outcome": self.outcome,
            "sentence": self.sentence,
            "legal_principles": self.legal_principles,
            "keywords": self.keywords
        }
    
    def __repr__(self):
        return f"Case({self.case_id}: {self.case_name[:30] if self.case_name else self.case_id} ({self.year}))"

# REAL CRIMINAL APPEAL CASES
ALL_CRIMINAL_CASES = [
'''
    
    # Add each case
    for idx, row in df.iterrows():
        # Clean and escape strings
        case_name = str(row['case_name'])[:100] if pd.notna(row['case_name']) else ''
        case_name = case_name.replace('\\', '\\\\').replace('"', '\\"').replace('\n', ' ')
        
        facts = str(row['facts'])[:800] if pd.notna(row['facts']) else ''
        facts = facts.replace('\\', '\\\\').replace('"""', "'''").replace('\n', ' ')
        
        charges = str(row['charges'])[:400] if pd.notna(row['charges']) else ''
        charges = charges.replace('\\', '\\\\').replace('"""', "'''").replace('\n', ' ')
        
        ordinance_refs = str(row['ordinance_refs']) if pd.notna(row['ordinance_refs']) else ''
        ordinance_refs = ordinance_refs.replace('\\', '\\\\').replace('"', '\\"')
        
        outcome = str(row['outcome'])[:200] if pd.notna(row['outcome']) else ''
        outcome = outcome.replace('\\', '\\\\').replace('"""', "'''").replace('\n', ' ')
        
        sentence = str(row['sentence']) if pd.notna(row['sentence']) else ''
        sentence = sentence.replace('\\', '\\\\').replace('"', '\\"')
        
        keywords_list = str(row['keywords']).split(', ') if pd.notna(row['keywords']) else []
        keywords_str = '", "'.join(keywords_list[:6])  # Limit to 6 keywords
        
        # Derive legal principles from facts/outcome
        legal_principles = []
        if 'appeal' in outcome.lower() and 'dismissed' in outcome.lower():
            legal_principles.append("Appeal dismissed - conviction upheld")
        elif 'appeal' in outcome.lower() and 'allowed' in outcome.lower():
            legal_principles.append("Appeal allowed")
        if 'sentence' in outcome.lower() and 'reduced' in outcome.lower():
            legal_principles.append("Sentence reduced on appeal")
        
        if not legal_principles:
            legal_principles = ["Criminal appeal principles apply"]
        
        legal_principles_str = '",\n            "'.join(legal_principles)
        
        python_code += f'''    CriminalCase(
        case_id="{row['case_id']}",
        case_name="{case_name}",
        year={row['year']},
        court="Court of Appeal",
        facts="""{facts}""",
        charges="""{charges}""",
        ordinance_refs="{ordinance_refs}",
        outcome="""{outcome}""",
        sentence="{sentence}",
        legal_principles=[
            "{legal_principles_str}"
        ],
        keywords=["{keywords_str}"]
    ),
'''
    
    # Add footer
    python_code += ''']

# Categorize cases
CASES_BY_CATEGORY = {}
for case in ALL_CRIMINAL_CASES:
    for keyword in case.keywords:
        if keyword not in CASES_BY_CATEGORY:
            CASES_BY_CATEGORY[keyword] = []
        CASES_BY_CATEGORY[keyword].append(case)

# All cases list (for backward compatibility)
ALL_CASES = ALL_CRIMINAL_CASES
ALL_LEGAL_CASES = ALL_CRIMINAL_CASES

# Statistics
TOTAL_CASES = len(ALL_CASES)

def get_case_by_id(case_id):
    """Get case by ID"""
    for case in ALL_CASES:
        if case.case_id == case_id:
            return case
    return None

def search_cases_by_keyword(keyword):
    """Search cases by keyword"""
    keyword_lower = keyword.lower()
    results = []
    for case in ALL_CASES:
        if keyword_lower in ' '.join(case.keywords).lower():
            results.append(case)
    return results

# Export
__all__ = [
    'CriminalCase',
    'ALL_CASES',
    'ALL_CRIMINAL_CASES',
    'ALL_LEGAL_CASES',
    'TOTAL_CASES',
    'CASES_BY_CATEGORY',
    'get_case_by_id',
    'search_cases_by_keyword'
]

if __name__ == '__main__':
    print(f"Hong Kong Criminal Appeal Cases Database")
    print(f"Total cases: {TOTAL_CASES}")
    print(f"\\nSample cases:")
    for case in ALL_CASES[:3]:
        print(f"  - {case}")
'''
    
    # Write to file
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(python_code)
    
    print(f"✅ Generated Python code: {output_path}")
    print(f"   Total cases: {len(df)}")
    print()

def main():
    """Main entry point"""
    print("=" * 80)
    print("CSV TO PYTHON CONVERTER")
    print("=" * 80)
    print()
    
    csv_path = project_root / "knowledge_base" / "real_cases.csv"
    output_path = project_root / "knowledge_base" / "all_cases_database.py"
    
    if not csv_path.exists():
        print(f"❌ CSV file not found: {csv_path}")
        print("   Please run parse_court_cases.py first")
        return 1
    
    # Backup old database
    if output_path.exists():
        backup_path = project_root / "knowledge_base" / "all_cases_database_OLD.py"
        import shutil
        shutil.copy(output_path, backup_path)
        print(f"📦 Backed up old database to: {backup_path}")
        print()
    
    # Convert CSV to Python
    csv_to_python_cases(csv_path, output_path)
    
    print("=" * 80)
    print("✅ CONVERSION COMPLETE!")
    print("=" * 80)
    print()
    print("Next steps:")
    print("1. Review knowledge_base/all_cases_database.py")
    print("2. Test case search: python query.py --mode cases 'drug'")
    print("3. Rebuild case embeddings: python -m knowledge_base.embeddings_index --rebuild")
    print("4. Add disclaimers to web UI")
    print()
    
    return 0

if __name__ == '__main__':
    sys.exit(main())

