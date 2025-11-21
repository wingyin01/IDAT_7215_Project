"""
Enhanced Rule Engine with Auto-Generated Rules
Combines 54 manual rules + auto-generated rules + RAG fallback
Scales to cover all 52,269 HK legislation sections intelligently
"""

from typing import List, Dict, Set, Tuple
from knowledge_base.all_legal_rules import ALL_LEGAL_RULES, RULE_DICT
from knowledge_base.criminal_rules import Rule
from engine.auto_rule_generator import AutoRuleGenerator
from engine.hybrid_search import HybridSearchEngine

class EnhancedRuleEngine:
    """
    Enhanced rule engine that combines:
    1. Manual rules (54 high-quality rules)
    2. Auto-generated rules (from legislation)
    3. Hybrid search fallback (for uncovered scenarios)
    """
    
    def __init__(self, ordinances_dict=None, use_auto_rules=True):
        """
        Initialize enhanced rule engine
        
        Args:
            ordinances_dict: Legislation database
            use_auto_rules: Whether to generate automatic rules
        """
        print("=" * 80)
        print("ENHANCED RULE ENGINE INITIALIZATION")
        print("=" * 80)
        
        # Manual rules (high confidence)
        self.manual_rules = ALL_LEGAL_RULES
        print(f"✅ Loaded {len(self.manual_rules)} manual rules")
        
        # Auto-generated rules (medium confidence)
        self.auto_rules = []
        if use_auto_rules and ordinances_dict:
            print("🔄 Generating automatic rules from legislation...")
            generator = AutoRuleGenerator()
            self.auto_rules = generator.generate_rules_from_ordinances(ordinances_dict)
            print(f"✅ Generated {len(self.auto_rules)} automatic rules")
        
        # Combined rule set
        self.all_rules = self.manual_rules + self.auto_rules
        
        # Hybrid search for fallback
        self.hybrid_search = None
        if ordinances_dict:
            print("🔄 Initializing hybrid search for fallback...")
            self.hybrid_search = HybridSearchEngine()
            self.hybrid_search.index_legislation(ordinances_dict)
            print("✅ Hybrid search ready")
        
        # Statistics
        self.stats = {
            'manual_rules': len(self.manual_rules),
            'auto_rules': len(self.auto_rules),
            'total_rules': len(self.all_rules),
            'queries_handled': 0,
            'manual_rule_matches': 0,
            'auto_rule_matches': 0,
            'fallback_searches': 0
        }
        
        print("=" * 80)
        print(f"✅ Enhanced Rule Engine Ready")
        print(f"   Manual Rules: {len(self.manual_rules)}")
        print(f"   Auto Rules: {len(self.auto_rules)}")
        print(f"   Total Coverage: {len(self.all_rules)} rules")
        print("=" * 80)
        print()
    
    def analyze(self, facts: Set[str], query_text: str = "") -> Dict:
        """
        Analyze scenario using enhanced rule engine
        
        Args:
            facts: Set of extracted facts
            query_text: Original query text (for fallback search)
        
        Returns:
            Analysis results with matched rules and fallback results
        """
        self.stats['queries_handled'] += 1
        
        results = {
            'matched_rules': [],
            'rule_source': [],  # 'manual' or 'auto' or 'fallback'
            'confidence': 0.0,
            'fallback_sections': [],
            'coverage': 'full'  # 'full', 'partial', or 'fallback'
        }
        
        # Step 1: Try manual rules first (highest confidence)
        manual_matches = self._match_rules(facts, self.manual_rules)
        if manual_matches:
            results['matched_rules'].extend(manual_matches)
            results['rule_source'].extend(['manual'] * len(manual_matches))
            results['confidence'] = 1.0
            results['coverage'] = 'full'
            self.stats['manual_rule_matches'] += len(manual_matches)
            return results
        
        # Step 2: Try auto-generated rules (medium confidence)
        auto_matches = self._match_rules(facts, self.auto_rules)
        if auto_matches:
            results['matched_rules'].extend(auto_matches)
            results['rule_source'].extend(['auto'] * len(auto_matches))
            results['confidence'] = 0.7
            results['coverage'] = 'full'
            self.stats['auto_rule_matches'] += len(auto_matches)
            return results
        
        # Step 3: Fallback to hybrid search if no rules match
        if self.hybrid_search and query_text:
            print("⚠️  No matching rules found. Using hybrid search fallback...")
            fallback_results = self._fallback_search(query_text, facts)
            results['fallback_sections'] = fallback_results
            results['confidence'] = 0.5
            results['coverage'] = 'fallback'
            self.stats['fallback_searches'] += 1
            return results
        
        # No matches at all
        results['coverage'] = 'none'
        return results
    
    def _match_rules(self, facts: Set[str], rule_set: List[Rule]) -> List[Rule]:
        """
        Match facts against a set of rules
        
        Args:
            facts: Set of facts
            rule_set: List of rules to check
        
        Returns:
            List of matched rules
        """
        matched = []
        for rule in rule_set:
            if rule.matches(facts):
                matched.append(rule)
        return matched
    
    def _fallback_search(self, query_text: str, facts: Set[str]) -> List[Dict]:
        """
        Fallback to hybrid search when no rules match
        
        Args:
            query_text: Original query
            facts: Extracted facts
        
        Returns:
            List of relevant legislation sections
        """
        # Combine query text with facts for better search
        enhanced_query = query_text + " " + " ".join(facts)
        
        # Search legislation
        results = self.hybrid_search.search(
            enhanced_query,
            top_k=5,
            source='legislation'
        )
        
        return results
    
    def explain_analysis(self, results: Dict) -> str:
        """
        Generate human-readable explanation of analysis
        
        Args:
            results: Analysis results from analyze()
        
        Returns:
            Explanation string
        """
        explanation = []
        
        if results['coverage'] == 'full':
            if 'manual' in results['rule_source']:
                explanation.append("✅ Matched using manual expert rules (high confidence)")
            elif 'auto' in results['rule_source']:
                explanation.append("✅ Matched using auto-generated rules (medium confidence)")
            
            explanation.append(f"\n📋 Found {len(results['matched_rules'])} applicable rule(s):\n")
            
            for i, rule in enumerate(results['matched_rules'], 1):
                explanation.append(f"{i}. {rule.name}")
                explanation.append(f"   Reference: {rule.ordinance_ref}")
                explanation.append(f"   Penalty: {rule.penalty}")
                explanation.append(f"   Confidence: {rule.confidence * 100:.0f}%\n")
        
        elif results['coverage'] == 'fallback':
            explanation.append("⚠️  No exact rule match found. Using hybrid search fallback.\n")
            explanation.append(f"📋 Found {len(results['fallback_sections'])} potentially relevant sections:\n")
            
            for i, section in enumerate(results['fallback_sections'], 1):
                metadata = section.get('metadata', {})
                explanation.append(f"{i}. {metadata.get('ordinance_title', 'Unknown')}")
                explanation.append(f"   {metadata.get('chapter', '')} s.{metadata.get('section', '')}")
                explanation.append(f"   Score: {section.get('score', 0):.2f}\n")
            
            explanation.append("💡 Recommendation: Use Expert Mode (RAG) for comprehensive analysis.")
        
        else:
            explanation.append("❌ No matching rules or relevant sections found.")
            explanation.append("💡 Please:\n")
            explanation.append("   1. Rephrase your query with more details")
            explanation.append("   2. Try Expert Mode (RAG) for better coverage")
            explanation.append("   3. Consult a legal professional")
        
        return "\n".join(explanation)
    
    def get_statistics(self) -> Dict:
        """Get usage statistics"""
        stats = self.stats.copy()
        
        if stats['queries_handled'] > 0:
            stats['manual_coverage'] = (stats['manual_rule_matches'] / stats['queries_handled']) * 100
            stats['auto_coverage'] = (stats['auto_rule_matches'] / stats['queries_handled']) * 100
            stats['fallback_rate'] = (stats['fallback_searches'] / stats['queries_handled']) * 100
        else:
            stats['manual_coverage'] = 0
            stats['auto_coverage'] = 0
            stats['fallback_rate'] = 0
        
        return stats
    
    def print_statistics(self):
        """Print usage statistics"""
        stats = self.get_statistics()
        
        print("\n" + "=" * 80)
        print("ENHANCED RULE ENGINE STATISTICS")
        print("=" * 80)
        print(f"Manual Rules: {stats['manual_rules']}")
        print(f"Auto Rules: {stats['auto_rules']}")
        print(f"Total Rules: {stats['total_rules']}")
        print()
        print(f"Queries Handled: {stats['queries_handled']}")
        print(f"Manual Rule Matches: {stats['manual_rule_matches']} ({stats['manual_coverage']:.1f}%)")
        print(f"Auto Rule Matches: {stats['auto_rule_matches']} ({stats['auto_coverage']:.1f}%)")
        print(f"Fallback Searches: {stats['fallback_searches']} ({stats['fallback_rate']:.1f}%)")
        print("=" * 80)
    
    def find_rule_gaps(self, common_scenarios: List[str]) -> Dict:
        """
        Identify gaps in rule coverage by testing common scenarios
        
        Args:
            common_scenarios: List of common legal scenarios
        
        Returns:
            Dictionary with gap analysis
        """
        gaps = {
            'covered_by_manual': [],
            'covered_by_auto': [],
            'not_covered': []
        }
        
        for scenario in common_scenarios:
            # This would need NLP to extract facts from scenario
            # Simplified for now
            facts = set()  # Would be extracted by document analyzer
            
            manual_matches = self._match_rules(facts, self.manual_rules)
            auto_matches = self._match_rules(facts, self.auto_rules)
            
            if manual_matches:
                gaps['covered_by_manual'].append(scenario)
            elif auto_matches:
                gaps['covered_by_auto'].append(scenario)
            else:
                gaps['not_covered'].append(scenario)
        
        return gaps


