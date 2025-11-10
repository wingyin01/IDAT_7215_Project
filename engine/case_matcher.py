"""
Case Matcher using TF-IDF and Cosine Similarity
Finds similar past cases based on fact similarity
"""

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# Import comprehensive case database
try:
    from knowledge_base.all_cases_database import ALL_LEGAL_CASES as ALL_CASES
except ImportError:
    from knowledge_base.case_database import ALL_CASES

class CaseMatcher:
    """
    Matches cases using TF-IDF vectorization and cosine similarity
    """
    
    def __init__(self, cases=None):
        """
        Initialize the case matcher
        
        Args:
            cases: List of CriminalCase objects. If None, uses ALL_CASES from database
        """
        self.cases = cases if cases is not None else ALL_CASES
        self.vectorizer = None
        self.case_vectors = None
        self._prepare_vectorizer()
    
    def _prepare_vectorizer(self):
        """Prepare TF-IDF vectorizer and compute vectors for all cases"""
        if not self.cases:
            return
        
        # Extract facts text from all cases (combine facts, legal principles, and keywords)
        case_texts = []
        for case in self.cases:
            combined_text = (
                case.facts + " " +
                " ".join(case.legal_principles) + " " +
                " ".join(case.keywords)
            )
            case_texts.append(combined_text)
        
        # Create TF-IDF vectorizer
        self.vectorizer = TfidfVectorizer(
            max_features=500,
            stop_words='english',
            ngram_range=(1, 2),  # Use unigrams and bigrams
            min_df=1
        )
        
        # Fit and transform case texts
        self.case_vectors = self.vectorizer.fit_transform(case_texts)
    
    def find_similar_cases(self, query_text, top_n=5, min_similarity=0.1):
        """
        Find most similar cases to the query
        
        Args:
            query_text: Text description of facts/situation
            top_n: Number of similar cases to return
            min_similarity: Minimum similarity threshold (0-1)
        
        Returns:
            List of tuples (case, similarity_score)
        """
        if self.vectorizer is None:
            return []
        
        # Transform query text
        query_vector = self.vectorizer.transform([query_text])
        
        # Compute cosine similarity
        similarities = cosine_similarity(query_vector, self.case_vectors)[0]
        
        # Get top N cases
        top_indices = np.argsort(similarities)[::-1][:top_n]
        
        results = []
        for idx in top_indices:
            if similarities[idx] >= min_similarity:
                results.append((self.cases[idx], float(similarities[idx])))
        
        return results
    
    def find_similar_by_facts(self, facts_list, top_n=5):
        """
        Find similar cases given a list of facts
        
        Args:
            facts_list: List of fact strings
            top_n: Number of cases to return
        
        Returns:
            List of tuples (case, similarity_score)
        """
        query_text = " ".join(facts_list)
        return self.find_similar_cases(query_text, top_n)
    
    def find_by_ordinance(self, chapter, section=None):
        """
        Find cases involving specific ordinance
        
        Args:
            chapter: Chapter number (e.g., "200", "210")
            section: Optional section number
        
        Returns:
            List of matching cases
        """
        matching_cases = []
        for case in self.cases:
            for ref in case.ordinance_refs:
                if f"Cap. {chapter}" in ref:
                    if section is None or f"s.{section}" in ref:
                        matching_cases.append(case)
                        break
        return matching_cases
    
    def find_by_keyword(self, keyword):
        """
        Find cases by keyword
        
        Args:
            keyword: Search keyword
        
        Returns:
            List of matching cases
        """
        keyword_lower = keyword.lower()
        matching_cases = []
        
        for case in self.cases:
            if (keyword_lower in case.facts.lower() or
                keyword_lower in " ".join(case.keywords).lower() or
                keyword_lower in case.case_name.lower()):
                matching_cases.append(case)
        
        return matching_cases
    
    def find_by_outcome(self, outcome):
        """
        Find cases with specific outcome
        
        Args:
            outcome: "Guilty", "Not Guilty", etc.
        
        Returns:
            List of matching cases
        """
        return [case for case in self.cases if case.outcome == outcome]
    
    def compare_cases(self, case1, case2):
        """
        Compare two cases and return similarity score
        
        Args:
            case1: First case (CriminalCase object or text)
            case2: Second case (CriminalCase object or text)
        
        Returns:
            Similarity score (0-1)
        """
        if self.vectorizer is None:
            return 0.0
        
        # Extract text from cases
        text1 = case1.facts if hasattr(case1, 'facts') else str(case1)
        text2 = case2.facts if hasattr(case2, 'facts') else str(case2)
        
        # Vectorize
        vec1 = self.vectorizer.transform([text1])
        vec2 = self.vectorizer.transform([text2])
        
        # Compute similarity
        similarity = cosine_similarity(vec1, vec2)[0][0]
        return float(similarity)
    
    def get_case_summary(self, case, similarity_score=None):
        """
        Get a formatted summary of a case
        
        Args:
            case: CriminalCase object
            similarity_score: Optional similarity score
        
        Returns:
            Formatted string summary
        """
        summary = []
        
        if similarity_score is not None:
            summary.append(f"Similarity: {similarity_score:.2%}")
            summary.append("")
        
        summary.append(f"Case: {case.case_name} ({case.year})")
        summary.append(f"Court: {case.court}")
        summary.append(f"Outcome: {case.outcome}")
        summary.append(f"Sentence: {case.sentence}")
        summary.append("")
        
        summary.append("Facts:")
        summary.append(case.facts[:300] + "..." if len(case.facts) > 300 else case.facts)
        summary.append("")
        
        summary.append("Charges:")
        for charge in case.charges:
            summary.append(f"  - {charge}")
        summary.append("")
        
        summary.append("Legal Principles:")
        for principle in case.legal_principles:
            summary.append(f"  - {principle}")
        
        return "\n".join(summary)
    
    def generate_case_analysis_report(self, query_text, top_n=3):
        """
        Generate comprehensive case analysis report
        
        Args:
            query_text: Query facts text
            top_n: Number of similar cases to include
        
        Returns:
            Formatted report string
        """
        similar_cases = self.find_similar_cases(query_text, top_n)
        
        if not similar_cases:
            return "No similar cases found in the database."
        
        report = []
        report.append("=" * 60)
        report.append("SIMILAR CASE ANALYSIS REPORT")
        report.append("=" * 60)
        report.append("")
        
        report.append("Query Facts:")
        report.append(query_text[:500] + "..." if len(query_text) > 500 else query_text)
        report.append("")
        report.append(f"Found {len(similar_cases)} similar case(s):")
        report.append("")
        
        for idx, (case, score) in enumerate(similar_cases, 1):
            report.append("-" * 60)
            report.append(f"SIMILAR CASE #{idx}")
            report.append("-" * 60)
            report.append(self.get_case_summary(case, score))
            report.append("")
        
        return "\n".join(report)


