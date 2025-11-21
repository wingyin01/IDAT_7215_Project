#!/usr/bin/env python3
"""
System Accuracy Evaluation Script
Measures actual performance metrics for all 8 algorithms
Generates results table for PPT/report
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import json
from typing import List, Dict, Set
from collections import defaultdict

# Import your system components
from engine.document_analyzer import DocumentAnalyzer
from engine.hybrid_search import HybridSearchEngine
from engine.enhanced_rule_engine import EnhancedRuleEngine
from engine.case_matcher import CaseMatcher
from knowledge_base.json_loader import ALL_ORDINANCES


class SystemEvaluator:
    """Evaluate accuracy of all system components"""
    
    def __init__(self):
        """Initialize all components for testing"""
        print("=" * 80)
        print("INITIALIZING SYSTEM FOR EVALUATION")
        print("=" * 80)
        
        self.nlp_analyzer = DocumentAnalyzer()
        self.hybrid_search = HybridSearchEngine()
        self.case_matcher = CaseMatcher()
        self.enhanced_engine = EnhancedRuleEngine(ALL_ORDINANCES, use_auto_rules=True)
        
        # Index legislation for search
        if ALL_ORDINANCES:
            self.hybrid_search.index_legislation(ALL_ORDINANCES)
        
        print("✅ All components initialized\n")
    
    def evaluate_nlp_accuracy(self, test_cases: List[Dict]) -> Dict:
        """
        Evaluate NLP fact extraction accuracy
        
        Test format:
        {
            "query": "Person stole laptop worth HK$50,000",
            "expected_facts": ["appropriates_property", "acts_dishonestly"],
            "expected_entities": {"amount": 50000}
        }
        """
        print("=" * 80)
        print("EVALUATING NLP FACT EXTRACTION")
        print("=" * 80)
        
        total_facts = 0
        correct_facts = 0
        total_entities = 0
        correct_entities = 0
        
        for i, case in enumerate(test_cases, 1):
            analysis = self.nlp_analyzer.analyze_document(case["query"])
            extracted_facts = set(analysis.get("facts", []))
            expected_facts = set(case.get("expected_facts", []))
            
            # Calculate fact accuracy
            if expected_facts:
                intersection = extracted_facts & expected_facts
                correct_facts += len(intersection)
                total_facts += len(expected_facts)
                
                fact_precision = len(intersection) / len(extracted_facts) if extracted_facts else 0
                fact_recall = len(intersection) / len(expected_facts) if expected_facts else 0
                
                print(f"Case {i}: {case['query'][:50]}...")
                print(f"  Expected: {expected_facts}")
                print(f"  Extracted: {extracted_facts}")
                print(f"  Precision: {fact_precision:.1%}, Recall: {fact_recall:.1%}")
        
        accuracy = correct_facts / total_facts if total_facts > 0 else 0
        
        print(f"\n{'=' * 80}")
        print(f"NLP FACT EXTRACTION ACCURACY: {accuracy:.1%}")
        print(f"Correct Facts: {correct_facts}/{total_facts}")
        print(f"{'=' * 80}\n")
        
        return {
            "accuracy": accuracy,
            "correct": correct_facts,
            "total": total_facts
        }
    
    def evaluate_search_accuracy(self, test_cases: List[Dict]) -> Dict:
        """
        Evaluate hybrid search precision@k
        
        Test format:
        {
            "query": "theft ordinance",
            "relevant_sections": ["Cap210_s2", "Cap210_s9"]
        }
        """
        print("=" * 80)
        print("EVALUATING HYBRID SEARCH")
        print("=" * 80)
        
        if not ALL_ORDINANCES:
            print("⚠️  No legislation loaded. Skipping search evaluation.")
            return {"precision_at_5": 0, "cases_tested": 0}
        
        precisions = []
        
        for i, case in enumerate(test_cases, 1):
            results = self.hybrid_search.search(
                case["query"], 
                top_k=5,
                source='legislation'
            )
            
            retrieved_ids = [r.get("metadata", {}).get("section_id", "") for r in results]
            relevant_sections = set(case["relevant_sections"])
            
            # Calculate precision@5
            relevant_in_top5 = sum(1 for rid in retrieved_ids if rid in relevant_sections)
            precision = relevant_in_top5 / 5 if len(retrieved_ids) >= 5 else 0
            precisions.append(precision)
            
            print(f"Case {i}: '{case['query']}'")
            print(f"  Relevant in top 5: {relevant_in_top5}/5")
            print(f"  Precision@5: {precision:.1%}")
        
        avg_precision = sum(precisions) / len(precisions) if precisions else 0
        
        print(f"\n{'=' * 80}")
        print(f"HYBRID SEARCH PRECISION@5: {avg_precision:.1%}")
        print(f"{'=' * 80}\n")
        
        return {
            "precision_at_5": avg_precision,
            "cases_tested": len(test_cases)
        }
    
    def evaluate_rule_engine_accuracy(self, test_cases: List[Dict]) -> Dict:
        """
        Evaluate rule engine accuracy
        
        Test format:
        {
            "facts": ["appropriates_property", "acts_dishonestly"],
            "query": "theft laptop",
            "expected_match": True,
            "expected_tier": 1  # 1=manual, 2=auto, 3=fallback
        }
        """
        print("=" * 80)
        print("EVALUATING ENHANCED RULE ENGINE")
        print("=" * 80)
        
        tier_stats = {1: {"correct": 0, "total": 0},
                      2: {"correct": 0, "total": 0},
                      3: {"correct": 0, "total": 0}}
        
        for i, case in enumerate(test_cases, 1):
            facts = set(case["facts"])
            results = self.enhanced_engine.analyze(facts, case.get("query", ""))
            
            expected_tier = case.get("expected_tier", 1)
            expected_match = case.get("expected_match", True)
            
            # Determine which tier was used
            if 'manual' in results.get('rule_source', []):
                actual_tier = 1
            elif 'auto' in results.get('rule_source', []):
                actual_tier = 2
            elif results.get('coverage') == 'fallback':
                actual_tier = 3
            else:
                actual_tier = 0  # No match
            
            # Check if correct
            tier_correct = (actual_tier == expected_tier)
            match_correct = (len(results.get('matched_rules', [])) > 0) == expected_match
            
            is_correct = tier_correct and match_correct
            tier_stats[expected_tier]["total"] += 1
            if is_correct:
                tier_stats[expected_tier]["correct"] += 1
            
            print(f"Case {i}: Facts={case['facts'][:3]}...")
            print(f"  Expected Tier: {expected_tier}, Actual: {actual_tier}")
            print(f"  Result: {'✓' if is_correct else '✗'}")
        
        print(f"\n{'=' * 80}")
        print("RULE ENGINE ACCURACY BY TIER:")
        for tier, stats in tier_stats.items():
            if stats["total"] > 0:
                accuracy = stats["correct"] / stats["total"]
                tier_name = {1: "Manual", 2: "Auto", 3: "Fallback"}[tier]
                print(f"  Tier {tier} ({tier_name}): {accuracy:.1%} ({stats['correct']}/{stats['total']})")
        print(f"{'=' * 80}\n")
        
        return tier_stats
    
    def evaluate_case_matching_accuracy(self, test_cases: List[Dict]) -> Dict:
        """
        Evaluate case matching Mean Average Precision
        
        Test format:
        {
            "query": "theft workplace laptop",
            "relevant_cases": ["HKCA_123_2020", "HKCA_456_2019"]
        }
        """
        print("=" * 80)
        print("EVALUATING CASE MATCHING")
        print("=" * 80)
        
        average_precisions = []
        
        for i, case in enumerate(test_cases, 1):
            results = self.case_matcher.find_similar_cases(case["query"], top_n=5)
            relevant_case_names = set(case["relevant_cases"])
            
            # Calculate average precision
            relevant_found = 0
            precisions = []
            
            for rank, (matched_case, score) in enumerate(results, 1):
                if matched_case.case_name in relevant_case_names:
                    relevant_found += 1
                    precision_at_rank = relevant_found / rank
                    precisions.append(precision_at_rank)
            
            avg_precision = sum(precisions) / len(relevant_case_names) if relevant_case_names else 0
            average_precisions.append(avg_precision)
            
            print(f"Case {i}: '{case['query']}'")
            print(f"  Relevant found: {relevant_found}/{len(relevant_case_names)}")
            print(f"  Average Precision: {avg_precision:.1%}")
        
        MAP = sum(average_precisions) / len(average_precisions) if average_precisions else 0
        
        print(f"\n{'=' * 80}")
        print(f"CASE MATCHING MAP: {MAP:.1%}")
        print(f"{'=' * 80}\n")
        
        return {
            "MAP": MAP,
            "cases_tested": len(test_cases)
        }
    
    def generate_report(self, results: Dict) -> str:
        """Generate formatted evaluation report"""
        
        report = []
        report.append("=" * 80)
        report.append("SYSTEM ACCURACY EVALUATION REPORT")
        report.append("=" * 80)
        report.append("")
        
        # NLP Results
        if "nlp" in results:
            nlp = results["nlp"]
            report.append(f"① NLP Fact Extraction: {nlp['accuracy']:.1%}")
            report.append(f"   Correct: {nlp['correct']}/{nlp['total']} facts")
            report.append("")
        
        # Search Results
        if "search" in results:
            search = results["search"]
            report.append(f"② Hybrid Search Precision@5: {search['precision_at_5']:.1%}")
            report.append(f"   Test cases: {search['cases_tested']}")
            report.append("")
        
        # Rule Engine Results
        if "rules" in results:
            report.append("⑤ Enhanced Rule Engine:")
            for tier, stats in results["rules"].items():
                if stats["total"] > 0:
                    accuracy = stats["correct"] / stats["total"]
                    tier_name = {1: "Manual (Tier 1)", 2: "Auto (Tier 2)", 3: "Fallback (Tier 3)"}[tier]
                    report.append(f"   {tier_name}: {accuracy:.1%} ({stats['correct']}/{stats['total']})")
            report.append("")
        
        # Case Matching Results
        if "cases" in results:
            cases = results["cases"]
            report.append(f"⑥ Case Matching MAP: {cases['MAP']:.1%}")
            report.append(f"   Test cases: {cases['cases_tested']}")
            report.append("")
        
        report.append("=" * 80)
        report.append("")
        
        # Performance Table
        report.append("PERFORMANCE SUMMARY TABLE (For PPT)")
        report.append("=" * 80)
        report.append("")
        report.append("| Component         | Measured Accuracy | Test Cases |")
        report.append("|-------------------|-------------------|------------|")
        
        if "nlp" in results:
            report.append(f"| NLP Processing    | {results['nlp']['accuracy']:.1%}            | {results['nlp']['total']}         |")
        
        if "search" in results:
            report.append(f"| Hybrid Search     | {results['search']['precision_at_5']:.1%}            | {results['search']['cases_tested']}          |")
        
        if "rules" in results:
            for tier, stats in results["rules"].items():
                if stats["total"] > 0:
                    accuracy = stats["correct"] / stats["total"]
                    tier_name = {1: "Rule Tier 1", 2: "Rule Tier 2", 3: "Rule Tier 3"}[tier]
                    report.append(f"| {tier_name:17} | {accuracy:.1%}            | {stats['total']:10} |")
        
        if "cases" in results:
            report.append(f"| Case Matching     | {results['cases']['MAP']:.1%}            | {results['cases']['cases_tested']}          |")
        
        report.append("")
        report.append("=" * 80)
        
        return "\n".join(report)


def load_test_data():
    """Load test data from JSON file"""
    
    test_file = Path(__file__).parent.parent / "tests" / "accuracy_test_cases.json"
    
    if not test_file.exists():
        print(f"⚠️  Test file not found: {test_file}")
        print("   Creating minimal test set...")
        return {
            "nlp": [],
            "search": [],
            "rules": [],
            "cases": []
        }
    
    with open(test_file, 'r') as f:
        data = json.load(f)
    
    return {
        "nlp": data.get("nlp_tests", []),
        "search": data.get("search_tests", []),
        "rules": data.get("rule_engine_tests", []),
        "cases": data.get("case_matching_tests", [])
    }


def main():
    """Run full system evaluation"""
    
    print("\n" + "=" * 80)
    print("HONG KONG LEGAL EXPERT SYSTEM - ACCURACY EVALUATION")
    print("=" * 80)
    print()
    
    # Initialize evaluator
    evaluator = SystemEvaluator()
    
    # Load test data
    print("Loading test data...")
    test_data = load_test_data()
    print(f"✅ Loaded test cases:")
    print(f"   - NLP: {len(test_data['nlp'])} cases")
    print(f"   - Search: {len(test_data['search'])} cases")
    print(f"   - Rules: {len(test_data['rules'])} cases")
    print(f"   - Case Matching: {len(test_data['cases'])} cases")
    print()
    
    # Run evaluations
    results = {}
    
    print("Starting evaluations...\n")
    
    # Evaluate NLP
    if test_data['nlp']:
        results['nlp'] = evaluator.evaluate_nlp_accuracy(test_data['nlp'])
    
    # Evaluate Search
    if test_data['search']:
        results['search'] = evaluator.evaluate_search_accuracy(test_data['search'])
    
    # Evaluate Rule Engine
    if test_data['rules']:
        results['rules'] = evaluator.evaluate_rule_engine_accuracy(test_data['rules'])
    
    # Evaluate Case Matching
    if test_data['cases']:
        results['cases'] = evaluator.evaluate_case_matching_accuracy(test_data['cases'])
    
    # Generate and print report
    report = evaluator.generate_report(results)
    print(report)
    
    # Save results
    output_file = Path(__file__).parent.parent / "evaluation_results.txt"
    with open(output_file, 'w') as f:
        f.write(report)
    
    print(f"✅ Results saved to: {output_file}")
    print()


if __name__ == '__main__':
    main()
