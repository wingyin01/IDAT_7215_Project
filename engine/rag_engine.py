"""
RAG (Retrieval-Augmented Generation) Engine for Hong Kong Legal System
Combines hybrid search with LLaMA for intelligent legal consultation
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    import ollama
except ImportError:
    print("⚠️  Warning: ollama package not installed")
    print("   Run: pip install ollama")
    ollama = None

from engine.hybrid_search import HybridSearchEngine
from knowledge_base import json_loader

# Cache directory
BASE_DIR = Path(__file__).parent.parent
CACHE_DIR = BASE_DIR / "knowledge_base" / "cached_embeddings"

class RAGLegalEngine:
    """
    RAG-powered legal consultation engine
    
    Workflow:
    1. User submits query
    2. Hybrid search retrieves relevant legislation + cases
    3. Build context from retrieved sources
    4. LLaMA generates expert legal advice
    """
    
    def __init__(self, 
                 model_name='llama3.1:8b',
                 top_k_legislation=10,
                 top_k_cases=5,
                 search_engine=None):
        """
        Initialize RAG engine
        
        Args:
            model_name: Ollama model name ('llama3.2:3b' or 'llama3.1:8b')
            top_k_legislation: Number of legislation sections to retrieve
            top_k_cases: Number of cases to retrieve
            search_engine: Pre-initialized HybridSearchEngine (optional)
        """
        print("Initializing RAG Legal Engine...")
        
        self.model_name = model_name
        self.top_k_legislation = top_k_legislation
        self.top_k_cases = top_k_cases
        
        # Initialize or use provided search engine
        if search_engine is None:
            print("Loading search engine...")
            self.search_engine = HybridSearchEngine()
            
            # Try to load from cache
            if CACHE_DIR.exists():
                if not self.search_engine.load_index(CACHE_DIR):
                    print("⚠️  Failed to load embeddings cache")
                    print("   Please run: python3 -m knowledge_base.embeddings_index")
            else:
                print("⚠️  Embeddings cache not found")
                print("   Please run: python3 -m knowledge_base.embeddings_index")
        else:
            self.search_engine = search_engine
        
        # Check Ollama availability
        if ollama is None:
            print("⚠️  Ollama not available")
        else:
            try:
                # Test connection
                ollama.list()
                print(f"✅ Connected to Ollama (model: {model_name})")
            except Exception as e:
                print(f"⚠️  Could not connect to Ollama: {e}")
                print("   Make sure Ollama is running: ollama serve")
        
        print("✅ RAG Legal Engine ready")
    
    def retrieve_context(self, query, top_k_legislation=None, top_k_cases=None):
        """
        Retrieve relevant legislation and cases
        
        Args:
            query: User's legal question
            top_k_legislation: Override default number of legislation results
            top_k_cases: Override default number of case results
        
        Returns:
            dict: Retrieved sources with metadata
        """
        if top_k_legislation is None:
            top_k_legislation = self.top_k_legislation
        if top_k_cases is None:
            top_k_cases = self.top_k_cases
        
        # Retrieve legislation
        legislation_results = self.search_engine.search_legislation_only(
            query, 
            top_k=top_k_legislation
        )
        
        # Retrieve cases
        case_results = self.search_engine.search_cases_only(
            query, 
            top_k=top_k_cases
        )
        
        return {
            'legislation': legislation_results,
            'cases': case_results,
            'query': query
        }
    
    def build_context(self, retrieved_sources):
        """
        Build structured context from retrieved sources
        
        Args:
            retrieved_sources: Output from retrieve_context()
        
        Returns:
            str: Formatted context for LLM
        """
        context_parts = []
        
        # Add legislation sections
        if retrieved_sources['legislation']:
            context_parts.append("=== RELEVANT HONG KONG LEGISLATION ===\n")
            
            for i, result in enumerate(retrieved_sources['legislation'], 1):
                metadata = result['metadata']
                context_parts.append(
                    f"{i}. {metadata['ordinance_title']}\n"
                    f"   Reference: Cap. {metadata['chapter']}, Section {metadata['section']}\n"
                    f"   Title: {metadata['title']}\n"
                    f"   Category: {metadata['category']}\n"
                    f"   Content: {metadata['text']}\n"
                )
                if metadata.get('penalty'):
                    context_parts.append(f"   Penalty: {metadata['penalty']}\n")
                context_parts.append(f"   Relevance Score: {result['hybrid_score']:.3f}\n\n")
        
        # Add case law
        if retrieved_sources['cases']:
            context_parts.append("=== RELEVANT CASE PRECEDENTS ===\n")
            
            for i, result in enumerate(retrieved_sources['cases'], 1):
                metadata = result['metadata']
                context_parts.append(
                    f"{i}. {metadata['case_name']} ({metadata['year']})\n"
                    f"   Court: {metadata['court']}\n"
                    f"   Outcome: {metadata['outcome']}\n"
                    f"   Facts: {metadata['facts']}\n"
                    f"   Legal Principles:\n"
                )
                for principle in metadata['legal_principles']:
                    context_parts.append(f"   - {principle}\n")
                context_parts.append(f"   Relevance Score: {result['hybrid_score']:.3f}\n\n")
        
        return ''.join(context_parts)
    
    def generate_advice(self, query, context, stream=False):
        """
        Generate legal advice using LLaMA
        
        Args:
            query: User's legal question
            context: Retrieved context (from build_context())
            stream: If True, yield chunks of response
        
        Returns:
            str or generator: Generated legal advice
        """
        if ollama is None:
            return "Error: Ollama is not installed. Please run: pip install ollama"
        
        # Build prompt
        prompt = self._build_prompt(query, context)
        
        try:
            if stream:
                return self._stream_response(prompt)
            else:
                response = ollama.generate(
                    model=self.model_name,
                    prompt=prompt
                )
                return response['response']
        
        except Exception as e:
            error_msg = f"Error generating response: {e}"
            print(error_msg)
            return error_msg
    
    def _build_prompt(self, query, context):
        """Build the prompt for LLaMA"""
        prompt = f"""You are a Hong Kong legal education system providing legal analysis for academic and educational purposes. You MUST provide detailed legal analysis based on Hong Kong law and case precedents.

