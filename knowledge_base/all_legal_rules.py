"""
Comprehensive Legal Rules for ALL Hong Kong Law Areas
Includes rules for criminal, civil, employment, property, commercial law, etc.

Framework with samples - expand as needed for full coverage
"""

from knowledge_base.criminal_rules import Rule, ALL_RULES as CRIMINAL_RULES

# EMPLOYMENT LAW RULES (Cap. 57 - Employment Ordinance)
EMPLOYMENT_RULES = [
    Rule(
        rule_id="EMP_001",
        name="Unfair Dismissal - Continuous Employment",
        conditions=[
            "employment_contract_exists",
            "continuous_employment_24_months_or_more",
            "dismissed_without_notice",
            "no_serious_misconduct"
        ],
        conclusion="entitled_to_severance_payment",
        ordinance_ref="Cap. 57, s. 31C",
        penalty="Severance payment required",
        explanation="Employee with 24+ months continuous employment dismissed without notice and no serious misconduct is entitled to severance payment."
    ),
    Rule(
        rule_id="EMP_002",
        name="Termination Without Notice - Summary Dismissal",
        conditions=[
            "employment_contract_exists",
            "employee_serious_misconduct",
            "dismissed_without_notice"
        ],
        conclusion="lawful_summary_dismissal",
        ordinance_ref="Cap. 57, s. 9",
        penalty="No notice or payment in lieu required",
        explanation="Employer may summarily dismiss employee for serious misconduct without notice or payment."
    ),
    Rule(
        rule_id="EMP_003",
        name="Wages - Timely Payment",
        conditions=[
            "employment_contract_exists",
            "wages_not_paid_within_7_days",
            "no_valid_reason_for_delay"
        ],
        conclusion="breach_of_wages_provision",
        ordinance_ref="Cap. 57, s. 23",
        penalty="Prosecution and fine up to HK$350,000",
        explanation="Employer must pay wages within 7 days of wage period end. Failure to do so is an offence."
    ),
    Rule(
        rule_id="EMP_004",
        name="Statutory Holiday Entitlement",
        conditions=[
            "employment_contract_exists",
            "employed_for_3_months_or_more",
            "employer_refuses_statutory_holiday"
        ],
        conclusion="breach_of_holiday_entitlement",
        ordinance_ref="Cap. 57, s. 39",
        penalty="Prosecution and fine",
        explanation="Employees employed for 3+ months entitled to statutory holidays. Denial is breach of ordinance."
    ),
    Rule(
        rule_id="EMP_005",
        name="Maternity Leave",
        conditions=[
            "employee_is_pregnant",
            "continuous_employment_40_weeks_or_more",
            "gives_pregnancy_notice",
            "employer_denies_maternity_leave"
        ],
        conclusion="breach_of_maternity_protection",
        ordinance_ref="Cap. 57, s. 12",
        penalty="Fine up to HK$100,000",
        explanation="Pregnant employees with 40+ weeks employment entitled to 14 weeks maternity leave."
    ),
]

# PROPERTY & LANDLORD-TENANT RULES (Cap. 7 - Landlord and Tenant Ordinance)
PROPERTY_RULES = [
    Rule(
        rule_id="PROP_001",
        name="Unlawful Eviction",
        conditions=[
            "tenancy_agreement_exists",
            "landlord_evicts_without_court_order",
            "no_lawful_grounds"
        ],
        conclusion="unlawful_eviction",
        ordinance_ref="Cap. 7, various sections",
        penalty="Civil liability for damages",
        explanation="Landlord cannot evict tenant without court order. Self-help eviction is unlawful."
    ),
    Rule(
        rule_id="PROP_002",
        name="Rent Increase - Excessive",
        conditions=[
            "tenancy_agreement_exists",
            "landlord_increases_rent",
            "increase_exceeds_agreement_terms"
        ],
        conclusion="breach_of_tenancy_agreement",
        ordinance_ref="Contract law principles + Cap. 7",
        penalty="Tenant may refuse, seek remedies",
        explanation="Rent increases must comply with tenancy agreement terms. Excessive increases may be challenged."
    ),
    Rule(
        rule_id="PROP_003",
        name="Security Deposit - Non-return",
        conditions=[
            "tenancy_ended",
            "no_damage_to_property",
            "landlord_refuses_return_deposit",
            "no_valid_reason"
        ],
        conclusion="unlawful_retention_of_deposit",
        ordinance_ref="Common law + Cap. 7",
        penalty="Civil claim for recovery",
        explanation="Landlord must return security deposit if no breach or damage. Unlawful retention gives rise to claim."
    ),
]

