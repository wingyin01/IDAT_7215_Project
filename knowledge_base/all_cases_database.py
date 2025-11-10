"""
Comprehensive Case Database - ALL Legal Areas
Includes criminal, civil, employment, property, commercial, family law cases
"""

class CriminalCase:
    """Represents a legal case (can be criminal, civil, employment, etc.)"""
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
        return f"Case({self.case_id}: {self.case_name} ({self.year}))"

# CRIMINAL LAW CASES (from original database)
CRIMINAL_CASES = [
    CriminalCase(
        case_id="THEFT_001",
        case_name="HKSAR v. Chan Tai Man",
        year=2019,
        court="District Court",
        facts="""The defendant entered a convenience store at 2 AM. He took several cartons of 
        cigarettes worth HK$8,000 and left without paying. CCTV footage clearly showed him concealing 
        the items in his bag.""",
        charges=["Theft contrary to s.2 of the Theft Ordinance, Cap. 210"],
        ordinance_refs=["Cap. 210, s.2"],
        outcome="Guilty",
        sentence="6 months imprisonment",
        legal_principles=["All elements of theft proven: appropriation, property belonging to another, dishonestly, with intent to permanently deprive"],
        keywords=["theft", "shop theft", "dishonesty"]
    ),
    CriminalCase(
        case_id="ROBBERY_001",
        case_name="HKSAR v. Wong Siu Ming",
        year=2020,
        court="Court of First Instance",
        facts="""The defendant approached a pedestrian on Nathan Road at night. He brandished a knife 
        and demanded the victim hand over his wallet and mobile phone.""",
        charges=["Robbery contrary to s.10 of the Crimes Ordinance, Cap. 200"],
        ordinance_refs=["Cap. 200, s.10"],
        outcome="Guilty",
        sentence="5 years imprisonment",
        legal_principles=["Robbery established: theft combined with use of force or threat of force"],
        keywords=["robbery", "knife", "threat of force", "weapon"]
    ),
]

# EMPLOYMENT LAW CASES
EMPLOYMENT_CASES = [
    CriminalCase(
        case_id="EMP_CASE_001",
        case_name="Wong v. ABC Company Limited",
        year=2021,
        court="Labour Tribunal",
        facts="""The plaintiff was employed as a sales manager for 5 years. On 15 March 2021, 
        the employer dismissed her immediately without notice, citing 'restructuring'. No prior warnings 
        were given. No severance payment was offered. Plaintiff claimed unfair dismissal and sought 
        severance payment equivalent to 2.5 months' wages.""",
        charges=["Breach of Employment Ordinance - Severance Payment"],
        ordinance_refs=["Cap. 57, s.31C"],
        outcome="Plaintiff successful",
        sentence="Employer ordered to pay HK$85,000 severance payment",
        legal_principles=[
            "Continuous employment of 24+ months entitles employee to severance payment",
            "Restructuring is a valid business reason but severance still required",
            "Summary dismissal without cause requires notice or payment in lieu"
        ],
        keywords=["employment", "unfair dismissal", "severance payment", "continuous employment"]
    ),
    
    CriminalCase(
        case_id="EMP_CASE_002",
        case_name="HKSAR v. XYZ Restaurant Limited",
        year=2020,
        court="Magistrates' Court",
        facts="""The employer failed to pay wages to 8 employees for 3 consecutive months. Total 
        outstanding wages were HK$240,000. Employees reported to Labour Department. Employer claimed 
        business difficulties but had not filed for bankruptcy. Prosecution brought under Employment 
        Ordinance.""",
        charges=["Failure to pay wages contrary to Cap. 57, s.23"],
        ordinance_refs=["Cap. 57, s.23"],
        outcome="Guilty",
        sentence="Fine of HK$200,000 and ordered to pay outstanding wages",
        legal_principles=[
            "Wages must be paid within 7 days of end of wage period",
            "Financial difficulties do not excuse non-payment of wages",
            "Wilful failure to pay wages is criminal offence",
            "Court may order payment in addition to fine"
        ],
        keywords=["employment", "wages", "non-payment", "prosecution"]
    ),
]

