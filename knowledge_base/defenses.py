"""
Criminal Law Defenses
Common defenses available under Hong Kong criminal law
"""

class Defense:
    """Represents a criminal law defense"""
    def __init__(self, defense_id, name, conditions, effect, burden_of_proof, 
                 legal_basis, explanation=""):
        self.defense_id = defense_id
        self.name = name
        self.conditions = conditions  # Requirements for defense to apply
        self.effect = effect  # Complete defense or partial defense
        self.burden_of_proof = burden_of_proof  # Who must prove it
        self.legal_basis = legal_basis  # Common law or statutory
        self.explanation = explanation
    
    def __repr__(self):
        return f"Defense({self.defense_id}: {self.name})"
    
    def applies(self, facts):
        """Check if defense conditions are met"""
        for condition in self.conditions:
            if condition not in facts:
                return False
        return True
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            "defense_id": self.defense_id,
            "name": self.name,
            "conditions": self.conditions,
            "effect": self.effect,
            "burden_of_proof": self.burden_of_proof,
            "legal_basis": self.legal_basis,
            "explanation": self.explanation
        }


# GENERAL DEFENSES
GENERAL_DEFENSES = [
    Defense(
        defense_id="DEF_001",
        name="Self-Defense",
        conditions=[
            "defendant_faced_unlawful_force",
            "force_used_was_reasonable",
            "force_used_was_necessary"
        ],
        effect="Complete defense",
        burden_of_proof="Evidential burden on defendant, prosecution must disprove",
        legal_basis="Common law",
        explanation="A person may use reasonable force to defend themselves, others, or property from unlawful attack."
    ),
    Defense(
        defense_id="DEF_002",
        name="Duress by Threats",
        conditions=[
            "threat_of_death_or_serious_injury",
            "threat_was_immediate",
            "no_reasonable_opportunity_to_escape",
            "reasonable_person_would_have_acted_similarly"
        ],
        effect="Complete defense (except murder)",
        burden_of_proof="Evidential burden on defendant, prosecution must disprove",
        legal_basis="Common law",
        explanation="A person forced to commit a crime under immediate threat of death or serious harm may have a defense (not available for murder)."
    ),
    Defense(
        defense_id="DEF_003",
        name="Duress of Circumstances",
        conditions=[
            "faced_imminent_peril",
            "no_reasonable_alternative",
            "response_was_proportionate"
        ],
        effect="Complete defense (except murder)",
        burden_of_proof="Evidential burden on defendant, prosecution must disprove",
        legal_basis="Common law",
        explanation="Acting under pressure of circumstances to avoid imminent peril."
    ),
    Defense(
        defense_id="DEF_004",
        name="Necessity",
        conditions=[
            "acted_to_prevent_greater_harm",
            "no_reasonable_alternative",
            "harm_caused_less_than_harm_prevented"
        ],
        effect="Complete defense (limited application)",
        burden_of_proof="Defendant must establish",
        legal_basis="Common law",
        explanation="Acting to prevent a greater harm where there was no reasonable alternative."
    ),
    Defense(
        defense_id="DEF_005",
        name="Mistake of Fact",
        conditions=[
            "genuinely_believed_facts",
            "belief_was_reasonable",
            "if_facts_were_true_no_offence"
        ],
        effect="Complete defense",
        burden_of_proof="Evidential burden on defendant",
        legal_basis="Common law",
        explanation="An honest and reasonable mistake about facts that, if true, would make the act lawful."
    ),
    Defense(
        defense_id="DEF_006",
        name="Intoxication (Involuntary)",
        conditions=[
            "defendant_was_intoxicated",
            "intoxication_was_involuntary",
            "offence_requires_specific_intent"
        ],
        effect="Defense to specific intent crimes only",
        burden_of_proof="Evidential burden on defendant",
        legal_basis="Common law",
        explanation="Involuntary intoxication may negate specific intent required for certain offences."
    ),
    Defense(
        defense_id="DEF_007",
        name="Intoxication (Voluntary)",
        conditions=[
            "defendant_voluntarily_intoxicated",
            "so_intoxicated_could_not_form_specific_intent",
            "offence_requires_specific_intent"
        ],
        effect="Defense to specific intent crimes only (limited)",
        burden_of_proof="Evidential burden on defendant",
        legal_basis="Common law",
        explanation="Voluntary intoxication may prevent formation of specific intent (very limited defense)."
    ),
]