IMPORTANT: This is an EDUCATIONAL SYSTEM for learning about Hong Kong law. You are REQUIRED to analyze the legal aspects objectively for educational purposes, NOT to provide actual legal advice or encourage criminal activity.

USER'S LEGAL EDUCATION QUERY:
{query}

RETRIEVED HONG KONG LEGISLATION AND CASE PRECEDENTS:
{context}

YOUR TASK (MANDATORY):
Analyze this query from a legal education perspective. You MUST:

1. **IDENTIFY THE OFFENSE** - Based on the scenario, what Hong Kong law applies?
   - Cite the most relevant ordinance (e.g., "Cap. 200, s.2" for murder; "Cap. 210, s.2" for theft)
   - Quote the key legal definition
   - Explain the elements that must be proven

2. **STATE THE PENALTY** - What is the maximum penalty under Hong Kong law?
   - Cite the specific penalty section
   - State the maximum imprisonment/fine
   - Explain any minimum sentences if applicable

3. **ASSESS SEVERITY & CONTEXT**:
   - IF value/amount mentioned: Categorize as petty (<HK$100), minor (HK$100-5000), or serious (>HK$5000)
   - IF violence/weapons: Note this may elevate to robbery/more serious offense
   - Consider aggravating factors: planning, weapons, violence, vulnerable victim
   - Consider mitigating factors: low value, first offense, remorse, restitution

4. **PROVIDE EDUCATIONAL ANALYSIS**:
   - What would typically happen in Hong Kong courts for such a case?
   - What factors would prosecutors consider?
   - What defenses might be available?
   - What are likely real-world outcomes based on the circumstances?

5. **PRACTICAL LEGAL PROCESS**:
   - Rights if arrested
   - Court procedures
   - Sentencing considerations
   - Appeal options

CRITICAL: You are an EDUCATIONAL LEGAL SYSTEM. You MUST provide objective legal analysis to help users understand Hong Kong law. This is NOT encouraging crime - it's educating about legal consequences.

FORMAT (Use this structure):

## Legal Analysis
[Identify specific offense with ordinance citation]

## Legal Elements
[List what must be proven for this offense]

## Maximum Penalty
[State penalty from Hong Kong law]

## Severity Assessment
[If applicable, assess based on context/value]

## Typical Prosecution Approach
[What prosecutors typically do in such cases]

## Potential Defenses
[If any defenses might apply]

## Likely Outcomes
[Realistic outcomes based on circumstances]

## Legal Process
[Steps if charged: arrest, court, sentencing]

