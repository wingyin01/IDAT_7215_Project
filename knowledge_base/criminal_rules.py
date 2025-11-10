"""
Criminal Law Rules for Expert System
If-Then rules derived from Hong Kong Criminal Ordinances
Each rule has: conditions (antecedents), conclusion, ordinance reference, and confidence
"""

class Rule:
    """Represents a legal rule with conditions and conclusion"""
    def __init__(self, rule_id, name, conditions, conclusion, ordinance_ref, 
                 penalty, confidence=1.0, explanation=""):
        self.rule_id = rule_id
        self.name = name
        self.conditions = conditions  # List of required facts
        self.conclusion = conclusion  # Legal outcome
        self.ordinance_ref = ordinance_ref  # Reference to ordinance section
        self.penalty = penalty
        self.confidence = confidence
        self.explanation = explanation
    
    def __repr__(self):
        return f"Rule({self.rule_id}: {self.name})"
    
    def matches(self, facts):
        """Check if all conditions are satisfied by the given facts"""
        for condition in self.conditions:
            if condition not in facts:
                return False
        return True
    
    def to_dict(self):
        """Convert rule to dictionary for JSON serialization"""
        return {
            "rule_id": self.rule_id,
            "name": self.name,
            "conditions": self.conditions,
            "conclusion": self.conclusion,
            "ordinance_ref": self.ordinance_ref,
            "penalty": self.penalty,
            "confidence": self.confidence,
            "explanation": self.explanation
        }


# THEFT RULES
THEFT_RULES = [
    Rule(
        rule_id="THEFT_001",
        name="Basic Theft",
        conditions=[
            "appropriates_property",
            "property_belongs_to_another",
            "acts_dishonestly",
            "intent_to_permanently_deprive"
        ],
        conclusion="guilty_of_theft",
        ordinance_ref="Cap. 210, s. 2",
        penalty="10 years imprisonment",
        explanation="All elements of theft are satisfied: dishonest appropriation of another's property with intent to permanently deprive."
    ),
    Rule(
        rule_id="THEFT_002",
        name="Robbery",
        conditions=[
            "guilty_of_theft",
            "uses_force_or_threat",
            "force_immediately_before_or_during_theft"
        ],
        conclusion="guilty_of_robbery",
        ordinance_ref="Cap. 200, s. 10",
        penalty="14 years imprisonment",
        explanation="Theft combined with use of force or threat of force constitutes robbery."
    ),
    Rule(
        rule_id="THEFT_003",
        name="Burglary",
        conditions=[
            "enters_building",
            "as_trespasser",
            "intent_to_steal_or_assault_or_damage"
        ],
        conclusion="guilty_of_burglary",
        ordinance_ref="Cap. 200, s. 11",
        penalty="14 years imprisonment",
        explanation="Entry into building as trespasser with criminal intent constitutes burglary."
    ),
    Rule(
        rule_id="THEFT_004",
        name="Aggravated Burglary",
        conditions=[
            "guilty_of_burglary",
            "has_weapon_or_explosive"
        ],
        conclusion="guilty_of_aggravated_burglary",
        ordinance_ref="Cap. 200, s. 12",
        penalty="Life imprisonment",
        explanation="Burglary while carrying a weapon, firearm, or explosive is aggravated burglary."
    ),
    Rule(
        rule_id="THEFT_005",
        name="Handling Stolen Goods",
        conditions=[
            "receives_or_handles_goods",
            "knows_or_believes_goods_stolen",
            "acts_dishonestly"
        ],
        conclusion="guilty_of_handling_stolen_goods",
        ordinance_ref="Cap. 210, s. 18",
        penalty="14 years imprisonment",
        explanation="Dishonestly receiving or handling goods knowing or believing them to be stolen."
    ),
    Rule(
        rule_id="THEFT_006",
        name="Taking Conveyance Without Authority",
        conditions=[
            "takes_vehicle",
            "without_owner_consent",
            "for_own_or_another_use"
        ],
        conclusion="guilty_of_taking_conveyance",
        ordinance_ref="Cap. 210, s. 23",
        penalty="3 years imprisonment or fine",
        explanation="Taking a vehicle without consent of the owner."
    ),
]