# Global case matcher instance
_global_matcher = None

def get_case_matcher():
    """Get or create global case matcher instance"""
    global _global_matcher
    if _global_matcher is None:
        _global_matcher = CaseMatcher()
    return _global_matcher


if __name__ == '__main__':
    print("=== Testing Case Matcher ===\n")
    
    # Create matcher
    matcher = CaseMatcher()
    
    # Test 1: Find similar cases for theft scenario
    print("Test 1: Finding similar cases for theft scenario")
    print("-" * 60)
    
    query1 = """
    A person entered a store at night, took expensive items worth HK$10,000
    without paying, and left. CCTV showed him concealing items. He intended
    to keep them permanently.
    """
    
    results1 = matcher.find_similar_cases(query1, top_n=3)
    print(f"Found {len(results1)} similar cases:\n")
    for case, score in results1:
        print(f"- {case.case_name} ({case.year}): {score:.2%} similar")
        print(f"  Charges: {', '.join(case.charges)}")
        print()
    
    print("\n" + "=" * 60 + "\n")
    
    # Test 2: Find similar cases for violent robbery
    print("Test 2: Finding similar cases for violent robbery")
    print("-" * 60)
    
    query2 = """
    A person threatened a victim with a knife and demanded their wallet and phone.
    The victim was scared and handed over the items. The attacker fled with property
    worth HK$20,000.
    """
    
    results2 = matcher.find_similar_cases(query2, top_n=3)
    print(f"Found {len(results2)} similar cases:\n")
    for case, score in results2:
        print(f"- {case.case_name} ({case.year}): {score:.2%} similar")
        print(f"  Outcome: {case.outcome}, Sentence: {case.sentence}")
        print()
    
    print("\n" + "=" * 60 + "\n")
    
    # Test 3: Generate full report
    print("Test 3: Full Case Analysis Report")
    print("=" * 60)
    
    report = matcher.generate_case_analysis_report(query2, top_n=2)
    print(report)