# PROPERTY & LANDLORD-TENANT CASES
PROPERTY_CASES = [
    CriminalCase(
        case_id="PROP_CASE_001",
        case_name="Li v. Chan",
        year=2020,
        court="District Court",
        facts="""Landlord Li and tenant Chan had 2-year tenancy agreement for a residential flat 
        in Tsim Sha Tsui. After 18 months, landlord wanted to sell the property and offered to pay 
        tenant HK$50,000 to terminate early. Tenant refused. Landlord changed locks while tenant was 
        at work, preventing access. Tenant sued for unlawful eviction.""",
        charges=["Unlawful eviction"],
        ordinance_refs=["Cap. 7, Landlord and Tenant (Consolidation) Ordinance"],
        outcome="Plaintiff (tenant) successful",
        sentence="Damages of HK$120,000 awarded to tenant, mandatory injunction for re-entry",
        legal_principles=[
            "Self-help eviction without court order is unlawful",
            "Landlord must obtain court order to evict tenant",
            "Tenant entitled to damages for unlawful eviction",
            "Valid tenancy agreement cannot be unilaterally terminated"
        ],
        keywords=["property", "landlord", "tenant", "unlawful eviction", "damages"]
    ),
]

# CIVIL LAW CASES
CIVIL_CASES = [
    CriminalCase(
        case_id="CIVIL_CASE_001",
        case_name="Yip v. Golden Electronics Limited",
        year=2019,
        court="Small Claims Tribunal",
        facts="""Plaintiff purchased a laptop for HK$12,000 with 1-year warranty. After 3 months, 
        laptop stopped working. Plaintiff returned for repair. Defendant refused, claiming damage 
        was caused by plaintiff. Independent expert confirmed manufacturing defect. Plaintiff sought 
        refund under Sale of Goods Ordinance.""",
        charges=["Breach of implied condition - merchantable quality"],
        ordinance_refs=["Cap. 26, s.16 Sale of Goods Ordinance"],
        outcome="Plaintiff successful",
        sentence="Full refund of HK$12,000 ordered",
        legal_principles=[
            "Implied condition that goods must be of merchantable quality",
            "Manufacturing defect breaches implied condition",
            "Buyer entitled to reject goods and claim refund",
            "Burden on seller to prove damage caused by buyer"
        ],
        keywords=["civil", "contract", "sale of goods", "merchantable quality", "consumer rights"]
    ),
    
    CriminalCase(
        case_id="CIVIL_CASE_002",
        case_name="Ng v. MTR Corporation Limited",
        year=2021,
        court="District Court",
        facts="""Plaintiff slipped and fell on wet floor at MTR station. Floor was wet from mopping 
        but no warning sign displayed. Plaintiff suffered fractured wrist requiring surgery. Medical 
        expenses HK$80,000. Lost wages HK$120,000. Sued for negligence.""",
        charges=["Negligence"],
        ordinance_refs=["Common law tort of negligence"],
        outcome="Plaintiff successful (contributory negligence 20%)",
        sentence="Damages of HK$160,000 awarded (80% of HK$200,000)",
        legal_principles=[
            "MTR owes duty of care to passengers",
            "Failure to warn of wet floor is breach of duty",
            "Plaintiff's injuries were foreseeable consequence",
            "Contributory negligence reduces damages where plaintiff partly at fault"
        ],
        keywords=["negligence", "duty of care", "personal injury", "damages", "contributory negligence"]
    ),
]