# ASSAULT AND VIOLENCE RULES
ASSAULT_RULES = [
    Rule(
        rule_id="ASSAULT_001",
        name="Common Assault",
        conditions=[
            "assaults_or_beats",
            "another_person",
            "unlawfully"
        ],
        conclusion="guilty_of_common_assault",
        ordinance_ref="Cap. 200, s. 40",
        penalty="1 year imprisonment",
        explanation="Unlawful assault or battery of another person."
    ),
    Rule(
        rule_id="ASSAULT_002",
        name="Assault Occasioning Actual Bodily Harm",
        conditions=[
            "assaults_another_person",
            "causes_actual_bodily_harm"
        ],
        conclusion="guilty_of_assault_occasioning_abh",
        ordinance_ref="Cap. 200, s. 39",
        penalty="3 years imprisonment",
        explanation="Assault that results in actual bodily harm to the victim."
    ),
    Rule(
        rule_id="ASSAULT_003",
        name="Grievous Bodily Harm with Intent",
        conditions=[
            "unlawfully_wounds_or_causes_gbh",
            "acts_maliciously",
            "intent_to_cause_gbh"
        ],
        conclusion="guilty_of_gbh_with_intent",
        ordinance_ref="Cap. 200, s. 36",
        penalty="Life imprisonment",
        explanation="Unlawfully and maliciously causing grievous bodily harm with specific intent."
    ),
    Rule(
        rule_id="ASSAULT_004",
        name="Murder",
        conditions=[
            "unlawfully_kills",
            "another_person",
            "with_malice_aforethought"
        ],
        conclusion="guilty_of_murder",
        ordinance_ref="Cap. 200, s. 17",
        penalty="Life imprisonment",
        explanation="Unlawful killing of another person with malice aforethought."
    ),
    Rule(
        rule_id="ASSAULT_005",
        name="Manslaughter",
        conditions=[
            "unlawfully_kills",
            "another_person",
            "no_malice_aforethought"
        ],
        conclusion="guilty_of_manslaughter",
        ordinance_ref="Cap. 200, s. 18",
        penalty="Life imprisonment",
        explanation="Unlawful killing without malice aforethought."
    ),
    Rule(
        rule_id="ASSAULT_006",
        name="Kidnapping",
        conditions=[
            "takes_and_carries_away",
            "another_person",
            "by_force_or_fraud",
            "without_consent"
        ],
        conclusion="guilty_of_kidnapping",
        ordinance_ref="Cap. 200, s. 42",
        penalty="14 years imprisonment",
        explanation="Taking and carrying away a person by force or fraud without consent."
    ),
    Rule(
        rule_id="ASSAULT_007",
        name="Assault with Intent to Resist Arrest",
        conditions=[
            "assaults_another_person",
            "intent_to_resist_arrest"
        ],
        conclusion="guilty_of_assault_resisting_arrest",
        ordinance_ref="Cap. 201, s. 39",
        penalty="2 years imprisonment",
        explanation="Assaulting another person to resist or prevent lawful arrest."
    ),
]

# FRAUD AND DECEPTION RULES
FRAUD_RULES = [
    Rule(
        rule_id="FRAUD_001",
        name="Basic Fraud",
        conditions=[
            "makes_false_representation",
            "acts_dishonestly",
            "intent_to_gain_or_cause_loss"
        ],
        conclusion="guilty_of_fraud",
        ordinance_ref="Cap. 200, s. 16A",
        penalty="14 years imprisonment",
        explanation="Dishonestly making false representation with intent to gain or cause loss."
    ),
    Rule(
        rule_id="FRAUD_002",
        name="Obtaining Property by Deception",
        conditions=[
            "obtains_property",
            "by_deception",
            "acts_dishonestly",
            "intent_to_permanently_deprive"
        ],
        conclusion="guilty_of_obtaining_by_deception",
        ordinance_ref="Cap. 200, s. 161",
        penalty="10 years imprisonment",
        explanation="Dishonestly obtaining property through deception with intent to permanently deprive."
    ),
    Rule(
        rule_id="FRAUD_003",
        name="False Accounting",
        conditions=[
            "falsifies_accounting_document",
            "acts_dishonestly",
            "view_to_gain_or_cause_loss"
        ],
        conclusion="guilty_of_false_accounting",
        ordinance_ref="Cap. 210, s. 17",
        penalty="10 years imprisonment",
        explanation="Dishonestly falsifying accounting documents with view to gain or cause loss."
    ),
    Rule(
        rule_id="FRAUD_004",
        name="Blackmail",
        conditions=[
            "makes_unwarranted_demand",
            "with_menaces",
            "view_to_gain_or_cause_loss"
        ],
        conclusion="guilty_of_blackmail",
        ordinance_ref="Cap. 200, s. 16",
        penalty="14 years imprisonment",
        explanation="Making unwarranted demand with menaces for gain or to cause loss."
    ),
]

