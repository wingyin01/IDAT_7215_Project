"""
Enhanced Legal Analyzer
Combines rule-based inference with semantic search and context analysis
Provides detailed, realistic legal advice
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from engine.document_analyzer import DocumentAnalyzer
from engine.rule_engine import analyze_case
from engine.context_analyzer import ContextAnalyzer
from engine.hybrid_search import HybridSearchEngine
from engine.risk_assessor import get_risk_assessor
from engine.risk_assessor import get_risk_assessor

# Cache directory
CACHE_DIR = Path(__file__).parent.parent / "knowledge_base" / "cached_embeddings"

class EnhancedLegalAnalyzer:
    """Enhanced analyzer with semantic search + rules + context"""
    
    def __init__(self):
        self.doc_analyzer = DocumentAnalyzer()
        self.context_analyzer = ContextAnalyzer()
        
        # Load search engine for finding relevant laws
        self.search_engine = None
        if CACHE_DIR.exists():
            try:
                self.search_engine = HybridSearchEngine()
                self.search_engine.load_index(CACHE_DIR)
            except:
                print("⚠️ Could not load search engine for enhanced analysis")
    
    def analyze(self, text):
        """
        Comprehensive analysis with context awareness
        
        Args:
            text: User's query or scenario description
        
        Returns:
            dict: Complete analysis with context, laws, and advice
        """
        # Check if text is empty or trivial
        if not text or len(text.strip()) < 3:
            return {
                'success': False,
                'comprehensive_advice': '### ⚠️ NO INPUT PROVIDED\n\nPlease provide a scenario or legal question to analyze.'
            }
        
        # Step 1: Document analysis
        doc_analysis = self.doc_analyzer.analyze_document(text)
        
        # Step 2: Extract context (amounts, severity)
        context = self.context_analyzer.assess_theft_severity(text)
        
        # Step 3: Semantic search for relevant laws
        relevant_laws = []
        
        # First, add essential definitional sections for detected offenses
        offences_list = doc_analysis.get('offences', [])
        has_theft = (offences_list and 'theft' in offences_list[0].get('type', '')) or \
                    any(word in text.lower() for word in ['steal', 'stole', 'theft', 'shoplifting'])
        
        if has_theft:
            # Force-add Cap. 210 theft sections
            from knowledge_base import json_loader
            theft_def = json_loader.get_ordinance_section('210', '2')
            theft_penalty = json_loader.get_ordinance_section('210', '9')
            
            if theft_def:
                relevant_laws.append({
                    'reference': 'Cap. 210, s.2',
                    'title': theft_def.get('title', 'Basic definition of theft'),
                    'text': theft_def.get('text', '')[:300],
                    'penalty': theft_def.get('penalty', ''),
                    'score': 1.0  # Top priority
                })
            
            if theft_penalty:
                relevant_laws.append({
                    'reference': 'Cap. 210, s.9',
                    'title': theft_penalty.get('title', 'Punishment for theft'),
                    'text': theft_penalty.get('text', '')[:300],
                    'penalty': theft_penalty.get('penalty', ''),
                    'score': 0.95  # High priority
                })
        
        if self.search_engine:
            # Search for additional relevant legislation
            results = self.search_engine.search_legislation_only(text, top_k=10)
            
            # Prioritize definitional sections
            prioritized_results = []
            for result in results:
                metadata = result['metadata']
                score = result['hybrid_score']
                
                # Boost key definitional sections
                if (metadata['chapter'] == '210' and metadata['section'] == '2'):
                    score *= 2.0  # Double boost for Cap. 210, s.2 (theft definition)
                elif (metadata['chapter'] == '210' and metadata['section'] == '9'):
                    score *= 1.5  # Boost for Cap. 210, s.9 (theft penalty)
                elif 'definition' in metadata['title'].lower() or 'basic' in metadata['title'].lower():
                    score *= 1.3  # Boost for definition sections
                
                prioritized_results.append((score, result))
            
            # Re-sort by boosted scores
            prioritized_results.sort(key=lambda x: x[0], reverse=True)
            
            for score, result in prioritized_results[:8]:
                metadata = result['metadata']
                relevant_laws.append({
                    'reference': f"Cap. {metadata['chapter']}, s.{metadata['section']}",
                    'title': metadata['title'],
                    'text': metadata['text'][:300],
                    'penalty': metadata.get('penalty', ''),
                    'score': score  # Use boosted score
                })
        
        # Step 4: Traditional rule-based analysis
        extracted_facts = self.doc_analyzer.extract_for_inference(text)
        rule_results = None
        has_offense = False
        
        if extracted_facts:
            try:
                engine = analyze_case(extracted_facts)
                offences = engine.get_offences()
                if offences:
                    has_offense = True
                    # Convert offences to JSON-serializable format (remove Rule objects)
                    serializable_offences = [
                        {
                            'offence': o['offence'],
                            'ordinance_ref': o['ordinance_ref'],
                            'penalty': o['penalty']
                        } for o in offences
                    ]
                    rule_results = {
                        'offences': serializable_offences,
                        'explanation': engine.explain()
                    }
            except Exception as e:
                print(f"Warning: Rule-based analysis failed: {e}")
                # Continue without rule results
        
        # If no offense detected from rules, check if we should proceed
        # Only proceed if we have BOTH offense detection AND high-relevance legislation
        if not has_offense:
            # Check if we have any highly relevant legislation (score > 0.5)
            high_relevance_laws = [law for law in relevant_laws if law.get('score', 0) > 0.5]
            
            if not high_relevance_laws:
                # No offense detected and no highly relevant laws
                return {
                    'success': True,
                    'comprehensive_advice': self._generate_no_offense_message(text),
                    'document_analysis': doc_analysis,
                    'context_assessment': context,
                    'relevant_laws': [],
                    'rule_based_results': None,
                    'risk_assessment': None
                }
        
        # Step 5: Risk assessment
        risk_assessor = get_risk_assessor()
        offense_type = 'theft'  # Default
        if doc_analysis.get('offences') and len(doc_analysis['offences']) > 0:
            offense_type = doc_analysis['offences'][0].get('type', 'theft')
        
        risk_assessment = risk_assessor.comprehensive_risk_assessment(text, context, offense_type='theft')
        
        # Step 6: Generate comprehensive advice
        advice = self._generate_comprehensive_advice(
            text, doc_analysis, context, relevant_laws, rule_results, risk_assessment
        )
        
        return {
            'document_analysis': doc_analysis,
            'context_assessment': context,
            'relevant_laws': relevant_laws,
            'rule_based_results': rule_results,
            'risk_assessment': risk_assessment,
            'comprehensive_advice': advice,
            'success': True
        }
    
    def _generate_comprehensive_advice(self, text, doc_analysis, context, laws, rules, risk=None):
        """Generate comprehensive legal advice"""
        sections = []
        
        # 1. Offense Identification
        sections.append("### 🔴 OFFENSE IDENTIFICATION\n")
        
        if rules and rules['offences']:
            for offence in rules['offences']:
                sections.append(f"**{offence['offence']}** ({offence['ordinance_ref']})\n")
                sections.append(f"- Maximum Penalty: {offence['penalty']}\n")
        elif laws:
            # Use semantic search results
            sections.append(f"**Potential Offense**: Based on the scenario\n")
            sections.append(f"- Most relevant law: {laws[0]['reference']} - {laws[0]['title']}\n")
        else:
            sections.append(f"**No specific offense identified by rule engine**\n")
            sections.append(f"- Analysis based on legislation search\n")
        
        # 2. Context & Severity
        if context['severity'] != 'unknown':
            sections.append(f"\n### ⚖️ SEVERITY ASSESSMENT: {context['category']}\n")
            
            if context.get('amount'):
                sections.append(f"**Property Value**: HK${context['amount']}\n\n")
            
            sections.append("**Context Considerations**:\n")
            for consideration in context['considerations']:
                sections.append(f"- {consideration}\n")
        
        # 3. Relevant Laws
        sections.append("\n### 📖 RELEVANT LEGISLATION\n")
        for law in laws[:3]:  # Top 3 most relevant
            sections.append(f"\n**{law['reference']}**: {law['title']}\n")
            sections.append(f"- {law['text']}...\n")
            if law['penalty']:
                sections.append(f"- **Penalty**: {law['penalty']}\n")
        
        # 4. Aggravating/Mitigating Factors
        if context.get('aggravating_factors'):
            sections.append("\n### ⚠️ AGGRAVATING FACTORS\n")
            for factor in context['aggravating_factors']:
                sections.append(f"- {factor}\n")
        
        if context.get('mitigation_factors'):
            sections.append("\n### ✓ MITIGATING FACTORS\n")
            for factor in context['mitigation_factors']:
                sections.append(f"- {factor}\n")
        
        # 5. Risk Assessment & Prediction (REMOVED DUPLICATE - handled in section 6 below)
        
        # 6. Practical Advice
        if context.get('practical_advice'):
            sections.append("\n### 💼 PRACTICAL ADVICE\n")
            for advice in context['practical_advice']:
                sections.append(f"- {advice}\n")
        
        # 6. Risk Assessment & Prediction
        if risk:
            sections.append("\n### ⚠️ RISK ASSESSMENT & PREDICTION\n")
            sections.append(f"**Overall Risk Level**: {risk['risk_level']['level']} ({risk['risk_level']['score']}/100)\n\n")
            
            # Prosecution likelihood
            prosecution = risk['prosecution']
            sections.append(f"**Prosecution Likelihood**: {prosecution['likelihood']}% ({prosecution['category']})\n")
            if prosecution.get('adjustments'):
                sections.append("- Factors considered:\n")
                for adj, reason in prosecution['adjustments']:
                    sections.append(f"  - {reason} ({adj})\n")
            sections.append("\n")
            
            # Sentence prediction
            sent_pred = risk['sentence_prediction']
            
            # Check if this is a fine-only offense
            if sent_pred.get('is_fine_only', False):
                sections.append(f"**Penalty**: Fine Only (No Prison)\n")
                sections.append(f"- **Fine Range**: HK${sent_pred.get('fine_range', 'Unknown')}\n")
                sections.append(f"- This is a regulatory offense with fixed penalty\n")
                sections.append(f"- **No imprisonment** for this offense\n")
                sections.append(f"- Confidence: {sent_pred['confidence']}%\n")
                sections.append(f"- {sent_pred['basis']}\n\n")
            else:
                # Prison sentence possible
                sections.append(f"**Predicted Sentence Range**:\n")
                
                risk_assessor = get_risk_assessor()
                low_text = risk_assessor.format_months_to_text(sent_pred['low_months'])
                typical_text = risk_assessor.format_months_to_text(sent_pred['typical_months'])
                high_text = risk_assessor.format_months_to_text(sent_pred['high_months'])
                
                sections.append(f"- Low estimate: {low_text}\n")
                sections.append(f"- **Typical sentence: {typical_text}**\n")
                sections.append(f"- High estimate: {high_text}\n")
                sections.append(f"- Confidence: {sent_pred['confidence']}%\n")
                sections.append(f"- {sent_pred['basis']}\n")
                
                if sent_pred.get('adjustments'):
                    sections.append("\n- Sentence adjustments:\n")
                    for adj in sent_pred['adjustments']:
                        sections.append(f"  - {adj}\n")
                sections.append("\n")
            
            # Outcome probabilities
            outcomes = risk['outcome_probabilities']
            sections.append(f"**Outcome Probabilities**:\n")
            sections.append(f"- Conviction likelihood: {outcomes['conviction_likelihood']}%\n")
            sections.append(f"- Custodial (prison) sentence: {outcomes['custodial_sentence']}%\n")
            sections.append(f"- Non-custodial options: {outcomes['non_custodial']}%\n")
            sections.append(f"- Appeal success rate: {outcomes['appeal_success_rate']}% (based on real HK cases)\n")
            sections.append("\n")
        
        # 7. Legal Process (adjust based on offense severity)
        sections.append("\n### 📋 LEGAL PROCESS\n")
        if risk and risk['sentence_prediction'].get('is_fine_only'):
            sections.append("- **If caught**: Usually issued fixed penalty notice on the spot\n")
            sections.append("- **Payment**: Pay fine within specified time period\n")
            sections.append("- **If don't pay**: May be summoned to court for prosecution\n")
        else:
            sections.append("- **If arrested**: Right to remain silent, right to legal representation\n")
            sections.append("- **If charged**: Will be brought to court, may apply for bail\n")
            sections.append("- **Possible outcomes**: Caution, bind-over, conviction, imprisonment\n")
        
        # 8. Important Notes
        sections.append("\n### ⚠️ IMPORTANT DISCLAIMER\n")
        sections.append("- This is general legal information, NOT legal advice\n")
        sections.append("- Every case has unique circumstances\n")
        sections.append("- Consult a qualified Hong Kong criminal defense lawyer\n")
        sections.append("- Do not rely solely on this analysis for legal decisions\n")
        
        return ''.join(sections)
    
    def _generate_no_offense_message(self, text):
        """Generate message when no offense is detected"""
        return f"""### ✅ NO LEGAL VIOLATION DETECTED

