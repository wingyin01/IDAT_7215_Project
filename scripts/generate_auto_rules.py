#!/usr/bin/env python3
"""
Script to Generate Automatic Rules from Legislation
Run this to expand from 54 manual rules to thousands of auto-generated rules
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from engine.auto_rule_generator import AutoRuleGenerator
from knowledge_base.json_loader import ALL_ORDINANCES

def main():
    """Generate automatic rules and save them"""
    
    print("\n" + "=" * 80)
    print("AUTOMATIC RULE GENERATION SCRIPT")
    print("=" * 80)
    print()
    
    # Check if legislation database is loaded
    if not ALL_ORDINANCES:
        print("❌ Error: Legislation database not loaded.")
        print("   Please run: python -m knowledge_base.preprocess_legislation")
        return
    
    print(f"📚 Loaded {len(ALL_ORDINANCES)} ordinances")
    
    # Initialize generator
    generator = AutoRuleGenerator()
    
    # Generate rules
    print("\n🔄 Starting automatic rule generation...")
    print("   This may take 10-30 seconds...\n")
    
    rules = generator.generate_rules_from_ordinances(ALL_ORDINANCES)
    
    # Show statistics
    stats = generator.get_rule_statistics()
    
    print("\n" + "=" * 80)
    print("GENERATION RESULTS")
    print("=" * 80)
    print(f"✅ Total Rules Generated: {stats['total']}")
    print(f"✅ Chapters Covered: {len(stats['by_category'])}")
    print()
    
    # Show top chapters by rule count
    print("Top Chapters by Rule Count:")
    sorted_chapters = sorted(stats['by_category'].items(), key=lambda x: x[1], reverse=True)
    for i, (chapter, count) in enumerate(sorted_chapters[:10], 1):
        print(f"   {i}. {chapter}: {count} rules")
    print()
    
    # Show sample rules
    print("=" * 80)
    print("SAMPLE GENERATED RULES")
    print("=" * 80)
    
    for i, rule in enumerate(rules[:10], 1):
        print(f"\n{i}. {rule.name}")
        print(f"   ID: {rule.rule_id}")
        print(f"   Ref: {rule.ordinance_ref}")
        print(f"   Conditions: {rule.conditions}")
        print(f"   Conclusion: {rule.conclusion}")
        print(f"   Penalty: {rule.penalty}")
        print(f"   Confidence: {rule.confidence}")
    
    # Save to file
    output_file = Path(__file__).parent.parent / 'knowledge_base' / 'auto_generated_rules.py'
    print(f"\n{'=' * 80}")
    print(f"Saving rules to: {output_file}")
    print(f"{'=' * 80}")
    
    generator.save_generated_rules(str(output_file))
    
    print("\n✅ SUCCESS!")
    print()
    print("Next Steps:")
    print("1. Import auto-generated rules in your rule engine")
    print("2. Test with: python scripts/test_enhanced_engine.py")
    print("3. Use in query.py with --use-auto-rules flag")
    print()


if __name__ == '__main__':
    main()