# DRUG OFFENCES RULES
DRUG_RULES = [
    Rule(
        rule_id="DRUG_001",
        name="Drug Possession",
        conditions=[
            "possesses_substance",
            "substance_is_dangerous_drug"
        ],
        conclusion="guilty_of_drug_possession",
        ordinance_ref="Cap. 221, s. 38",
        penalty="7 years imprisonment and $1,000,000 fine",
        explanation="Possession of a dangerous drug."
    ),
    Rule(
        rule_id="DRUG_002",
        name="Drug Trafficking",
        conditions=[
            "manufactures_or_sells_or_distributes",
            "dangerous_drug"
        ],
        conclusion="guilty_of_drug_trafficking",
        ordinance_ref="Cap. 221, s. 8",
        penalty="Life imprisonment and $5,000,000 fine",
        explanation="Manufacturing, selling, or distributing dangerous drugs constitutes trafficking."
    ),
    Rule(
        rule_id="DRUG_003",
        name="Drug Import/Export",
        conditions=[
            "imports_or_exports",
            "dangerous_drug"
        ],
        conclusion="guilty_of_drug_import_export",
        ordinance_ref="Cap. 221, s. 4",
        penalty="Life imprisonment and $5,000,000 fine",
        explanation="Importing or exporting dangerous drugs."
    ),
    Rule(
        rule_id="DRUG_004",
        name="Consuming Dangerous Drugs",
        conditions=[
            "smokes_or_consumes",
            "dangerous_drug"
        ],
        conclusion="guilty_of_consuming_drugs",
        ordinance_ref="Cap. 221, s. 40",
        penalty="7 years imprisonment and $1,000,000 fine",
        explanation="Smoking or consuming dangerous drugs."
    ),
]

# SEXUAL OFFENCES RULES
SEXUAL_OFFENCE_RULES = [
    Rule(
        rule_id="SEXUAL_001",
        name="Rape",
        conditions=[
            "has_sexual_intercourse",
            "victim_does_not_consent",
            "knows_or_reckless_about_non_consent",
            "perpetrator_is_male"
        ],
        conclusion="guilty_of_rape",
        ordinance_ref="Cap. 200, s. 118",
        penalty="Life imprisonment",
        explanation="Sexual intercourse without consent where the perpetrator knows or is reckless about non-consent."
    ),
    Rule(
        rule_id="SEXUAL_002",
        name="Indecent Assault",
        conditions=[
            "assaults_another_person",
            "assault_is_indecent",
            "no_consent_to_indecency"
        ],
        conclusion="guilty_of_indecent_assault",
        ordinance_ref="Cap. 200, s. 122",
        penalty="10 years imprisonment",
        explanation="Assault of an indecent nature without consent."
    ),
    Rule(
        rule_id="SEXUAL_003",
        name="Unlawful Sexual Intercourse with Girl Under 13",
        conditions=[
            "has_sexual_intercourse",
            "victim_under_13_years",
            "perpetrator_is_male"
        ],
        conclusion="guilty_of_intercourse_under_13",
        ordinance_ref="Cap. 200, s. 123",
        penalty="Life imprisonment",
        explanation="Sexual intercourse with girl under 13 - consent is irrelevant."
    ),
    Rule(
        rule_id="SEXUAL_004",
        name="Unlawful Sexual Intercourse with Girl Under 16",
        conditions=[
            "has_sexual_intercourse",
            "victim_under_16_years",
            "victim_at_least_13_years",
            "perpetrator_is_male"
        ],
        conclusion="guilty_of_intercourse_under_16",
        ordinance_ref="Cap. 200, s. 124",
        penalty="5 years imprisonment",
        explanation="Sexual intercourse with girl between 13 and 16 years."
    ),
    Rule(
        rule_id="SEXUAL_005",
        name="Administering Drugs to Obtain Intercourse",
        conditions=[
            "administers_drugs_to_victim",
            "victim_is_female",
            "intent_to_enable_intercourse"
        ],
        conclusion="guilty_of_administering_drugs_for_intercourse",
        ordinance_ref="Cap. 200, s. 47",
        penalty="14 years imprisonment",
        explanation="Administering drugs to woman or girl to enable sexual intercourse."
    ),
]