def demo_enhanced_engine():
    """Demo the enhanced rule engine"""
    from knowledge_base.json_loader import ALL_ORDINANCES
    
    print("\n" + "=" * 80)
    print("ENHANCED RULE ENGINE DEMO")
    print("=" * 80)
    
    # Initialize engine
    engine = EnhancedRuleEngine(ALL_ORDINANCES, use_auto_rules=True)
    
    # Test scenarios
    test_scenarios = [
        {
            'description': 'Theft scenario',
            'facts': {'appropriates_property', 'acts_dishonestly', 'property_belongs_to_another'},
            'query': 'Person stole a laptop'
        },
        {
            'description': 'Assault scenario',
            'facts': {'applies_force', 'without_consent', 'causes_bodily_harm'},
            'query': 'Person hit someone causing injury'
        },
        {
            'description': 'Unknown scenario (test fallback)',
            'facts': {'unknown_fact'},
            'query': 'Can I register a company while on work visa?'
        }
    ]
    
    for scenario in test_scenarios:
        print(f"\n{'=' * 80}")
        print(f"Test: {scenario['description']}")
        print(f"Query: {scenario['query']}")
        print(f"Facts: {scenario['facts']}")
        print(f"{'=' * 80}")
        
        results = engine.analyze(scenario['facts'], scenario['query'])
        explanation = engine.explain_analysis(results)
        print(explanation)
    
    # Print statistics
    engine.print_statistics()


if __name__ == '__main__':
    demo_enhanced_engine()