# COMMERCIAL LAW CASES
COMMERCIAL_CASES = [
    CriminalCase(
        case_id="COMM_CASE_001",
        case_name="HKSAR v. Cheung (Director)",
        year=2020,
        court="District Court",
        facts="""The defendant was director of a property development company. He caused the company 
        to enter into contracts with a construction firm owned by his brother, paying 30% above market 
        rates. He did not disclose his relationship to the board. Company suffered loss of HK$5 million. 
        Shareholders brought derivative action.""",
        charges=["Breach of director's duties - conflict of interest"],
        ordinance_refs=["Cap. 622, s.536 Companies Ordinance"],
        outcome="Found liable",
        sentence="Personal liability for HK$5 million, disqualified from being director for 5 years",
        legal_principles=[
            "Directors must avoid conflicts of interest",
            "Failure to disclose material interest is breach of duty",
            "Directors liable for losses caused by breach",
            "Court may disqualify directors for breaches"
        ],
        keywords=["commercial", "director's duties", "conflict of interest", "companies", "breach of duty"]
    ),
]

# FAMILY LAW CASES
FAMILY_CASES = [
    CriminalCase(
        case_id="FAM_CASE_001",
        case_name="Lam v. Lam",
        year=2021,
        court="Family Court",
        facts="""Married for 8 years. Husband had affair. Wife petitioned for divorce on grounds of 
        adultery. Couple had two children aged 5 and 7. Disputed custody and division of matrimonial 
        home worth HK$8 million. Husband's income HK$80,000/month, wife HK$40,000/month.""",
        charges=["Divorce petition - adultery"],
        ordinance_refs=["Cap. 179, s.11 Matrimonial Causes Ordinance"],
        outcome="Decree absolute granted",
        sentence="Joint custody of children, matrimonial home sold with 60:40 division favoring wife, maintenance HK$15,000/month",
        legal_principles=[
            "Adultery is ground for divorce petition",
            "Best interests of children paramount in custody decisions",
            "Matrimonial assets divided according to contributions",
            "Maintenance based on needs and earning capacity"
        ],
        keywords=["family", "divorce", "custody", "matrimonial property", "maintenance"]
    ),
]

# Consolidate ALL cases
ALL_LEGAL_CASES = (
    CRIMINAL_CASES +
    EMPLOYMENT_CASES +
    PROPERTY_CASES +
    CIVIL_CASES +
    COMMERCIAL_CASES +
    FAMILY_CASES
)

# Create case lookup
CASE_DICT = {case.case_id: case for case in ALL_LEGAL_CASES}

# Organize by category
CASES_BY_CATEGORY = {
    'Criminal Law': CRIMINAL_CASES,
    'Employment Law': EMPLOYMENT_CASES,
    'Property & Land': PROPERTY_CASES,
    'Civil Law': CIVIL_CASES,
    'Commercial & Company': COMMERCIAL_CASES,
    'Family Law': FAMILY_CASES,
}

def get_case_by_id(case_id):
    """Get a case by its ID"""
    return CASE_DICT.get(case_id)

def get_cases_by_category(category):
    """Get all cases in a category"""
    return CASES_BY_CATEGORY.get(category, [])

def search_cases_by_keyword(keyword):
    """Search cases by keyword"""
    results = []
    keyword_lower = keyword.lower()
    
    for case in ALL_LEGAL_CASES:
        if (keyword_lower in case.facts.lower() or
            keyword_lower in ' '.join(case.legal_principles).lower() or
            keyword_lower in ' '.join(case.keywords).lower()):
            results.append(case)
    
    return results

# Statistics
TOTAL_CASES = len(ALL_LEGAL_CASES)
CASES_BY_AREA = {cat: len(cases) for cat, cases in CASES_BY_CATEGORY.items()}

print(f"Loaded {TOTAL_CASES} legal cases across {len(CASES_BY_CATEGORY)} categories")

if __name__ == '__main__':
    print("\n" + "=" * 80)
    print("ALL LEGAL CASES DATABASE")
    print("=" * 80)
    print(f"Total Cases: {TOTAL_CASES}")
    print("\nBy Category:")
    for category, count in sorted(CASES_BY_AREA.items(), key=lambda x: x[1], reverse=True):
        print(f"  {category}: {count} cases")
    print("=" * 80)

