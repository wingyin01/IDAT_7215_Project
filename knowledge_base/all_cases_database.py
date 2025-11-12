"""
Real Hong Kong Criminal Appeal Cases Database
Cases from Court of Appeal of the High Court (Criminal Appeals)
Source: Official HK Judiciary Database (legalref.judiciary.hk)
Manually downloaded and processed for educational purposes

⚠️ Copyright Notice:
These cases are from official Hong Kong Judiciary sources.
Data is used for educational/research purposes under fair use.
For official case law research, visit: https://legalref.judiciary.hk/
"""

class CriminalCase:
    """Represents a criminal appeal case"""
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
        return f"Case({self.case_id}: {self.case_name[:30] if self.case_name else self.case_id} ({self.year}))"

# REAL CRIMINAL APPEAL CASES
ALL_CRIMINAL_CASES = [
    CriminalCase(
        case_id="CACC000001A",
        case_name="",
        year=2018,
        court="Court of Appeal",
        facts="""The prosecution case It was alleged that, on the morning of 3 February 2016, a team of Customs officers carried out a surveillance operation at the departure area of Hong Kong International Airport and observed, at 7:45 am, D2 pulling a silver-coloured suitcase (“the suitcase”) and meeting up with D3.  At 7:50 am, D1 appeared and joined both D2 and D3; D2 then passed the suitcase to D1 and the three of them proceeded to the airline’s self-check in counter.  D1 alone pulled the suitcase aside and, having briefly checked its contents, gave it to D2 to look after.  From time to time, D1 talked on his mobile telephone and subsequently hurried to the drop-off area to meet D4, who did not arrive until 8:10 am.  The two of them then proceeded to join D2 and D3, whereupon D2 passed the suitcase to""",
        charges="""On 24 June 2020, D1 filed an application to renew his application for leave to appeal (Form XIII). At the conclusion of the hearing of the renewal application, we refused D1 leave to renew his application and dismissed his appeal.  We also made a 6 weeks loss of time order against D1.  We said we would hand down the reasons for our decisions in due course.  These are our reasons. The delay and dis""",
        ordinance_refs="",
        outcome="""CRIMINAL APPEAL NO 1 OF 2018 (ON APPEAL FROM HCCC NO 305 OF 2016) _______________ HKSAR	Respondent v LEE ERNEST	Applicant _______________ Before:  Hon Macrae VP, Zervos and M Poon JJA in Court Date of""",
        sentence="",
        legal_principles=[
            "Criminal appeal principles apply"
        ],
        keywords=["robbery", "drug", "fraud", "murder", "possession", "trafficking"]
    ),
    CriminalCase(
        case_id="CACC000001",
        case_name="",
        year=2020,
        court="Court of Appeal",
        facts="""At the time of sentence, the applicant was 43 years of age.  He lived alone, although he had been previously married and had a son.  He occasionally worked running parallel goods.  He had six previous criminal convictions since 1992 and his last conviction was in 2012 when he was convicted for trafficking in a dangerous drug and sentenced to 7 years’ imprisonment. The judge in her reasons for sentence did not find any meaningful mitigation advanced on the applicant’s behalf.  She applied the sentencing guidelines laid down in HKSAR v Abdallah Anwar Abbas [2009] 2 HKLRD 437 and adopted a starting point of 21 years and 9 months’ imprisonment.  She enhanced the notional starting point by 2 years for the international element to 23 years and 9 months’ imprisonment, which she reduced by one thi""",
        charges="""At the time of sentence, the applicant was 43 years of age.  He lived alone, although he had been previously married and had a son.  He occasionally worked running parallel goods.  He had six previous criminal convictions since 1992 and his last conviction was in 2012 when he was convicted for trafficking in a dangerous drug and sentenced to 7 years’ imprisonment. The judge in her reasons for sent""",
        ordinance_refs="",
        outcome="""CRIMINAL APPEAL NO 1 OF 2020 (ON APPEAL FROM HCCC NO 148 OF 2018) _______________ HKSAR	Respondent v WONG YU-WO (黃裕和)	Applicant _______________ Before:  Hon Zervos JA in Court Date of Hearing:  3 Marc""",
        sentence="",
        legal_principles=[
            "Criminal appeal principles apply"
        ],
        keywords=["drug", "trafficking"]
    ),
    CriminalCase(
        case_id="CACC000001",
        case_name="I am separately concerned whether the enhancement of 3 months’ imprisonment for the applicant’s stat",
        year=2024,
        court="Court of Appeal",
        facts="""""",
        charges="""""",
        ordinance_refs="",
        outcome="""in the high court of the hong kong special administrative region court of appeal criminal appeal no 1 of 2024 (on appeal from DCCC NO 131 of 2023) BETWEEN Before: Hon Macrae Acting CJHC in Chambers Da""",
        sentence="",
        legal_principles=[
            "Criminal appeal principles apply"
        ],
        keywords=[""]
    ),
    CriminalCase(
        case_id="CACC000003",
        case_name="",
        year=2022,
        court="Court of Appeal",
        facts="""""",
        charges="""On 6 January 2022, the applicant applied for leave to appeal his sentence. Ms Anna Ho, for the applicant, advances three grounds of appeal against sentence.  Ground 1 complains that the starting point adopted by the judge for Charge 2 was manifestly excessive.  Ground 2 avers that the judge erred in considering the role of the applicant in the two charges and adopting a consecutive element of 12 m""",
        ordinance_refs="",
        outcome="""CRIMINAL APPEAL NO 3 OF 2022 (ON APPEAL FROM DCCC NO 757 OF 2021) _______________ HKSAR	Respondent v Lau Ka Fai, Coffee (劉家輝)	Applicant _______________ Before:  Hon Zervos JA in Court Date of Hearing:""",
        sentence="",
        legal_principles=[
            "Criminal appeal principles apply"
        ],
        keywords=["drug", "possession", "trafficking"]
    ),
    CriminalCase(
        case_id="CACC000003",
        case_name="",
        year=2025,
        court="Court of Appeal",
        facts="""""",
        charges="""""",
        ordinance_refs="",
        outcome="""""",
        sentence="",
        legal_principles=[
            "Criminal appeal principles apply"
        ],
        keywords=[""]
    ),
    CriminalCase(
        case_id="CACC000005B",
        case_name="BETWEEN Before: Hon Macrae VP, Zervos JA and A Pang JA in Court",
        year=2018,
        court="Court of Appeal",
        facts="""“Where the plaintiff belongs to a class which either is or ought to be within the contemplation of the defendant and the defendant by reason of his involvement in an activity which gives him a measure of control over and responsibility for a situation which, if dangerous, will be liable to injure the plaintiff, the defendant is liable if as a result of his unreasonable lack of care he causes a situation to exist which does in fact cause the plaintiff injury. … Once proximity is established by reference to the test which I have identified, none of the more sophisticated criteria which have to be used in relation to allegations of liability for mere economic loss need to be applied in relation to personal injury, nor have they been in the decided cases.” Given, as we described, “the overwhel""",
        charges="""The five points of law, as set out in D1’s Notice of Motion dated 9 November 2021, are as follows: “1.	In cases of Gross Negligence Manslaughter (in which a convicted defendant could face life imprisonment) is it necessary to establish that an individual defendant assumed personal responsibility for the actions by third parties employed by a company controlled by him that were the substantial caus""",
        ordinance_refs="",
        outcome="""Appeal Dismissed""",
        sentence="",
        legal_principles=[
            "Appeal dismissed - conviction upheld"
        ],
        keywords=["murder"]
    ),
    CriminalCase(
        case_id="CACC000006",
        case_name="",
        year=2020,
        court="Court of Appeal",
        facts="""The facts outlined to the judge and admitted by the applicant when he pleaded guilty were as follows.  On 24 February 2016, the applicant, a Peruvian national, arrived in Hong Kong from Amsterdam, although his journey originated in Lima, Peru.  He was detained on arrival as it was suspected he had items concealed in his body.  He was taken to the North Lantau District Hospital where it was confirmed that he had foreign objects in his body cavity.  He was transferred to the Queen Mary Hospital and subsequently discharged 52 packets which were later confirmed to contain the dangerous drug particularized in the charge.  The estimated retail value of the cocaine at the time of the offence was $488,215. In a subsequent record of interview, the applicant admitted that a friend, by the name of Lu""",
        charges="""On 14 September 2016, the applicant appeared before Wong J (the judge), who sentenced him to 11 years and 8 months’ imprisonment. On 13 January 2020, 3 years and 4 months after he was sentenced, the applicant filed a notice of application for leave to appeal against sentence out of time.  He claims the delay in filing his application was because he was looking for grounds of appeal.  He said he re""",
        ordinance_refs="",
        outcome="""CRIMINAL APPEAL NO 6 OF 2020 (ON APPEAL FROM HCCC NO 337 OF 2016) _______________ HKSAR	Respondent v INZA MADUENO Andrew Anthony	Applicant _______________ Before:  Hon Zervos JA in Court Date of Heari""",
        sentence="11 years imprisonment",
        legal_principles=[
            "Criminal appeal principles apply"
        ],
        keywords=["drug", "trafficking"]
    ),
    CriminalCase(
        case_id="CACC000007",
        case_name="",
        year=2019,
        court="Court of Appeal",
        facts="""""",
        charges="""The applicant’s case was fixed for trial in the Court of First Instance on 5 December 2018, with 7 days set aside, and for a case management hearing on 10 September 2018.  It was not until the case management hearing that the applicant admitted the offence of possession of dangerous drugs, as an alternative to the charge of trafficking in dangerous drugs. The applicant went to trial and was acquit""",
        ordinance_refs="",
        outcome="""CRIMINAL APPEAL NO 7 OF 2019 (ON APPEAL FROM HCCC NO 176 OF 2018) _________________ HKSAR	Respondent v SHEK Po-sin (石寶善)	Applicant _________________ Before:  Hon Zervos JA in Court Date of Hearing:  9""",
        sentence="",
        legal_principles=[
            "Criminal appeal principles apply"
        ],
        keywords=["drug", "possession", "trafficking"]
    ),
    CriminalCase(
        case_id="CACC000007",
        case_name="",
        year=2020,
        court="Court of Appeal",
        facts="""Most of the facts of the case were not in dispute and adduced into evidence by agreement of the parties.  On 31 May 2018, Customs officers intercepted a parcel from Lithuania addressed to D1.  Upon inspection, they found it contained three bottles of liquid with a total volume of 2,910 millilitres containing 3.26 kilogrammes of GBL.  In the morning of the next day, Customs officers, posing as postal workers, delivered the parcel to a flat in Sham Shui Po.  D1 acknowledged that the parcel was addressed to him and accepted receipt of it.  He was arrested and upon being cautioned admitted that he had ordered the substance in the parcel online.  He said he intended to use the substance as a cleaning agent for his car.  In support of his claim, he provided the website of an online shop from whi""",
        charges="""(i) 	trafficking in a dangerous drug, namely 2,910 millimetres of a liquid containing 3.26 kilogrammes of gamma butyrolactone (commonly known as GBL), contrary to section 4(1)(a) and (3) of the Dangerous Drugs Ordinance, Cap 134, (the DDO) (Charge 1); (ii) 	possession of dangerous drugs, namely 34 millilitres of a liquid containing 36.6 grammes of GBL and 34 millilitres of a liquid, weighing 0.08 """,
        ordinance_refs="",
        outcome="""CRIMINAL APPEAL NO 7 OF 2020 (ON APPEAL FROM DCCC NO 416 OF 2019) _______________ HKSAR	Respondent v KO WAI SHING (高威誠)	Applicant _______________ Before:  Hon Zervos JA in Court Date of Hearing:  4 Se""",
        sentence="",
        legal_principles=[
            "Criminal appeal principles apply"
        ],
        keywords=["assault", "drug", "sexual", "possession", "trafficking"]
    ),
    CriminalCase(
        case_id="CACC000007",
        case_name="",
        year=2021,
        court="Court of Appeal",
        facts="""The prosecution case was given the Form 8 holder status of the applicant and the street value of the drugs at $12,900 the only inference to be drawn was that the applicant possessed the cocaine for the purposes of trafficking. Defence case The applicant did not give evidence.  His case was that he did not possess the cigarette packet or the drugs contained inside.  He denied saying that Fiaz gave him the drugs to sell to others.  It was Fiaz who was in possession of the cocaine who dropped the packet.  He believed that Fiaz was a police informant and the police had falsely implicated him in an effort to protect Fiaz. Public Interest Immunity (PII) claim An application for disclosure of whether or not Fiaz was a police informant was made.  The applicant was granted police bail after his arr""",
        charges="""Prosecution case On 4 October 2017, PW1 (PC 19566) and PW2 (PC 21352), were patrolling in uniform along Middle Road.  The applicant was seen with another male Mohammad Mohsan Fiaz (“Fiaz”) leaning against a concrete barrier on the opposite side of the road.  Both of them walked in different directions upon seeing the police officers. PW1 and PW2 approached the applicant and Fiaz.  PW1 testified th""",
        ordinance_refs="",
        outcome="""CRIMINAL APPEAL NO 7 OF 2021 (ON APPEAL FROM DCCC NO 157 OF 2019 __________________________ BETWEEN HKSAR 	Respondent and HAQUE AAMIR	Applicant __________________________ Before: Hon M Poon JA in Cour""",
        sentence="",
        legal_principles=[
            "Criminal appeal principles apply"
        ],
        keywords=["drug", "possession", "trafficking"]
    ),
    CriminalCase(
        case_id="CACC000008A",
        case_name="",
        year=2022,
        court="Court of Appeal",
        facts="""The movements of the appellant and Chan inside Rambler Hotel, including their checking in and the four occasions they went in and out of the hotel together on 3 October 2019; The arrests of the appellant and Chan and the seizure of the drugs.  At about 8:23 pm, the two men were both arrested at Rambler ‍Plaza, Tsing Yi.  At that time, Chan was carrying a bag containing the drugs particularised in Count 1 (which was concealed inside a packet of cat food (Exhibits P1-3)).  The retail value of these drugs was $246,007.  The appellant was escorted back to Room 2355.  The drugs particularised in Count 2 were then found in a wallet carried by the appellant.  The drugs particularised in Count 3 were found in Room 2355 and their retail value was about $847,467; The appellant’s left thumb fingerpri""",
        charges="""The appellant sought to appeal against his conviction only.  At the leave hearing on 15 December 2022, at which he was legally represented, the Single Judge noted that his sole ground of appeal comprised two matters.  The first matter constituted a pure question of law and did not require leave to appeal, namely whether the judge’s directions on drawing inferences unlawfully placed an onus of proo""",
        ordinance_refs="",
        outcome="""CRIMINAL APPEAL NO 8 OF 2022 (ON APPEAL FROM HCCC NO 264 OF 2020) _______________ HKSAR	Respondent v Cheung Hoi Pun (張海賓)	Appellant _______________ Before:  Hon Macrae VP, Zervos and M Poon JJA in Cou""",
        sentence="",
        legal_principles=[
            "Criminal appeal principles apply"
        ],
        keywords=["drug", "possession", "trafficking"]
    ),
    CriminalCase(
        case_id="CACC000008",
        case_name="BETWEEN Before: Hon Macrae VP in Court",
        year=2023,
        court="Court of Appeal",
        facts="""The applicant was found with the subject-matter of the count contained in six packets on his person when intercepted by police officers, whilst walking along Nam Cheong Street in Sham Shui Po, Kowloon at about 3 am on 1 January 2021.  At the time, he also had with him three mobile telephones and HK$10,606 in cash.  Following his arrest and caution, the applicant responded that he had nothing to say.  In a later video-recorded interview, the applicant declined to answer any questions put to him. The estimated street value of the ‘Ice’ at the time was HK$20,891.64.  At his plea, the applicant admitted that he was unlawfully trafficking in the said ‘Ice’ at the time. The applicant had 15 previous court appearances, 12 of which were concerned with dangerous drugs.  Although most of these 12 ‍a""",
        charges="""Mitigation It was submitted in mitigation that in 1989, the applicant had committed his first offence of keeping a vice establishment, for which he was sentenced to 9 months’ imprisonment.  His wife had subsequently left him taking their two children, after which he had lost contact with them.  This led to a spiral of depression and involvement with dangerous drugs.  However, following his last re""",
        ordinance_refs="",
        outcome="""in the high court of the hong kong special administrative region court of appeal criminal appeal no 8 of 2023 (on appeal from hccc NO 95 of 2022) BETWEEN Before: Hon Macrae VP in Court Date of Hearing""",
        sentence="",
        legal_principles=[
            "Criminal appeal principles apply"
        ],
        keywords=["drug", "possession", "trafficking"]
    ),
    CriminalCase(
        case_id="CACC000009",
        case_name="BETWEEN Before: Hon Macrae VP in Court",
        year=2020,
        court="Court of Appeal",
        facts="""""",
        charges="""After hearing from counsel, I reserved judgment on both applications and said that I would give my decision in due course.  This is my decision and the reasons therefor. The prosecution case Ms X’s evidence It was the prosecution allegation that the applicant raped Ms ‍X, who was PW1 at trial, on 22 ‍November ‍2018 at a flat in Savoy Garden, Shatin, New Territories.  Ms X sold luxury watches and l""",
        ordinance_refs="",
        outcome="""criminal appeal no 9 of 2020 (on appeal from HCCC NO 244 of 2019) BETWEEN Before: Hon Macrae VP in Court Date of Hearing: 22 October 2021 Date of Judgment: 28 October 2021 The applicant was indicted o""",
        sentence="",
        legal_principles=[
            "Criminal appeal principles apply"
        ],
        keywords=["assault", "sexual"]
    ),
    CriminalCase(
        case_id="CACC000009",
        case_name="",
        year=2025,
        court="Court of Appeal",
        facts="""Particulars Immediately before delivering the verdict, the Court informed the parties that she had studied the facts in HKSAR v. TANG Wai-sum and others, CACC 171/2021, relating to the same incident/riot. 2. 	In relation to Charge 2, whether it is correct in law to convict a person with ‘conspiracy to wounding with intent’ when the intention and/or the foresight of that intention, is only limited to cause grievous bodily harm, particularly when that foresight and/or consequence would not cause necessary cause grievous bodily harm. Particulars At paragraphs 95 and 96 where the Court below found that, ‘D had the specific intent for wounding with intent.  I find that D foresaw grievous bodily harm as an inevitable consequence of hitting with wooden pole or rattan stick’. DPP v. Smith [1961] A""",
        charges="""On 15 January 2025, the applicant filed a notice of application for leave to appeal his convictions. In the Amended Perfected Grounds of Appeal filed on 18 March 2025, Mr David Boyton, who represented the applicant at trial and on appeal, advanced the following four grounds of appeal: “1.	Whether it is permissible in law for a tribunal of fact to consider the facts of an appellate judgment (of a c""",
        ordinance_refs="",
        outcome="""IN THE HIGH COURT OF THE HONG KONG SPECIAL ADMINISTRATIVE REGION COURT OF APPEAL CRIMINAL APPEAL NO 9 OF 2025 (ON APPEAL FROM DCCC NO 6 OF 2022) _______________ BETWEEN HKSAR	Respondent and Tang Ka-ma""",
        sentence="",
        legal_principles=[
            "Criminal appeal principles apply"
        ],
        keywords=["firearm"]
    ),
    CriminalCase(
        case_id="CACC000010",
        case_name="",
        year=2020,
        court="Court of Appeal",
        facts="""In cross-examination, Dr Chan agreed that the applicant believed what he was saying “but it was not of the delusional level …because the origin of his belief was actually from some documents or person’s account that he was relying on”.  He said the applicant seemed to have fixated ideas about something, but he could not conclude that the applicant was suffering from a delusional disorder without the documents on which the applicant relied being proven to be false.  In the end, he accepted that he could not rule out that the applicant was suffering from a delusional disorder. The defence case The applicant elected not to testify but called one defence witness, Dr Gabriel Hung (“Dr Hung”), a psychiatrist who had visited the applicant once on 21 December 2018 during his remand at Stanley Pris""",
        charges="""At the hearing of the application I granted the applicant leave to appeal against both his conviction and sentence but was subsequently told that the applicant decided to abandon his appeal against sentence.  However, that ultimately did not happen and awaiting his decision on that issue caused delay in the handing down of this judgment. The prosecution case On 9 April 2018, the applicant, a Filip""",
        ordinance_refs="",
        outcome="""CRIMINAL APPEAL NO 10 OF 2020 (ON APPEAL FROM DCCC 545/2018) ------------------------------- BETWEEN HKSAR	Respondent and BOLANOS BRUDENCIO JAO	Applicant ------------------------------- Before: Hon Mc""",
        sentence="",
        legal_principles=[
            "Criminal appeal principles apply"
        ],
        keywords=[""]
    ),
    CriminalCase(
        case_id="CACC000010",
        case_name="BETWEEN Before: Hon Macrae Acting CJHC in Court Date of Hearing: 5 December 2023 Date of Judgment: 5",
        year=2022,
        court="Court of Appeal",
        facts="""It was admitted by the applicant at trial, by way of two sets of Admitted Facts, made under section 65C of the Criminal Procedure ‍Ordinance, Cap 221, that at 23:02 hours on 28 ‍December ‍2018, she and Wu were intercepted by the police at the lift lobby of the address stated in the indictment.  Upon interception, DPC 7157 found inside a grey paper bag that was being carried by the applicant a green camouflage sweater, wrapped inside of which was a transparent re-sealable plastic bag containing another black plastic bag.  Inside the black plastic bag was a block wrapped in cling film and tin foil, which was later confirmed to be the dangerous drug particularised in the indictment. The applicant and Wu were both arrested for trafficking in a dangerous drug.  Under caution, the applicant said""",
        charges="""The undisputed facts It was admitted by the applicant at trial, by way of two sets of Admitted Facts, made under section 65C of the Criminal Procedure ‍Ordinance, Cap 221, that at 23:02 hours on 28 ‍December ‍2018, she and Wu were intercepted by the police at the lift lobby of the address stated in the indictment.  Upon interception, DPC 7157 found inside a grey paper bag that was being carried by""",
        ordinance_refs="",
        outcome="""criminal appeal no 10 of 2022 (on appeal from hccc NO 176 of 2020) BETWEEN Before: Hon Macrae Acting CJHC in Court Date of Hearing: 5 December 2023 Date of Judgment: 5 December 2023 The applicant plea""",
        sentence="",
        legal_principles=[
            "Criminal appeal principles apply"
        ],
        keywords=["drug", "possession", "trafficking"]
    ),
    CriminalCase(
        case_id="CACC000011A",
        case_name="",
        year=2021,
        court="Court of Appeal",
        facts="""""",
        charges="""""",
        ordinance_refs="",
        outcome="""""",
        sentence="",
        legal_principles=[
            "Criminal appeal principles apply"
        ],
        keywords=[""]
    ),
    CriminalCase(
        case_id="CACC000012A",
        case_name="BETWEEN Before: Hon Macrae VP, Zervos and M Poon JJA in Court",
        year=2022,
        court="Court of Appeal",
        facts="""The trial judge failed to direct the jury on “drawing inferences” and “speculation” sufficiently, or at all.  Since the jury were not legally trained, they should have been given a more elaborate explanation of these matters; The trial judge failed to explain to the jury how to approach the “hearsay evidence” in the case, for example, the testimony of A and Tiger, since they were not present at the scene of the alleged rape and, therefore, what they claimed to know could only have come from X and B; There was no eyewitness to the alleged offence; and The applicant’s conviction for attempted rape was inconsistent with the pathologist’s finding of the existence of penetration, which was also made the subject of an admitted fact. The respondent’s submission in reply Ms Betty Fu, together with""",
        charges="""On 13 October 2022, the applicant filed a notice seeking to renew his application for leave to appeal against conviction (Form XIII) and, on 21 December 2023, appeared in person at the hearing of his renewed application.  Having heard arguments from the applicant and the respondent, we refused the application, saying that we would hand down the reasons for our decision in due course.  This we now """,
        ordinance_refs="",
        outcome="""criminal appeal no 12 of 2022 (on appeal from hccc NO 50 of 2021) BETWEEN Before: Hon Macrae VP, Zervos and M Poon JJA in Court Date of Hearing: 21 December 2023 Date of Judgment: 21 December 2023 Dat""",
        sentence="",
        legal_principles=[
            "Criminal appeal principles apply"
        ],
        keywords=["assault", "sexual"]
    ),
    CriminalCase(
        case_id="CACC000014",
        case_name="",
        year=2018,
        court="Court of Appeal",
        facts="""The Summary of Facts, which was admitted by the applicant and used for his sentencing, revealed that on 24 April 2015, the applicant was observed by police officers handing a white plastic shopping bag to D2 outside a shop on Cheung Sha Wan Road, Sham Shui Po.  The officers then approached, stopped and searched both men.  They found a total of 549 grammes of cocaine, wrapped in 74 plastic pellets in the shopping bag that D2 was by then holding. The street value of the cocaine was HK$1,500,114 at the time of its seizure. Under caution, both the applicant and D2 denied any involvement in the offence but in the Summary of Facts the applicant admitted having committed the offence. The procedural history of the applicant’s case During a pre-trial review on 7 June 2016 before Zervos J, as Zervos""",
        charges="""The applicant subsequently filed a Notice of Application for Leave to Appeal against sentence (Form XI).  However, on 19 June 2018, he filed a Notice of Abandonment in respect of this Application for Leave to Appeal, as a consequence of which his appeal was dismissed pursuant to Rule 39 of the Criminal Appeal Rules, Cap 221A. On 7 November 2018, the applicant made and filed an affirmation seeking """,
        ordinance_refs="",
        outcome="""CRIMINAL APPEAL NO 14 OF 2018 (on appeal from HCCC NO 457 of 2015 & HCCC No 59 of 2016) ------------------------ BETWEEN HKSAR	Respondent and MADUEKWE AKACHUKWU BELLAMINE	Applicant alias TUNKARA OMAR """,
        sentence="",
        legal_principles=[
            "Criminal appeal principles apply"
        ],
        keywords=["drug", "trafficking"]
    ),
    CriminalCase(
        case_id="CACC000015",
        case_name="BETWEEN Before: Hon Macrae Acting CJHC in Court Date of Hearing: 3 September 2025 Date of Judgment: ",
        year=2025,
        court="Court of Appeal",
        facts="""The facts, which the applicant agreed, were that on 24 March 2024, at 12:06 am, he was observed wandering around Ching Yuk House, Tsz Ching Estate in Wong Tai Sin, Kowloon.  When a team of police officers on anti-crime patrol in the area approached him, he lowered his head and quickly walked away.  One of the officers (PW1), however, intercepted the applicant, revealed his police identity and asked him what he was doing.  The applicant said he was looking for his friend but could not explain where his friend was.  He was then searched and in the right pocket of his trousers were found: One plastic bag containing 3 stapled plastic bags, inside of which were 0.87 grammes of a solid containing 0.73 grammes of cocaine. One plastic bag containing 14 stapled plastic bags, inside of which were 4.""",
        charges="""Facts agreed by the applicant The facts, which the applicant agreed, were that on 24 March 2024, at 12:06 am, he was observed wandering around Ching Yuk House, Tsz Ching Estate in Wong Tai Sin, Kowloon.  When a team of police officers on anti-crime patrol in the area approached him, he lowered his head and quickly walked away.  One of the officers (PW1), however, intercepted the applicant, reveale""",
        ordinance_refs="",
        outcome="""in the high court of the hong kong special administrative region court of appeal criminal appeal no 15 of 2025 (on appeal from DCCC NO 787 of 2024) BETWEEN Before: Hon Macrae Acting CJHC in Court Date""",
        sentence="",
        legal_principles=[
            "Criminal appeal principles apply"
        ],
        keywords=["drug", "possession", "trafficking"]
    ),
    CriminalCase(
        case_id="CACC000020",
        case_name="BETWEEN Before: Hon Macrae Acting CJHC in Chambers Dates of Written Submissions: 28 June 2024 (Appli",
        year=2024,
        court="Court of Appeal",
        facts="""""",
        charges="""""",
        ordinance_refs="",
        outcome="""in the high court of the hong kong special administrative region court of appeal criminal appeal no 20 of 2024 (on appeal from HCCC NO 106 of 2022) BETWEEN Before: Hon Macrae Acting CJHC in Chambers D""",
        sentence="",
        legal_principles=[
            "Criminal appeal principles apply"
        ],
        keywords=[""]
    ),
    CriminalCase(
        case_id="CACC000028",
        case_name="BETWEEN Before: Hon Macrae VP in Court",
        year=2025,
        court="Court of Appeal",
        facts="""In the evening of 2 April 2022, during an anti-narcotics operation, the police took the opportunity to enter Room 2110, Hoi ‍Yan ‍House, Hoi Fu Court, Mong Kok (“the Flat”) when Ms ‍Hon ‍Yin-‍hiu opened the door for two visitors.  The applicant, being the Flat’s registered tenant, was lying on a bed inside the premises. Six re-sealable plastic bags containing 8.49 grammes of methamphetamine hydrochloride, commonly known as “Ice”, were found on Ms Hon after a body search. On a table in the Flat, the police found a metal box with the following contents: 4 re-sealable plastic bags containing totally 17.0 grammes of “Ice”; An electronic scale; Multiple re-sealable plastic bags contained in a larger re-‍sealable plastic bag; 2 glass bottles each attached with a straw, resembling pipes for smoki""",
        charges="""Background of the applicant In mitigation, it was said that the applicant was brought up in a modest family in the mainland.  At 21, he came to Hong Kong in pursuit of a better life.  However, marginalised and frustrated by society, he descended into a life of crime and bad habits.  At the time of sentencing, the applicant was a former drug abuser aged 68, with 20 previous convictions, for which h""",
        ordinance_refs="",
        outcome="""in the high court of the hong kong special administrative region court of appeal criminal appeal no 28 of 2025 (on appeal from HCCC NO 114 of 2024) BETWEEN Before: Hon Macrae VP in Court Date of Heari""",
        sentence="",
        legal_principles=[
            "Criminal appeal principles apply"
        ],
        keywords=["theft", "robbery", "assault", "drug", "fraud", "sexual"]
    ),
    CriminalCase(
        case_id="CACC000031",
        case_name="BETWEEN (Heard together) Before: Hon Macrae VP in Court",
        year=2024,
        court="Court of Appeal",
        facts="""In pleading guilty to all of the charges, the applicant admitted two sets of facts detailing the background and evidence relevant to each case.  The facts which constituted the individual charges arose in this way. (Charge 5 in Case 2) On 3 March 2022, a Mr Chan (“Chan”) posted a handbag for sale on Facebook for HK$36,500.  On 4 March 2022, Chan was contacted by a purported buyer and subsequently met with the applicant, who claimed to be the purported buyer’s boyfriend.  Chan then checked through his online banking application and noted that two cheques, both in the sum of HK$36,500, had been deposited into his account.  The applicant then told Chan that an extra HK$36,500 had been mistakenly deposited into his account and asked for reimbursement in cash.  However, Chan did not make any re""",
        charges="""DCCC 1079/2022 & 709/2023 (“Case 1”): two theft charges of an ATM card and an identity card; (Charges 1 and 2); one charge of using an identity card relating to another person (Charge 3); three charges of conspiracy to defraud (Charges ‍4, 5 and 7); and one charge of handling stolen goods (Charge ‍6); and DCCC 21 & 297/2023 (“Case 2”): one charge of handling stolen goods (Charge 4) and one charge """,
        ordinance_refs="",
        outcome="""(Heard together) in the high court of the hong kong special administrative region court of appeal criminal appeal nos 31 & 32 of 2024 (on appeal from dccc NOs 1079 of 2022 & 709 of 2023 (CONSOLIDATED)""",
        sentence="",
        legal_principles=[
            "Criminal appeal principles apply"
        ],
        keywords=["theft", "drug", "fraud", "trafficking"]
    ),
    CriminalCase(
        case_id="CACC000047",
        case_name="",
        year=2025,
        court="Court of Appeal",
        facts="""The respondent faced trial in the District Court before Deputy District Judge M H Tsui (the judge) for the offence of dangerous driving causing death.  The offence alleged that the respondent, a driver of a public light bus, at around 9:47 pm on 13 April 2023 while executing a right-hand turn at the traffic light junction on Lai Chi Kok Road, entered the pedestrian crossing resulting in the bus’s offside front striking the deceased, who was using the pedestrian crossing at the time.  The respondent was following the traffic control signal, which was green for vehicular traffic, while the deceased was facing a red light for the pedestrian crossing.  There was little dispute between the parties as to what took place that evening, as most of the evidence was admitted.  The respondent’s defenc""",
        charges="""Section 84 provides that the Secretary for Justice can appeal by way of case stated to the Court of Appeal against a verdict or order of acquittal on a question of law only.  It is stipulated under section 84(a) that “within 7 clear days after the reasons for a verdict have been recorded or after the order of acquittal, or within such further period as a judge of the High Court may, whether before""",
        ordinance_refs="",
        outcome="""IN THE HIGH COURT OF THE HONG KONG SPECIAL ADMINISTRATIVE REGION COURT OF APPEAL CRIMINAL APPEAL NO 47 OF 2025 (ON APPEAL FROM DCCC NO 1134 OF 2023) _______________ BETWEEN Secretary for Justice	Appli""",
        sentence="",
        legal_principles=[
            "Criminal appeal principles apply"
        ],
        keywords=[""]
    ),
    CriminalCase(
        case_id="CACC000059",
        case_name="",
        year=2025,
        court="Court of Appeal",
        facts="""Almost two years later, the applicant committed the other robbery offence.  On the afternoon of 14 April 2022, the applicant robbed a bank teller (PW2) of HK$14,000 at a bank in Yau Ma Tei.  He posed as a customer and handed PW2 a note that read in Chinese, “Robbery, we have gun, quickly put the money in the bag, failure to cooperate, we will shoot” (Count 2).  PW2 triggered a discreet alarm to notify her manager, while the applicant pointed a pistol-like object at her and gave her a bag for the money.  When PW2 began counting the cash, he warned her to stop counting or otherwise she would be dead.  She then placed a total of HK$14,000 into his bag and gave it to him.  He fled with the money, leaving the note behind.  The robbery was witnessed by other bank staff and captured on a CCTV cam""",
        charges="""At the leave hearing on 4 November 2025, the applicant appeared in person, having had legal aid refused on 12 May 2025.  At the conclusion of the hearing, I granted the applicant leave to appeal his sentence and an appeal aid certificate so that he would be legally represented on his appeal.  I said I would hand down my reasons in due course.  These are my reasons. In order to have a proper unders""",
        ordinance_refs="",
        outcome="""IN THE HIGH COURT OF THE HONG KONG SPECIAL ADMINISTRATIVE REGION COURT OF APPEAL CRIMINAL APPEAL NO 59 OF 2025 (ON APPEAL FROM HCCC NO 180 OF 2023) _______________ BETWEEN HKSAR	Respondent and Leong H""",
        sentence="",
        legal_principles=[
            "Criminal appeal principles apply"
        ],
        keywords=["robbery", "firearm"]
    ),
    CriminalCase(
        case_id="CACC000068",
        case_name="",
        year=2025,
        court="Court of Appeal",
        facts="""The applicant is a Form 8 Recognizance holder, whose refoulement application has been refused.  As a result of his immigration status, he was required to report to the Immigration Department, but stopped doing so in November 2022.  He was placed on a wanted list and subsequently arrested.  Since 12 August 2024, he has been remanded in custody pending repatriation.  I am informed that he has refused to provide details of his travel documents and personal particulars, which has caused a delay in the processing of his repatriation. On 3 April 2025, the applicant filed a notice for leave to appeal against conviction and sentence out of time by approximately three years and seven months.  The applicant appears in person in his leave application, having had legal aid refused on 16 May 2025. The """,
        charges="""The applicant is a Form 8 Recognizance holder, whose refoulement application has been refused.  As a result of his immigration status, he was required to report to the Immigration Department, but stopped doing so in November 2022.  He was placed on a wanted list and subsequently arrested.  Since 12 August 2024, he has been remanded in custody pending repatriation.  I am informed that he has refuse""",
        ordinance_refs="",
        outcome="""IN THE HIGH COURT OF THE HONG KONG SPECIAL ADMINISTRATIVE REGION COURT OF APPEAL CRIMINAL APPEAL NO 68 OF 2025 (ON APPEAL FROM DCCC NO 895 OF 2020) _______________ BETWEEN HKSAR	Respondent and HOSSAIN""",
        sentence="",
        legal_principles=[
            "Criminal appeal principles apply"
        ],
        keywords=["theft", "robbery"]
    ),
    CriminalCase(
        case_id="CACC000104",
        case_name="",
        year=2025,
        court="Court of Appeal",
        facts="""At about 11 am on 3 March 2020, five masked and gloved men, including D2 and D3, entered a ground-floor jewellery and goldsmith shop (“the shop”) in Yuen Long, New Territories.  At the time, there were six staff members working in the shop, but no customers.  All five men had alighted from a vehicle driven by the applicant, who promptly drove off to wait for them nearby.  On entering the shop, one of the five robbers pointed a knife at staff members while others smashed the glass display units with an axe and two hammers.  A total of 7 gold rings and 71 gold bracelets valued at HK$605,091 were stolen.  The whole robbery was carried out within two minutes. The vehicle used in the robbery was discovered later that day and found to have been stolen a week or so earlier.  After some arrests, o""",
        charges="""Background of the applicant and mitigation The applicant was 53 years old at the time of sentencing.  He was single and had come to Hong Kong from Pakistan in 1990.  He had had several appearances and convictions before the courts since 2014 involving offences of possession of dangerous drugs, trafficking in dangerous drugs, theft as well as various driving offences, among them dangerous driving. """,
        ordinance_refs="",
        outcome="""in the high court of the hong kong special administrative region court of appeal criminal appeal no 104 of 2025 (on appeal from hccc NO 193 of 2024) BETWEEN Before: Hon Macrae Acting CJHC in Court Dat""",
        sentence="",
        legal_principles=[
            "Criminal appeal principles apply"
        ],
        keywords=["theft", "robbery", "drug", "possession", "trafficking", "firearm"]
    ),
    CriminalCase(
        case_id="CACC000137",
        case_name="",
        year=2025,
        court="Court of Appeal",
        facts="""At the time of sentencing, the applicant was 50 years old, educated to Form 3 level, and living in a public housing unit with his parents.  He had a 15-year-old daughter who lived with his ex-wife.  He had worked in casual jobs earning HK$20,000 per month, but was unemployed prior to his arrest. Among the applicant’s 15 previous convictions, three were for possession of dangerous drugs in July 1999, May 2001 and March 2002; and two were for trafficking in dangerous drugs in June 2014 and November 2018, for which he was sentenced in the High Court to 5 years’ imprisonment and 7 years and 4 months’ imprisonment, respectively.  He committed the present offence three months after his release from prison on 30 June 2022. In sentencing the applicant, the judge identified the starting points as 7""",
        charges="""In sentencing the applicant, the judge identified the starting points as 7 to 11 years’ imprisonment for the 22.3 grammes of Ice, and 2 to 5 years’ imprisonment for the 0.22 gramme of heroin, according to the applicable guideline bands.  Applying the sentencing approach in HKSAR v Islam SM Majharul and HKSAR v Herry Jane Yusuph, the judge considered the applicant’s role as a courier and adopted a """,
        ordinance_refs="",
        outcome="""IN THE HIGH COURT OF THE HONG KONG SPECIAL ADMINISTRATIVE REGION COURT OF APPEAL CRIMINAL APPEAL NO 137 OF 2025 (ON APPEAL FROM HCCC NO 135 OF 2024) _______________ BETWEEN HKSAR	Respondent and Tai Si""",
        sentence="",
        legal_principles=[
            "Criminal appeal principles apply"
        ],
        keywords=["drug", "possession", "trafficking"]
    ),
    CriminalCase(
        case_id="CACC000225A",
        case_name="",
        year=2020,
        court="Court of Appeal",
        facts="""So the application from the defence is refused.” DCCC 346 and 625/2019 On 11 December 2020, in DCCC 346 and 625/2019, the appellant pleaded guilty to 16 charges of fraud (Charges 1 to 3, 6, 9, 10, 13, 14, 17, 18, 21, 22, 25, 26, 29, and 32), 7 charges of driving without a valid driving licence (Charges 4, 7, 11, 15, 19, 23 and 27), 7 charges of using a motor vehicle without third-party insurance (Charges 5, 8, 12, 16, 20, 24 and 28), 1 charge of possession of an identity card relating to another person (Charge 30), 1 charge of failing to surrender to custody without reasonable cause (Charge 31), and 3 charges of theft (Charges 33 to 35).  On the same day, he was sentenced to imprisonment for 56 months and 120 days (the equivalent of 5 years’ imprisonment) and disqualified from driving or h""",
        charges="""The appellant is an unrepentant recidivist with a long list of convictions for offences involving fraud and dishonesty.  He committed a spree of crimes for which he was eventually charged and brought before the courts.  Two cases were consolidated and transferred to the District Court (DCCC 346 and 625/2019).  Sometime later, two other cases were transferred consecutively to the District Court (DC""",
        ordinance_refs="",
        outcome="""CRIMINAL APPEAL NO 225 OF 2020, NOS 5 & 9 OF 2021 (ON APPEAL FROM DCCC NOS 346 & 625 OF 2019, 365 & 626 OF 2020) _______________ HKSAR	Respondent v LAM SEE CHUNG STEPHEN	Appellant _______________ Befo""",
        sentence="",
        legal_principles=[
            "Criminal appeal principles apply"
        ],
        keywords=["theft", "fraud", "possession"]
    ),
]