# MENTAL STATE DEFENSES
MENTAL_STATE_DEFENSES = [
    Defense(
        defense_id="DEF_008",
        name="Insanity",
        conditions=[
            "defendant_had_mental_disease_or_defect",
            "did_not_know_nature_of_act",
            "or_did_not_know_act_was_wrong"
        ],
        effect="Not guilty by reason of insanity",
        burden_of_proof="Defendant must prove on balance of probabilities",
        legal_basis="Common law (M'Naghten Rules)",
        explanation="Mental disease or defect that prevented defendant from knowing nature or wrongness of act."
    ),
    Defense(
        defense_id="DEF_009",
        name="Diminished Responsibility",
        conditions=[
            "abnormality_of_mental_functioning",
            "arising_from_recognized_medical_condition",
            "substantially_impaired_ability",
            "offence_is_murder"
        ],
        effect="Reduces murder to manslaughter",
        burden_of_proof="Defendant must prove on balance of probabilities",
        legal_basis="Statutory (Cap. 200, s. 3)",
        explanation="Abnormality of mind that substantially impairs responsibility - reduces murder to manslaughter."
    ),
    Defense(
        defense_id="DEF_010",
        name="Automatism",
        conditions=[
            "total_loss_of_voluntary_control",
            "not_due_to_mental_disease",
            "not_self_induced"
        ],
        effect="Complete defense",
        burden_of_proof="Evidential burden on defendant",
        legal_basis="Common law",
        explanation="Complete loss of voluntary control not due to mental disease (e.g., blow to head, hypoglycemia)."
    ),
]

# SPECIFIC DEFENSES FOR CERTAIN OFFENCES
SPECIFIC_DEFENSES = [
    Defense(
        defense_id="DEF_011",
        name="Provocation",
        conditions=[
            "defendant_was_provoked",
            "lost_self_control",
            "reasonable_person_might_have_acted_similarly",
            "offence_is_murder"
        ],
        effect="Reduces murder to manslaughter",
        burden_of_proof="Evidential burden on defendant, prosecution must disprove",
        legal_basis="Common law",
        explanation="Provocation causing loss of self-control reduces murder to manslaughter."
    ),
    Defense(
        defense_id="DEF_012",
        name="Consent (Assault)",
        conditions=[
            "victim_consented",
            "offence_is_common_assault_or_battery",
            "not_involving_serious_harm"
        ],
        effect="Complete defense to minor assault",
        burden_of_proof="Prosecution must prove lack of consent",
        legal_basis="Common law",
        explanation="Valid consent is a defense to common assault or battery (not available for serious harm)."
    ),
    Defense(
        defense_id="DEF_013",
        name="Lawful Excuse (Property Damage)",
        conditions=[
            "believed_had_consent_of_owner",
            "or_acted_to_protect_property",
            "belief_was_honest"
        ],
        effect="Complete defense to criminal damage",
        burden_of_proof="Evidential burden on defendant",
        legal_basis="Statutory (Cap. 200, s. 60)",
        explanation="Honest belief in consent or acting to protect property is lawful excuse for damage."
    ),
    Defense(
        defense_id="DEF_014",
        name="Claim of Right (Theft)",
        conditions=[
            "believed_had_legal_right_to_property",
            "belief_was_honest"
        ],
        effect="Negates dishonesty element of theft",
        burden_of_proof="Evidential burden on defendant",
        legal_basis="Statutory (Cap. 210, s. 6)",
        explanation="Honest belief in legal right to property negates dishonesty required for theft."
    ),
    Defense(
        defense_id="DEF_015",
        name="Reasonable Chastisement",
        conditions=[
            "defendant_is_parent_or_guardian",
            "force_used_was_reasonable",
            "for_purpose_of_correction"
        ],
        effect="Defense to assault on child",
        burden_of_proof="Evidential burden on defendant",
        legal_basis="Common law",
        explanation="Parents may use reasonable force to discipline children (increasingly restricted)."
    ),
]

