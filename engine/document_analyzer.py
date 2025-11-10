"""
Document Analyzer for Legal Text
Extracts facts and identifies legal issues from documents
"""

import re
from collections import Counter

class DocumentAnalyzer:
    """
    Analyzes legal documents to extract facts and identify issues
    """
    
    # Keywords for identifying legal facts
    FACT_KEYWORDS = {
        'theft': ['took', 'steal', 'stole', 'stolen', 'appropriat', 'without paying', 'shoplifting'],
        'robbery': ['rob', 'force', 'threat', 'weapon', 'knife', 'gun', 'demanded'],
        'assault': ['punch', 'hit', 'struck', 'attack', 'beat', 'assault', 'injur', 'harm'],
        'murder': ['kill', 'murder', 'stab', 'shot', 'death', 'died', 'fatal'],
        'drugs': ['drug', 'cocaine', 'heroin', 'methamphetamine', 'cannabis', 'possess', 'trafficking'],
        'fraud': ['fraud', 'deceit', 'false representation', 'scam', 'cheat', 'mislead'],
        'sexual': ['rape', 'sexual', 'intercourse', 'indecent', 'consent', 'molest'],
        'property_damage': ['damage', 'destroy', 'vandal', 'arson', 'fire', 'burn'],
        'burglary': ['burgl', 'break', 'enter', 'trespass', 'residence'],
    }
    
    # Intent keywords
    INTENT_KEYWORDS = {
        'dishonestly': ['dishonest', 'fraud', 'deceit', 'cheat'],
        'intent_to_permanently_deprive': ['keep', 'permanently', 'never return', 'steal'],
        'maliciously': ['malicious', 'deliberate', 'intentional'],
        'recklessly': ['reckless', 'careless', 'disregard'],
    }
    
    # Action keywords
    ACTION_KEYWORDS = {
        'appropriates_property': ['took', 'taken', 'steal', 'appropriat'],
        'uses_force': ['force', 'violent', 'push', 'hit', 'strike'],
        'enters_building': ['enter', 'break in', 'trespass'],
        'causes_harm': ['injur', 'harm', 'hurt', 'wound'],
    }
    
    def __init__(self):
        pass
    
    def analyze_document(self, text):
        """
        Analyze a document and extract legal facts
        
        Args:
            text: Document text
        
        Returns:
            dict: Analysis results including facts, issues, and keywords
        """
        text_lower = text.lower()
        
        # Extract identified offences
        offences = self._identify_offences(text_lower)
        
        # Extract facts
        facts = self._extract_facts(text_lower)
        
        # Extract key information
        parties = self._extract_parties(text)
        dates = self._extract_dates(text)
        amounts = self._extract_amounts(text)
        locations = self._extract_locations(text)
        
        # Identify legal issues
        legal_issues = self._identify_legal_issues(offences, facts)
        
        # Generate summary
        summary = self._generate_summary(text, offences, facts)
        
        return {
            'offences': offences,
            'facts': facts,
            'parties': parties,
            'dates': dates,
            'amounts': amounts,
            'locations': locations,
            'legal_issues': legal_issues,
            'summary': summary,
            'text_length': len(text),
            'word_count': len(text.split())
        }
    
    def _identify_offences(self, text_lower):
        """Identify potential offences mentioned in text"""
        offences = []
        
        for offence_type, keywords in self.FACT_KEYWORDS.items():
            count = sum(1 for kw in keywords if kw in text_lower)
            if count > 0:
                offences.append({
                    'type': offence_type,
                    'confidence': min(count * 0.2, 1.0),
                    'keyword_matches': count
                })
        
        # Sort by confidence
        offences.sort(key=lambda x: x['confidence'], reverse=True)
        return offences
    
    def _extract_facts(self, text_lower):
        """Extract legal facts from text"""
        facts = []
        
        # Check for common fact patterns
        fact_patterns = {
            'property_belongs_to_another': ['belong to', 'owned by', 'property of', 'not his', 'not hers'],
            'acts_dishonestly': ['dishonest', 'without permission', 'without consent', 'secretly'],
            'intent_to_permanently_deprive': ['intend to keep', 'never return', 'permanently', 'steal'],
            'uses_force_or_threat': ['threaten', 'force', 'violence', 'weapon', 'scared', 'fear'],
            'victim_does_not_consent': ['no consent', 'refused', 'said no', 'unwilling', 'against will'],
            'unlawfully': ['unlawful', 'illegal', 'without authority', 'without permission'],
            'enters_building': ['enter', 'went into', 'broke into', 'trespass'],
            'as_trespasser': ['trespass', 'without permission', 'not allowed', 'uninvited'],
            'causes_actual_bodily_harm': ['injur', 'bruise', 'bleeding', 'pain', 'hospital'],
            'causes_gbh': ['serious injur', 'severe harm', 'fracture', 'permanent', 'surgery'],
        }
        
        for fact, patterns in fact_patterns.items():
            if any(pattern in text_lower for pattern in patterns):
                facts.append(fact)
        
        return facts
    
    def _extract_parties(self, text):
        """Extract names of parties involved"""
        # Simple pattern matching for names (capitalized words)
        name_pattern = r'\b([A-Z][a-z]+ [A-Z][a-z]+)\b'
        names = re.findall(name_pattern, text)
        return list(set(names))
    
    def _extract_dates(self, text):
        """Extract dates from text"""
        # Match various date formats
        date_patterns = [
            r'\d{1,2}[/-]\d{1,2}[/-]\d{2,4}',  # DD/MM/YYYY or DD-MM-YYYY
            r'\d{4}[/-]\d{1,2}[/-]\d{1,2}',    # YYYY/MM/DD
            r'\b\d{1,2}\s+(January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{4}\b',
            r'\b(Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday),?\s+\d{1,2}\s+(January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{4}\b'
        ]
        
        dates = []
        for pattern in date_patterns:
            dates.extend(re.findall(pattern, text, re.IGNORECASE))
        
        return list(set(dates))
    
    def _extract_amounts(self, text):
        """Extract monetary amounts"""
        # Match HK$ amounts
        amount_pattern = r'HK\$\s*[\d,]+(?:\.\d{2})?'
        amounts = re.findall(amount_pattern, text, re.IGNORECASE)
        return list(set(amounts))
    
    def _extract_locations(self, text):
        """Extract location names"""
        # Common HK locations
        hk_locations = [
            'Central', 'Causeway Bay', 'Mong Kok', 'Tsim Sha Tsui', 'Wan Chai',
            'Sham Shui Po', 'Yau Ma Tei', 'Jordan', 'Admiralty', 'Sheung Wan',
            'North Point', 'Quarry Bay', 'Tai Koo', 'Kowloon', 'Hong Kong Island',
            'New Territories', 'Nathan Road', 'MTR'
        ]
        
        locations = []
        for loc in hk_locations:
            if loc.lower() in text.lower():
                locations.append(loc)
        
        return locations
    
    def _identify_legal_issues(self, offences, facts):
        """Identify legal issues based on offences and facts"""
        issues = []
        
        if not offences:
            return ["Unable to identify specific legal issues. More information needed."]
        
        top_offence = offences[0]['type']
        
        issue_map = {
            'theft': [
                "Was there dishonest appropriation of property?",
                "Did the property belong to another?",
                "Was there intent to permanently deprive?",
                "Were all elements of theft satisfied?"
            ],
            'robbery': [
                "Was force or threat of force used?",
                "Was the force used immediately before or during the theft?",
                "Did the victim fear violence?",
                "Does this constitute robbery under s.10 Cap. 200?"
            ],
            'assault': [
                "What level of harm was caused?",
                "Was there intent to cause harm?",
                "Was the assault lawful (e.g., self-defense)?",
                "Does this constitute ABH, GBH, or common assault?"
            ],
            'murder': [
                "Was the killing unlawful?",
                "Was there malice aforethought?",
                "Was death caused by defendant's actions?",
                "Are there any defenses (provocation, diminished responsibility)?"
            ],
            'drugs': [
                "Was the defendant in possession of dangerous drugs?",
                "Did the defendant know the substance was a drug?",
                "Was there intent to supply/traffic?",
                "What quantity was involved?"
            ],
            'fraud': [
                "Was there a false representation?",
                "Did the defendant act dishonestly?",
                "Was there intent to gain or cause loss?",
                "Did anyone rely on the false representation?"
            ],
            'sexual': [
                "Was there consent?",
                "Did the defendant know or was reckless about non-consent?",
                "Was the act of a sexual nature?",
                "Are there any age-related issues?"
            ]
        }
        
        issues = issue_map.get(top_offence, ["General criminal liability issues"])
        
        return issues
    
    def _generate_summary(self, text, offences, facts):
        """Generate a brief summary of the document"""
        summary = []
        
        if offences:
            top_offences = [o['type'].replace('_', ' ').title() for o in offences[:3]]
            summary.append(f"Potential offences: {', '.join(top_offences)}")
        
        if facts:
            summary.append(f"Identified {len(facts)} relevant legal facts")
        
        if len(text) > 500:
            summary.append("Detailed factual scenario provided")
        
        return " | ".join(summary) if summary else "Brief description"
    
    def extract_for_inference(self, text):
        """
        Extract facts suitable for inference engine
        
        Args:
            text: Document text
        
        Returns:
            list: List of fact strings for inference engine
        """
        analysis = self.analyze_document(text)
        return analysis['facts']
    
    def generate_report(self, text):
        """
        Generate comprehensive analysis report
        
        Args:
            text: Document text
        
        Returns:
            Formatted report string
        """
        analysis = self.analyze_document(text)
        
        report = []
        report.append("=" * 70)
        report.append("DOCUMENT ANALYSIS REPORT")
        report.append("=" * 70)
        report.append("")
        
        report.append(f"Document Length: {analysis['word_count']} words")
        report.append(f"Summary: {analysis['summary']}")
        report.append("")
        
        report.append("POTENTIAL OFFENCES:")
        if analysis['offences']:
            for idx, offence in enumerate(analysis['offences'][:5], 1):
                report.append(f"  {idx}. {offence['type'].replace('_', ' ').title()} "
                            f"(Confidence: {offence['confidence']:.1%})")
        else:
            report.append("  None identified")
        report.append("")
        
        report.append("EXTRACTED FACTS:")
        if analysis['facts']:
            for fact in analysis['facts']:
                report.append(f"  - {fact.replace('_', ' ')}")
        else:
            report.append("  None identified")
        report.append("")
        
        if analysis['parties']:
            report.append("PARTIES INVOLVED:")
            for party in analysis['parties']:
                report.append(f"  - {party}")
            report.append("")
        
        if analysis['dates']:
            report.append("DATES:")
            for date in analysis['dates']:
                report.append(f"  - {date}")
            report.append("")
        
        if analysis['amounts']:
            report.append("MONETARY AMOUNTS:")
            for amount in analysis['amounts']:
                report.append(f"  - {amount}")
            report.append("")
        
        if analysis['locations']:
            report.append("LOCATIONS:")
            for loc in analysis['locations']:
                report.append(f"  - {loc}")
            report.append("")
        
        report.append("LEGAL ISSUES TO CONSIDER:")
        for issue in analysis['legal_issues']:
            report.append(f"  - {issue}")
        report.append("")
        
        report.append("=" * 70)
        
        return "\n".join(report)


if __name__ == '__main__':
    print("=== Testing Document Analyzer ===\n")
    
    analyzer = DocumentAnalyzer()
    
    # Test document
    test_doc = """
    On 15 May 2023, the defendant Chan Tai Man entered a jewelry store in Mong Kok
    at around 10 PM. He threatened the shop keeper with a knife and demanded she open
    the safe. Fearing for her life, she complied. The defendant took jewelry worth 
    HK$500,000 and fled. He was arrested the next day. The jewelry was not recovered.
    The defendant admitted he intended to keep the jewelry and sell it.
    """
    
    print("TEST DOCUMENT:")
    print(test_doc)
    print("\n")
    
    # Generate report
    report = analyzer.generate_report(test_doc)
    print(report)
    
    print("\n\nFACTS FOR INFERENCE ENGINE:")
    facts = analyzer.extract_for_inference(test_doc)
    for fact in facts:
        print(f"  - {fact}")

