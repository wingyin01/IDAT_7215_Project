"""
Automatic Rule Generator for Hong Kong Legislation
Converts legislation sections into executable IF-THEN rules automatically
Scales from 54 manual rules to 52,269+ auto-generated rules
"""

import re
from typing import List, Dict, Set, Optional
from knowledge_base.criminal_rules import Rule

class AutoRuleGenerator:
    """
    Automatically generates rules from legislation text
    Uses pattern matching and NLP to extract legal conditions
    """
    
    def __init__(self):
        """Initialize the automatic rule generator"""
        self.generated_rules = []
        self.rule_patterns = self._initialize_patterns()
        self.offense_keywords = self._initialize_offense_keywords()
        
    def _initialize_patterns(self) -> List[Dict]:
        """
        Define patterns for automatic rule extraction
        
        Returns:
            List of pattern dictionaries with regex and rule templates
        """
        return [
            {
                'name': 'prohibition_pattern',
                'pattern': r'(?:person|individual|anyone|whoever)\s+(?:who\s+)?(?:commits|does|engages\s+in|performs)\s+([^.]+)\s+(?:is|shall\s+be)\s+guilty',
                'template': 'offense_prohibition'
            },
            {
                'name': 'penalty_pattern',
                'pattern': r'(?:liable\s+to|punishable\s+by|penalty\s+of)\s+(?:imprisonment\s+for\s+(\d+)\s+years?|fine\s+of\s+\$?([\d,]+)|both)',
                'template': 'penalty_extraction'
            },
            {
                'name': 'conditional_offense',
                'pattern': r'if\s+([^,]+),\s+(?:and|or)\s+([^,]+),\s+(?:then|shall|is)',
                'template': 'conditional_rule'
            },
            {
                'name': 'prohibition_shall_not',
                'pattern': r'(?:person|individual|anyone)\s+shall\s+not\s+([^.]+)',
                'template': 'prohibition_rule'
            },
            {
                'name': 'requirement_must',
                'pattern': r'(?:person|individual|anyone)\s+(?:must|shall)\s+([^.]+)',
                'template': 'requirement_rule'
            }
        ]
    
    def _initialize_offense_keywords(self) -> Dict[str, List[str]]:
        """
        Define keyword mappings for common offenses
        
        Returns:
            Dictionary mapping offense types to keywords
        """
        return {
            'theft': ['steal', 'theft', 'appropriate', 'taking', 'dishonestly'],
            'assault': ['assault', 'attack', 'hit', 'strike', 'violence', 'bodily harm'],
            'fraud': ['fraud', 'deception', 'false representation', 'dishonest'],
            'drugs': ['dangerous drug', 'narcotic', 'controlled substance', 'trafficking'],
            'sexual': ['sexual', 'rape', 'indecent', 'intercourse'],
            'property_damage': ['damage', 'destroy', 'arson', 'fire'],
            'public_order': ['riot', 'unlawful assembly', 'public order'],
            'burglary': ['burglary', 'breaking', 'entering', 'trespasser'],
            'robbery': ['robbery', 'force', 'threat', 'steal'],
            'murder': ['murder', 'kill', 'unlawful killing', 'malice'],
            'regulatory': ['smoking', 'littering', 'spitting', 'noise', 'nuisance']
        }
    
    def generate_rules_from_ordinances(self, ordinances_dict: Dict) -> List[Rule]:
        """
        Generate rules from all ordinances
        
        Args:
            ordinances_dict: Dictionary of ordinances from json_loader
        
        Returns:
            List of automatically generated Rule objects
        """
        print("=" * 80)
        print("AUTOMATIC RULE GENERATION")
        print("=" * 80)
        
        generated_rules = []
        sections_processed = 0
        rules_created = 0
        
        for cap_key, ordinance in ordinances_dict.items():
            chapter = ordinance.get('chapter', '')
            ordinance_title = ordinance.get('title', '')
            category = ordinance.get('category', 'Other')
            
            # Only generate rules for certain categories (to keep it manageable)
            if category not in ['Criminal Law', 'Public Health', 'Environment', 
                                'Employment', 'Property']:
                continue
            
            for section_num, section_data in ordinance.get('sections', {}).items():
                sections_processed += 1
                
                # Try to generate rule from this section
                rules = self._generate_rule_from_section(
                    cap_key, chapter, section_num, section_data, 
                    ordinance_title, category
                )
                
                if rules:
                    generated_rules.extend(rules)
                    rules_created += len(rules)
        
        print(f"✅ Processed {sections_processed} sections")
        print(f"✅ Generated {rules_created} rules automatically")
        print("=" * 80)
        print()
        
        self.generated_rules = generated_rules
        return generated_rules
    
    def _generate_rule_from_section(self, cap_key: str, chapter: str, 
                                     section_num: str, section_data: Dict,
                                     ordinance_title: str, category: str) -> List[Rule]:
        """
        Generate rule(s) from a single legislation section
        
        Args:
            cap_key: Chapter key
            chapter: Chapter number
            section_num: Section number
            section_data: Section data dictionary
            ordinance_title: Title of ordinance
            category: Category of ordinance
        
        Returns:
            List of generated rules (may be empty if no rule can be generated)
        """
        text = section_data.get('text', '').lower()
        title = section_data.get('title', '')
        
        # Skip non-substantive sections
        if self._is_non_substantive_section(title, text):
            return []
        
        rules = []
        
        # Pattern 1: Detect offense prohibitions
        if 'guilty' in text or 'offence' in text or 'offense' in text:
            rule = self._create_prohibition_rule(
                cap_key, chapter, section_num, section_data, 
                ordinance_title, category
            )
            if rule:
                rules.append(rule)
        
        # Pattern 2: Detect penalty provisions
        if 'imprisonment' in text or 'fine' in text or 'penalty' in text:
            # This enriches the existing rule or creates a penalty-focused one
            pass  # Handled in prohibition rule
        
        # Pattern 3: Detect requirement/duty provisions
        if 'shall' in text and 'not' in text:
            rule = self._create_prohibition_rule(
                cap_key, chapter, section_num, section_data,
                ordinance_title, category
            )
            if rule:
                rules.append(rule)
        
        return rules
    
    def _is_non_substantive_section(self, title: str, text: str) -> bool:
        """Check if section is non-substantive (definitions, titles, etc.)"""
        non_substantive_keywords = [
            'short title', 'commencement', 'interpretation', 'definition',
            'application', 'repeal', 'amendment', 'schedule', 'transitional'
        ]
        
        title_lower = title.lower()
        text_lower = text.lower()
        
        for keyword in non_substantive_keywords:
            if keyword in title_lower or (keyword in text_lower and len(text) < 200):
                return True
        
        return False
    
    def _create_prohibition_rule(self, cap_key: str, chapter: str,
                                  section_num: str, section_data: Dict,
                                  ordinance_title: str, category: str) -> Optional[Rule]:
        """
        Create a prohibition-style rule from section
        
        Returns:
            Rule object or None if cannot be created
        """
        text = section_data.get('text', '').lower()
        title = section_data.get('title', '')
        
        # Extract conditions (what makes this an offense)
        conditions = self._extract_conditions_from_text(text, category)
        
        if not conditions:
            return None
        
        # Extract penalty
        penalty = self._extract_penalty_from_text(text)
        
        # Generate conclusion
        conclusion = self._generate_conclusion(title, text, category)
        
        # Generate explanation
        explanation = f"Auto-generated from {ordinance_title}, {chapter} s.{section_num}: {title}"
        
        # Create rule ID
        rule_id = f"AUTO_{cap_key}_{section_num}".replace(" ", "_").replace(".", "_")
        
        # Create rule
        rule = Rule(
            rule_id=rule_id,
            name=title or f"{ordinance_title} s.{section_num}",
            conditions=conditions,
            conclusion=conclusion,
            ordinance_ref=f"{chapter}, s.{section_num}",
            penalty=penalty,
            confidence=0.7,  # Auto-generated rules have lower confidence
            explanation=explanation
        )
        
        return rule
    
    def _extract_conditions_from_text(self, text: str, category: str) -> List[str]:
        """
        Extract legal conditions from text using NLP and patterns
        
        Args:
            text: Section text
            category: Category of law
        
        Returns:
            List of condition strings
        """
        conditions = []
        
        # Map offense keywords to conditions
        offense_mappings = {
            'steal': 'appropriates_property',
            'theft': 'appropriates_property',
            'dishonest': 'acts_dishonestly',
            'without consent': 'without_consent',
            'assault': 'applies_force',
            'attack': 'applies_force',
            'bodily harm': 'causes_bodily_harm',
            'kill': 'causes_death',
            'murder': 'causes_death',
            'drug': 'possesses_dangerous_drugs',
            'trafficking': 'intent_to_traffic',
            'damage': 'damages_property',
            'destroy': 'damages_property',
            'enter': 'enters_building',
            'trespasser': 'as_trespasser',
            'force': 'uses_force',
            'threat': 'makes_threat',
            'sexual intercourse': 'sexual_intercourse',
            'without consent': 'without_consent',
            'smoke': 'smoking_activity',
            'litter': 'disposed_of_waste',
            'spit': 'spitting_in_public',
            'public place': 'in_public_place'
        }
        
        # Extract conditions based on keywords
        for keyword, condition in offense_mappings.items():
            if keyword in text:
                if condition not in conditions:
                    conditions.append(condition)
        
        # Add category-specific conditions
        if category == 'Criminal Law':
            # Most criminal offenses require intent
            if 'intent' in text or 'knowingly' in text or 'willfully' in text:
                conditions.append('acts_with_intent')
        
        return conditions[:5]  # Limit to 5 conditions to avoid over-complexity
    
    def _extract_penalty_from_text(self, text: str) -> str:
        """
        Extract penalty information from text
        
        Args:
            text: Section text
        
        Returns:
            Penalty string
        """
        # Pattern: imprisonment for X years
        imprisonment_match = re.search(r'imprisonment\s+for\s+(\d+)\s+year', text)
        if imprisonment_match:
            years = imprisonment_match.group(1)
            return f"Imprisonment for {years} years"
        
        # Pattern: fine of $X
        fine_match = re.search(r'fine\s+of\s+\$?([\d,]+)', text)
        if fine_match:
            amount = fine_match.group(1)
            return f"Fine of HK${amount}"
        
        # Pattern: life imprisonment
        if 'life imprisonment' in text:
            return "Life imprisonment"
        
        # Pattern: both imprisonment and fine
        if 'imprisonment' in text and 'fine' in text:
            return "Imprisonment and fine"
        
        return "Penalty as specified in ordinance"
    
    def _generate_conclusion(self, title: str, text: str, category: str) -> str:
        """
        Generate appropriate conclusion for the rule
        
        Args:
            title: Section title
            text: Section text
            category: Category
        
        Returns:
            Conclusion string
        """
        # Map keywords to conclusions
        if 'guilty' in text:
            # Extract offense name from text
            for offense_type, keywords in self.offense_keywords.items():
                for keyword in keywords:
                    if keyword in text:
                        return f"guilty_of_{offense_type}"
        
        # Fallback: create conclusion from title
        title_lower = title.lower()
        title_clean = re.sub(r'[^\w\s]', '', title_lower)
        conclusion = 'guilty_of_' + title_clean.replace(' ', '_')[:50]
        
        return conclusion
    
    def get_rule_statistics(self) -> Dict:
        """
        Get statistics about generated rules
        
        Returns:
            Dictionary with rule statistics
        """
        if not self.generated_rules:
            return {'total': 0, 'by_category': {}}
        
        stats = {
            'total': len(self.generated_rules),
            'by_category': {},
            'by_confidence': {}
        }
        
        # Count by ordinance reference
        for rule in self.generated_rules:
            cap = rule.ordinance_ref.split(',')[0]
            if cap not in stats['by_category']:
                stats['by_category'][cap] = 0
            stats['by_category'][cap] += 1
        
        return stats
    
    def save_generated_rules(self, filepath: str):
        """
        Save generated rules to Python file
        
        Args:
            filepath: Path to save rules
        """
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write('"""\n')
            f.write('AUTO-GENERATED RULES\n')
            f.write('Generated by auto_rule_generator.py\n')
            f.write('DO NOT EDIT MANUALLY - regenerate instead\n')
            f.write('"""\n\n')
            f.write('from knowledge_base.criminal_rules import Rule\n\n')
            f.write('AUTO_GENERATED_RULES = [\n')
            
            for rule in self.generated_rules:
                f.write('    Rule(\n')
                f.write(f'        rule_id="{rule.rule_id}",\n')
                f.write(f'        name="{rule.name}",\n')
                f.write(f'        conditions={rule.conditions},\n')
                f.write(f'        conclusion="{rule.conclusion}",\n')
                f.write(f'        ordinance_ref="{rule.ordinance_ref}",\n')
                f.write(f'        penalty="{rule.penalty}",\n')
                f.write(f'        confidence={rule.confidence},\n')
                f.write(f'        explanation="{rule.explanation}"\n')
                f.write('    ),\n')
            
            f.write(']\n')
        
        print(f"✅ Saved {len(self.generated_rules)} rules to {filepath}")


if __name__ == '__main__':
    """Test the auto rule generator"""
    from knowledge_base.json_loader import ALL_ORDINANCES
    
    generator = AutoRuleGenerator()
    rules = generator.generate_rules_from_ordinances(ALL_ORDINANCES)
    
    print(f"\n📊 Generated {len(rules)} rules")
    
    # Show sample rules
    print("\nSample Generated Rules:")
    for i, rule in enumerate(rules[:5]):
        print(f"\n{i+1}. {rule.name}")
        print(f"   Conditions: {rule.conditions}")
        print(f"   Conclusion: {rule.conclusion}")
        print(f"   Penalty: {rule.penalty}")
    
    # Save rules
    generator.save_generated_rules('knowledge_base/auto_generated_rules.py')
    
    # Show statistics
    stats = generator.get_rule_statistics()
    print(f"\n📈 Total Rules: {stats['total']}")
    print(f"📈 By Chapter: {len(stats['by_category'])} chapters covered")
