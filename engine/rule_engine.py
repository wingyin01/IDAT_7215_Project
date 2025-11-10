"""
Rule-Based Inference Engine
Implements forward chaining for legal reasoning across ALL legal areas
"""

try:
    from knowledge_base.all_legal_rules import ALL_LEGAL_RULES as ALL_RULES, Rule
    from knowledge_base.defenses import ALL_DEFENSES, Defense
except ImportError:
    # Fallback to criminal rules only
    from knowledge_base.criminal_rules import ALL_RULES, Rule
    from knowledge_base.defenses import ALL_DEFENSES, Defense

class InferenceEngine:
    """
    Forward chaining inference engine for legal reasoning
    """
    
    def __init__(self):
        self.rules = ALL_RULES
        self.defenses = ALL_DEFENSES
        self.reset()
    
    def reset(self):
        """Reset the inference engine state"""
        self.facts = set()
        self.conclusions = []
        self.fired_rules = []
        self.applicable_defenses = []
        self.reasoning_chain = []
    
    def add_fact(self, fact):
        """Add a fact to the working memory"""
        if isinstance(fact, list):
            self.facts.update(fact)
        else:
            self.facts.add(fact)
    
    def add_facts(self, facts):
        """Add multiple facts"""
        self.facts.update(facts)
    
    def get_facts(self):
        """Get all current facts"""
        return self.facts
    
    def forward_chain(self, max_iterations=100):
        """
        Perform forward chaining inference
        Keep applying rules until no new conclusions can be drawn
        """
        iteration = 0
        new_facts_added = True
        
        while new_facts_added and iteration < max_iterations:
            new_facts_added = False
            iteration += 1
            
            for rule in self.rules:
                # Skip rules already fired
                if rule.rule_id in [r.rule_id for r in self.fired_rules]:
                    continue
                
                # Check if all conditions are met
                if rule.matches(self.facts):
                    # Fire the rule
                    self.fired_rules.append(rule)
                    
                    # Add conclusion to facts
                    if rule.conclusion not in self.facts:
                        self.facts.add(rule.conclusion)
                        new_facts_added = True
                    
                    # Record the conclusion
                    self.conclusions.append({
                        'conclusion': rule.conclusion,
                        'rule': rule,
                        'iteration': iteration
                    })
                    
                    # Record reasoning step
                    self.reasoning_chain.append({
                        'step': len(self.reasoning_chain) + 1,
                        'type': 'rule_application',
                        'rule_id': rule.rule_id,
                        'rule_name': rule.name,
                        'conditions_met': rule.conditions,
                        'conclusion': rule.conclusion,
                        'ordinance_ref': rule.ordinance_ref,
                        'explanation': rule.explanation
                    })
        
        # Check for applicable defenses after forward chaining
        self._check_defenses()
        
        return self.conclusions
    
    def _check_defenses(self):
        """Check which defenses might apply based on current facts"""
        for defense in self.defenses:
            if defense.applies(self.facts):
                self.applicable_defenses.append(defense)
                self.reasoning_chain.append({
                    'step': len(self.reasoning_chain) + 1,
                    'type': 'defense_check',
                    'defense_id': defense.defense_id,
                    'defense_name': defense.name,
                    'conditions_met': defense.conditions,
                    'effect': defense.effect,
                    'explanation': defense.explanation
                })
    
    def query(self, conclusion):
        """Check if a conclusion has been reached"""
        return conclusion in self.facts
    
    def get_conclusions(self):
        """Get all conclusions reached"""
        return self.conclusions
    
    def get_offences(self):
        """Get all criminal offences concluded"""
        offences = []
        for conclusion_data in self.conclusions:
            conclusion = conclusion_data['conclusion']
            if 'guilty_of_' in conclusion:
                offences.append({
                    'offence': conclusion.replace('guilty_of_', '').replace('_', ' ').title(),
                    'rule': conclusion_data['rule'],
                    'ordinance_ref': conclusion_data['rule'].ordinance_ref,
                    'penalty': conclusion_data['rule'].penalty
                })
        return offences
    
    def get_defenses(self):
        """Get all applicable defenses"""
        return self.applicable_defenses
    
    def get_reasoning_chain(self):
        """Get the complete reasoning chain"""
        return self.reasoning_chain
    
    def explain(self):
        """Generate human-readable explanation of reasoning"""
        explanation = []
        
        explanation.append("=== LEGAL ANALYSIS ===\n")
        
        # Show input facts
        explanation.append("INPUT FACTS:")
        for fact in sorted(self.facts):
            if not fact.startswith('guilty_of_'):
                explanation.append(f"  - {fact.replace('_', ' ')}")
        explanation.append("")
        
        # Show reasoning process
        explanation.append("REASONING PROCESS:")
        for step_data in self.reasoning_chain:
            if step_data['type'] == 'rule_application':
                explanation.append(f"\nStep {step_data['step']}: {step_data['rule_name']}")
                explanation.append(f"  Reference: {step_data['ordinance_ref']}")
                explanation.append(f"  Conditions satisfied:")
                for cond in step_data['conditions_met']:
                    explanation.append(f"    ✓ {cond.replace('_', ' ')}")
                explanation.append(f"  Conclusion: {step_data['conclusion'].replace('_', ' ')}")
                explanation.append(f"  Explanation: {step_data['explanation']}")
            
            elif step_data['type'] == 'defense_check':
                explanation.append(f"\nStep {step_data['step']}: Potential Defense - {step_data['defense_name']}")
                explanation.append(f"  Conditions satisfied:")
                for cond in step_data['conditions_met']:
                    explanation.append(f"    ✓ {cond.replace('_', ' ')}")
                explanation.append(f"  Effect: {step_data['effect']}")
                explanation.append(f"  Explanation: {step_data['explanation']}")
        
        explanation.append("\n=== CONCLUSIONS ===\n")
        
        # Show offences
        offences = self.get_offences()
        if offences:
            explanation.append("OFFENCES ESTABLISHED:")
            for idx, offence in enumerate(offences, 1):
                explanation.append(f"\n{idx}. {offence['offence']}")
                explanation.append(f"   Legal basis: {offence['ordinance_ref']}")
                explanation.append(f"   Maximum penalty: {offence['penalty']}")
        else:
            explanation.append("No criminal offences established based on the facts provided.")
        
        # Show defenses
        if self.applicable_defenses:
            explanation.append("\nPOTENTIAL DEFENSES:")
            for idx, defense in enumerate(self.applicable_defenses, 1):
                explanation.append(f"\n{idx}. {defense.name}")
                explanation.append(f"   Effect: {defense.effect}")
                explanation.append(f"   Burden of proof: {defense.burden_of_proof}")
                explanation.append(f"   Explanation: {defense.explanation}")
        else:
            explanation.append("\nNo defenses appear to be applicable.")
        
        return "\n".join(explanation)
    
    def get_summary(self):
        """Get a brief summary of the analysis"""
        offences = self.get_offences()
        defenses = self.get_defenses()
        
        summary = {
            'total_facts': len([f for f in self.facts if not f.startswith('guilty_of_')]),
            'rules_fired': len(self.fired_rules),
            'offences_found': len(offences),
            'offences': [o['offence'] for o in offences],
            'defenses_found': len(defenses),
            'defenses': [d.name for d in defenses],
            'reasoning_steps': len(self.reasoning_chain)
        }
        
        return summary