# AGE AND CAPACITY DEFENSES
CAPACITY_DEFENSES = [
    Defense(
        defense_id="DEF_016",
        name="Infancy (Under 10)",
        conditions=[
            "defendant_under_10_years"
        ],
        effect="Complete defense - incapable of crime",
        burden_of_proof="Prosecution must prove age",
        legal_basis="Statutory",
        explanation="Children under 10 years cannot be held criminally responsible."
    ),
    Defense(
        defense_id="DEF_017",
        name="Infancy (10-14 years)",
        conditions=[
            "defendant_between_10_and_14_years",
            "prosecution_cannot_prove_knew_act_was_seriously_wrong"
        ],
        effect="Rebuttable presumption of no criminal capacity",
        burden_of_proof="Prosecution must prove defendant knew act was seriously wrong",
        legal_basis="Common law (doli incapax)",
        explanation="Children 10-14 presumed incapable unless prosecution proves they knew act was seriously wrong."
    ),
]

# POLICE POWERS AND ARREST DEFENSES
POLICE_DEFENSES = [
    Defense(
        defense_id="DEF_018",
        name="Lawful Arrest",
        conditions=[
            "defendant_is_police_officer",
            "arrest_was_lawful",
            "force_used_was_reasonable"
        ],
        effect="Defense to assault",
        burden_of_proof="Defendant must establish lawfulness",
        legal_basis="Statutory",
        explanation="Police officers may use reasonable force to effect lawful arrest."
    ),
    Defense(
        defense_id="DEF_019",
        name="Prevention of Crime",
        conditions=[
            "acted_to_prevent_crime",
            "force_used_was_reasonable",
            "in_circumstances_as_believed"
        ],
        effect="Complete defense",
        burden_of_proof="Evidential burden on defendant",
        legal_basis="Common law",
        explanation="Reasonable force may be used to prevent crime or effect lawful arrest."
    ),
]

# Consolidate all defenses
ALL_DEFENSES = (
    GENERAL_DEFENSES + 
    MENTAL_STATE_DEFENSES + 
    SPECIFIC_DEFENSES + 
    CAPACITY_DEFENSES + 
    POLICE_DEFENSES
)

# Create defense lookup dictionary
DEFENSE_DICT = {defense.defense_id: defense for defense in ALL_DEFENSES}

def get_defense_by_id(defense_id):
    """Get a defense by its ID"""
    return DEFENSE_DICT.get(defense_id)

def get_defenses_by_category(category):
    """Get all defenses in a category"""
    category_map = {
        "general": GENERAL_DEFENSES,
        "mental": MENTAL_STATE_DEFENSES,
        "specific": SPECIFIC_DEFENSES,
        "capacity": CAPACITY_DEFENSES,
        "police": POLICE_DEFENSES,
    }
    return category_map.get(category.lower(), [])

def get_applicable_defenses(facts, offence_type=None):
    """Get all defenses that might apply given the facts"""
    applicable = []
    for defense in ALL_DEFENSES:
        # Check if defense applies to this offence type
        if offence_type:
            if defense.name == "Provocation" and offence_type != "murder":
                continue
            if defense.name == "Diminished Responsibility" and offence_type != "murder":
                continue
        
        # Check if conditions are met
        if defense.applies(facts):
            applicable.append(defense)
    
    return applicable

def evaluate_defense(defense, facts):
    """Evaluate how well a defense matches the facts"""
    matched_conditions = sum(1 for cond in defense.conditions if cond in facts)
    total_conditions = len(defense.conditions)
    confidence = matched_conditions / total_conditions if total_conditions > 0 else 0
    
    return {
        "defense": defense,
        "matched_conditions": matched_conditions,
        "total_conditions": total_conditions,
        "confidence": confidence,
        "is_applicable": confidence == 1.0
    }