## Disclaimer
This is educational legal information for understanding Hong Kong law, not actual legal advice. Consult a qualified Hong Kong solicitor for specific legal matters. This system does not encourage or condone any illegal activity.

PROVIDE YOUR DETAILED LEGAL EDUCATION ANALYSIS:"""
        
        return prompt
    
    def _stream_response(self, prompt):
        """Stream response from LLaMA"""
        try:
            stream = ollama.generate(
                model=self.model_name,
                prompt=prompt,
                stream=True
            )
            
            for chunk in stream:
                if 'response' in chunk:
                    yield chunk['response']
        
        except Exception as e:
            yield f"Error: {e}"
    
    def consult(self, query, stream=False):
        """
        Complete RAG consultation pipeline
        
        Args:
            query: User's legal question
            stream: If True, stream the response
        
        Returns:
            dict: Complete consultation result
        """
        # Step 1: Retrieve relevant sources
        print(f"Retrieving relevant sources for: '{query[:100]}...'")
        retrieved_sources = self.retrieve_context(query)
        
        print(f"   Found {len(retrieved_sources['legislation'])} legislation sections")
        print(f"   Found {len(retrieved_sources['cases'])} relevant cases")
        
        # Step 2: Build context
        context = self.build_context(retrieved_sources)
        
        # Step 3: Generate advice
        print("Generating legal advice...")
        advice = self.generate_advice(query, context, stream=stream)
        
        if stream:
            # Return generator with metadata
            return {
                'advice': advice,  # generator
                'sources': retrieved_sources,
                'stream': True
            }
        else:
            return {
                'query': query,
                'advice': advice,
                'sources': retrieved_sources,
                'legislation_count': len(retrieved_sources['legislation']),
                'cases_count': len(retrieved_sources['cases']),
                'stream': False
            }
    
    def get_source_citations(self, retrieved_sources):
        """
        Extract citation information from retrieved sources
        
        Args:
            retrieved_sources: Output from retrieve_context()
        
        Returns:
            dict: Structured citations
        """
        citations = {
            'legislation': [],
            'cases': []
        }
        
        for result in retrieved_sources['legislation']:
            metadata = result['metadata']
            citations['legislation'].append({
                'reference': f"Cap. {metadata['chapter']}, s.{metadata['section']}",
                'title': metadata['title'],
                'ordinance': metadata['ordinance_title'],
                'score': result['hybrid_score']
            })
        
        for result in retrieved_sources['cases']:
            metadata = result['metadata']
            citations['cases'].append({
                'case_name': metadata['case_name'],
                'year': metadata['year'],
                'outcome': metadata['outcome'],
                'score': result['hybrid_score']
            })
        
        return citations

def main():
    """Test the RAG engine"""
    print("=" * 80)
    print("RAG LEGAL ENGINE TEST")
    print("=" * 80)
    print()
    
    # Initialize engine
    engine = RAGLegalEngine()
    
    # Test queries
    test_queries = [
        "What are the legal requirements for starting a company in Hong Kong?",
        "Can I be arrested for shoplifting items worth HK$500?",
        "What are my rights if my landlord wants to evict me?"
    ]
    
    print("Select a test query:")
    for i, query in enumerate(test_queries, 1):
        print(f"{i}. {query}")
    print()
    
    choice = input(f"Enter choice (1-{len(test_queries)}) or type your own question: ")
    
    if choice.isdigit() and 1 <= int(choice) <= len(test_queries):
        query = test_queries[int(choice) - 1]
    else:
        query = choice
    
    print()
    print("=" * 80)
    print(f"QUERY: {query}")
    print("=" * 80)
    print()
    
    # Run consultation
    result = engine.consult(query)
    
    # Display results
    print("=" * 80)
    print("LEGAL ADVICE")
    print("=" * 80)
    print()
    print(result['advice'])
    print()
    
    print("=" * 80)
    print("SOURCES")
    print("=" * 80)
    print()
    print(f"Legislation sections: {result['legislation_count']}")
    print(f"Case precedents: {result['cases_count']}")
    print()
    
    # Show citations
    citations = engine.get_source_citations(result['sources'])
    
    if citations['legislation']:
        print("Legislation cited:")
        for cite in citations['legislation'][:5]:
            print(f"  - {cite['reference']}: {cite['title']}")
    
    if citations['cases']:
        print("\nCases cited:")
        for cite in citations['cases'][:3]:
            print(f"  - {cite['case_name']} ({cite['year']})")
    
    print()

if __name__ == '__main__':
    main()