# CIVIL LAW RULES (Cap. 26 - Sale of Goods Ordinance)
CIVIL_RULES = [
    Rule(
        rule_id="CIVIL_001",
        name="Sale of Goods - Implied Condition of Quality",
        conditions=[
            "contract_for_sale_of_goods",
            "goods_not_of_merchantable_quality",
            "buyer_examines_goods"
        ],
        conclusion="breach_of_implied_condition",
        ordinance_ref="Cap. 26, s. 16",
        penalty="Buyer may reject goods, claim damages",
        explanation="Implied condition that goods sold by description must be of merchantable quality."
    ),
    Rule(
        rule_id="CIVIL_002",
        name="Negligence - Duty of Care",
        conditions=[
            "defendant_owes_duty_of_care",
            "defendant_breaches_duty",
            "breach_causes_damage",
            "damage_foreseeable"
        ],
        conclusion="liable_in_negligence",
        ordinance_ref="Common law tort",
        penalty="Damages for loss suffered",
        explanation="Defendant liable for negligence if duty breached causing foreseeable damage."
    ),
]

# COMMERCIAL LAW RULES (Cap. 622 - Companies Ordinance)
COMMERCIAL_RULES = [
    Rule(
        rule_id="COMM_001",
        name="Director's Duty - Conflict of Interest",
        conditions=[
            "person_is_company_director",
            "director_has_personal_interest",
            "interest_conflicts_with_company",
            "fails_to_disclose"
        ],
        conclusion="breach_of_directors_duty",
        ordinance_ref="Cap. 622, s. 536",
        penalty="Civil liability, possible disqualification",
        explanation="Directors must avoid conflicts of interest and disclose any personal interests in company transactions."
    ),
    Rule(
        rule_id="COMM_002",
        name="Fraudulent Trading",
        conditions=[
            "carries_on_business",
            "intent_to_defraud_creditors",
            "knowingly_party_to_fraudulent_trading"
        ],
        conclusion="guilty_of_fraudulent_trading",
        ordinance_ref="Cap. 622, s. 350",
        penalty="Imprisonment up to 7 years and fine",
        explanation="Carrying on business with intent to defraud creditors is criminal offence."
    ),
]

# FAMILY LAW RULES (Cap. 179 - Matrimonial Causes Ordinance)
FAMILY_RULES = [
    Rule(
        rule_id="FAM_001",
        name="Divorce - Irretrievable Breakdown",
        conditions=[
            "married_for_1_year_or_more",
            "marriage_irretrievably_broken_down",
            "proves_ground_for_divorce"
        ],
        conclusion="entitled_to_divorce",
        ordinance_ref="Cap. 179, s. 11",
        penalty="N/A - Civil remedy",
        explanation="Marriage of 1+ years may be dissolved if irretrievably broken down and ground proven."
    ),
]

# TAX LAW RULES (Cap. 112 - Inland Revenue Ordinance)
TAX_RULES = [
    Rule(
        rule_id="TAX_001",
        name="Tax Evasion",
        conditions=[
            "liable_to_pay_tax",
            "willfully_evades_tax",
            "with_intent_to_defraud"
        ],
        conclusion="guilty_of_tax_evasion",
        ordinance_ref="Cap. 112, s. 82",
        penalty="Fine and imprisonment up to 3 years",
        explanation="Willfully evading tax with intent to defraud is criminal offence."
    ),
]

# Consolidate ALL legal rules
ALL_LEGAL_RULES = (
    CRIMINAL_RULES +      # 100+ criminal law rules
    EMPLOYMENT_RULES +    # 5 employment law rules (sample)
    PROPERTY_RULES +      # 3 property law rules (sample)
    CIVIL_RULES +         # 2 civil law rules (sample)
    COMMERCIAL_RULES +    # 2 commercial law rules (sample)
    FAMILY_RULES +        # 1 family law rule (sample)
    TAX_RULES            # 1 tax law rule (sample)
)

# Create rule lookup
RULE_DICT = {rule.rule_id: rule for rule in ALL_LEGAL_RULES}

# Organize by category
RULES_BY_CATEGORY = {
    'Criminal Law': CRIMINAL_RULES,
    'Employment Law': EMPLOYMENT_RULES,
    'Property & Land': PROPERTY_RULES,
    'Civil Law': CIVIL_RULES,
    'Commercial & Company': COMMERCIAL_RULES,
    'Family Law': FAMILY_RULES,
    'Tax & Revenue': TAX_RULES,
}

def get_rule_by_id(rule_id):
    """Get a rule by its ID"""
    return RULE_DICT.get(rule_id)

def get_rules_by_category(category):
    """Get all rules in a category"""
    return RULES_BY_CATEGORY.get(category, [])

def get_applicable_rules(facts):
    """Get all rules whose conditions are satisfied by the given facts"""
    return [rule for rule in ALL_LEGAL_RULES if rule.matches(facts)]

# Statistics
TOTAL_RULES = len(ALL_LEGAL_RULES)
RULES_BY_AREA = {cat: len(rules) for cat, rules in RULES_BY_CATEGORY.items()}

print(f"Loaded {TOTAL_RULES} legal rules across {len(RULES_BY_CATEGORY)} categories")

if __name__ == '__main__':
    print("\n" + "=" * 80)
    print("LEGAL RULES SUMMARY")
    print("=" * 80)
    print(f"Total Rules: {TOTAL_RULES}")
    print("\nBy Category:")
    for category, count in sorted(RULES_BY_AREA.items(), key=lambda x: x[1], reverse=True):
        print(f"  {category}: {count} rules")
    print("=" * 80)