**Your Input**: "{text}"

**Analysis Result**: This appears to be **legal conduct** under Hong Kong law. No criminal offense or regulatory violation was detected.

---

### 🎉 Good News!

Based on our analysis:
- ✅ **No criminal offense** identified
- ✅ **No regulatory violation** found
- ✅ **No legal rules** matched this scenario

**This is a normal, legal activity.**

---

### 💡 If This Doesn't Seem Right

If you expected this to be illegal, consider:

1. **Add more details** - Our system needs specific facts
   - Example: Instead of "I took something", try "I took a phone from a store without paying"

2. **Try Expert Mode (RAG)** 🚀
   - Uses AI for broader legal analysis
   - Can handle more complex queries
   - Better for unusual scenarios

3. **Consult a lawyer** for complex matters
   - Our system focuses on common offenses
   - Civil matters require professional advice

---

### 📚 What Our System Has

**Legislation Database** (Complete):
✅ **ALL Hong Kong Law** - 2,234 ordinances, 52,269 sections
✅ Criminal Law, Civil Law, Property, Employment, Commercial, Tax, Family Law, etc.

**Rule-Based Analysis** (Focused):
✅ Common criminal offenses (theft, assault, robbery, drugs, etc.)
✅ Regulatory offenses (smoking, littering, noise, etc.)
✅ Animal welfare violations
⚠️ Limited civil/commercial rules (use **Expert Mode** for these)

**Best Approach**:
- **Simple scenarios** → Rule-Based Analysis (fast, focused)
- **Complex queries** → Expert Mode (RAG) 🚀 (uses ALL legislation with AI)

---

⚠️ **Disclaimer**: This is general information. For actual legal matters, consult a qualified Hong Kong solicitor.
"""

# Singleton instance
_enhanced_analyzer = None

def get_enhanced_analyzer():
    """Get or create enhanced analyzer instance"""
    global _enhanced_analyzer
    if _enhanced_analyzer is None:
        _enhanced_analyzer = EnhancedLegalAnalyzer()
    return _enhanced_analyzer