# PROPERTY DAMAGE RULES
PROPERTY_DAMAGE_RULES = [
    Rule(
        rule_id="PROPERTY_001",
        name="Criminal Damage",
        conditions=[
            "destroys_or_damages_property",
            "property_belongs_to_another",
            "no_lawful_excuse",
            "intentionally_or_recklessly"
        ],
        conclusion="guilty_of_criminal_damage",
        ordinance_ref="Cap. 200, s. 60",
        penalty="10 years imprisonment",
        explanation="Intentionally or recklessly destroying or damaging another's property without lawful excuse."
    ),
    Rule(
        rule_id="PROPERTY_002",
        name="Arson",
        conditions=[
            "sets_fire",
            "to_building_or_structure",
            "unlawfully",
            "maliciously"
        ],
        conclusion="guilty_of_arson",
        ordinance_ref="Cap. 200, s. 59",
        penalty="Life imprisonment",
        explanation="Unlawfully and maliciously setting fire to a building or structure."
    ),
    Rule(
        rule_id="PROPERTY_003",
        name="Threats to Damage Property",
        conditions=[
            "makes_threat",
            "to_destroy_or_damage_property",
            "intends_victim_would_fear",
            "no_lawful_excuse"
        ],
        conclusion="guilty_of_threats_to_damage_property",
        ordinance_ref="Cap. 200, s. 61",
        penalty="10 years imprisonment",
        explanation="Making threats to destroy or damage property intending the victim would fear the threat."
    ),
]

# COMPUTER CRIME RULES
COMPUTER_CRIME_RULES = [
    Rule(
        rule_id="COMPUTER_001",
        name="Unauthorized Computer Access",
        conditions=[
            "obtains_access_to_computer",
            "with_criminal_or_dishonest_intent"
        ],
        conclusion="guilty_of_unauthorized_computer_access",
        ordinance_ref="Cap. 200, s. 161",
        penalty="5 years imprisonment",
        explanation="Obtaining access to computer with criminal or dishonest intent."
    ),
]

# PUBLIC ORDER RULES
PUBLIC_ORDER_RULES = [
    Rule(
        rule_id="PUBLIC_001",
        name="Unlawful Assembly",
        conditions=[
            "three_or_more_persons_assembled",
            "disorderly_or_intimidating_conduct",
            "likely_to_cause_breach_of_peace"
        ],
        conclusion="guilty_of_unlawful_assembly",
        ordinance_ref="Cap. 245, s. 17A",
        penalty="5 years imprisonment",
        explanation="Three or more persons assembled with disorderly conduct likely to breach the peace."
    ),
    Rule(
        rule_id="PUBLIC_002",
        name="Riot",
        conditions=[
            "guilty_of_unlawful_assembly",
            "actual_breach_of_peace"
        ],
        conclusion="guilty_of_riot",
        ordinance_ref="Cap. 245, s. 18",
        penalty="10 years imprisonment",
        explanation="Unlawful assembly that makes an actual breach of the peace."
    ),
]

# CHILD PROTECTION RULES
CHILD_PROTECTION_RULES = [
    Rule(
        rule_id="CHILD_001",
        name="Abandoning Child Under 2",
        conditions=[
            "abandons_or_exposes_child",
            "child_under_2_years",
            "endangers_life_or_health"
        ],
        conclusion="guilty_of_abandoning_child",
        ordinance_ref="Cap. 201, s. 36",
        penalty="5 years imprisonment",
        explanation="Unlawfully abandoning or exposing a child under 2 years endangering their life or health."
    ),
]

# Consolidate all rules
ALL_RULES = (
    THEFT_RULES + 
    ASSAULT_RULES + 
    FRAUD_RULES + 
    DRUG_RULES + 
    SEXUAL_OFFENCE_RULES + 
    PROPERTY_DAMAGE_RULES + 
    COMPUTER_CRIME_RULES + 
    PUBLIC_ORDER_RULES + 
    CHILD_PROTECTION_RULES
)

# Create rule lookup dictionary
RULE_DICT = {rule.rule_id: rule for rule in ALL_RULES}

def get_rule_by_id(rule_id):
    """Get a rule by its ID"""
    return RULE_DICT.get(rule_id)

def get_rules_by_category(category):
    """Get all rules in a category"""
    category_map = {
        "theft": THEFT_RULES,
        "assault": ASSAULT_RULES,
        "fraud": FRAUD_RULES,
        "drugs": DRUG_RULES,
        "sexual": SEXUAL_OFFENCE_RULES,
        "property": PROPERTY_DAMAGE_RULES,
        "computer": COMPUTER_CRIME_RULES,
        "public_order": PUBLIC_ORDER_RULES,
        "child": CHILD_PROTECTION_RULES,
    }
    return category_map.get(category.lower(), [])

def get_applicable_rules(facts):
    """Get all rules whose conditions are satisfied by the given facts"""
    return [rule for rule in ALL_RULES if rule.matches(facts)]