def analyze_case(facts):
    """
    Convenience function to analyze a case
    
    Args:
        facts: List of fact strings (e.g., ['appropriates_property', 'property_belongs_to_another'])
    
    Returns:
        InferenceEngine: Engine with analysis results
    """
    engine = InferenceEngine()
    engine.add_facts(facts)
    engine.forward_chain()
    return engine


if __name__ == '__main__':
    # Test case: Simple theft
    print("=== TEST CASE 1: Theft ===\n")
    
    facts1 = [
        'appropriates_property',
        'property_belongs_to_another',
        'acts_dishonestly',
        'intent_to_permanently_deprive'
    ]
    
    engine1 = analyze_case(facts1)
    print(engine1.explain())
    print("\n" + "="*50 + "\n")
    
    # Test case 2: Robbery
    print("=== TEST CASE 2: Robbery ===\n")
    
    facts2 = [
        'appropriates_property',
        'property_belongs_to_another',
        'acts_dishonestly',
        'intent_to_permanently_deprive',
        'uses_force_or_threat',
        'force_immediately_before_or_during_theft'
    ]
    
    engine2 = analyze_case(facts2)
    print(engine2.explain())
    print("\n" + "="*50 + "\n")
    
    # Test case 3: GBH with self-defense
    print("=== TEST CASE 3: GBH with Potential Self-Defense ===\n")
    
    facts3 = [
        'unlawfully_wounds_or_causes_gbh',
        'acts_maliciously',
        'intent_to_cause_gbh',
        'defendant_faced_unlawful_force',
        'force_used_was_reasonable',
        'force_used_was_necessary'
    ]
    
    engine3 = analyze_case(facts3)
    print(engine3.explain())