# Categorize cases
CASES_BY_CATEGORY = {}
for case in ALL_CRIMINAL_CASES:
    for keyword in case.keywords:
        if keyword not in CASES_BY_CATEGORY:
            CASES_BY_CATEGORY[keyword] = []
        CASES_BY_CATEGORY[keyword].append(case)

# All cases list (for backward compatibility)
ALL_CASES = ALL_CRIMINAL_CASES
ALL_LEGAL_CASES = ALL_CRIMINAL_CASES

# Statistics
TOTAL_CASES = len(ALL_CASES)

def get_case_by_id(case_id):
    """Get case by ID"""
    for case in ALL_CASES:
        if case.case_id == case_id:
            return case
    return None

def search_cases_by_keyword(keyword):
    """Search cases by keyword"""
    keyword_lower = keyword.lower()
    results = []
    for case in ALL_CASES:
        if keyword_lower in ' '.join(case.keywords).lower():
            results.append(case)
    return results

# Export
__all__ = [
    'CriminalCase',
    'ALL_CASES',
    'ALL_CRIMINAL_CASES',
    'ALL_LEGAL_CASES',
    'TOTAL_CASES',
    'CASES_BY_CATEGORY',
    'get_case_by_id',
    'search_cases_by_keyword'
]

if __name__ == '__main__':
    print(f"Hong Kong Criminal Appeal Cases Database")
    print(f"Total cases: {TOTAL_CASES}")
    print(f"\nSample cases:")
    for case in ALL_CASES[:3]:
        print(f"  - {case}")
