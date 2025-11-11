"""
Hybrid Search Engine for Hong Kong Legal System
Combines semantic embeddings (sentence-transformers) with TF-IDF for better retrieval
"""

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer
import pickle
from pathlib import Path

class HybridSearchEngine:
    """
    Hybrid search combining semantic embeddings and TF-IDF
    
    Scoring: final_score = 0.7 * semantic_score + 0.3 * tfidf_score
    """
    
    def __init__(self, 
                 embedding_model_name='all-MiniLM-L6-v2',
                 semantic_weight=0.7,
                 tfidf_weight=0.3):
        """
        Initialize the hybrid search engine
        
        Args:
            embedding_model_name: Name of sentence-transformers model
            semantic_weight: Weight for semantic similarity (0-1)
            tfidf_weight: Weight for TF-IDF similarity (0-1)
        """
        print("Initializing Hybrid Search Engine...")
        print(f"Loading embedding model: {embedding_model_name}")
        
        self.embedding_model = SentenceTransformer(embedding_model_name)
        self.semantic_weight = semantic_weight
        self.tfidf_weight = tfidf_weight
        
        # TF-IDF components
        self.tfidf_vectorizer = TfidfVectorizer(
            max_features=1000,
            stop_words='english',
            ngram_range=(1, 2),
            min_df=1
        )
        
        # Storage for indexed data
        self.legislation_embeddings = None
        self.legislation_tfidf = None
        self.legislation_texts = []
        self.legislation_metadata = []
        
        self.case_embeddings = None
        self.case_tfidf = None
        self.case_texts = []
        self.case_metadata = []
        
        self.is_indexed = False
        
        print("✅ Hybrid Search Engine initialized")
    
    def index_legislation(self, ordinances_dict):
        """
        Index all legislation sections
        
        Args:
            ordinances_dict: Dictionary of ordinances from json_loader
        """
        print("Indexing legislation sections...")
        
        self.legislation_texts = []
        self.legislation_metadata = []
        
        # Extract all sections
        for cap_key, ordinance in ordinances_dict.items():
            chapter = ordinance.get('chapter', '')
            ordinance_title = ordinance.get('title', '')
            category = ordinance.get('category', 'Other')
            
            for section_num, section_data in ordinance.get('sections', {}).items():
                # Use embedding_text field created during preprocessing
                embedding_text = section_data.get('embedding_text', '')
                
                if embedding_text:
                    self.legislation_texts.append(embedding_text)
                    self.legislation_metadata.append({
                        'cap_key': cap_key,
                        'chapter': chapter,
                        'section': section_num,
                        'title': section_data.get('title', ''),
                        'text': section_data.get('text', ''),
                        'ordinance_title': ordinance_title,
                        'category': category,
                        'penalty': section_data.get('penalty', ''),
                        'type': 'legislation'
                    })
        
        print(f"   Found {len(self.legislation_texts)} sections to index")
        
        # Create semantic embeddings
        print("   Generating semantic embeddings...")
        self.legislation_embeddings = self.embedding_model.encode(
            self.legislation_texts,
            show_progress_bar=True,
            batch_size=32,
            convert_to_numpy=True
        )
        
        # Create TF-IDF vectors
        print("   Generating TF-IDF vectors...")
        self.legislation_tfidf = self.tfidf_vectorizer.fit_transform(self.legislation_texts)
        
        print(f"✅ Indexed {len(self.legislation_texts)} legislation sections")
        self.is_indexed = True
    
    def index_cases(self, cases_list):
        """
        Index all case law
        
        Args:
            cases_list: List of case objects from case_database
        """
        print("Indexing case law...")
        
        self.case_texts = []
        self.case_metadata = []
        
        for case in cases_list:
            # Combine case information for embedding
            case_text = (
                f"Case: {case.case_name} ({case.year}). "
                f"Facts: {case.facts} "
                f"Legal Principles: {' '.join(case.legal_principles)} "
                f"Keywords: {' '.join(case.keywords)}"
            )
            
            self.case_texts.append(case_text)
            self.case_metadata.append({
                'case_id': case.case_id,
                'case_name': case.case_name,
                'year': case.year,
                'court': case.court,
                'facts': case.facts,
                'charges': case.charges,
                'outcome': case.outcome,
                'sentence': case.sentence,
                'legal_principles': case.legal_principles,
                'keywords': case.keywords,
                'type': 'case'
            })
        
        print(f"   Found {len(self.case_texts)} cases to index")
        
        if self.case_texts:
            # Create semantic embeddings
            print("   Generating semantic embeddings...")
            self.case_embeddings = self.embedding_model.encode(
                self.case_texts,
                show_progress_bar=True,
                batch_size=32,
                convert_to_numpy=True
            )
            
            # Create TF-IDF vectors
            print("   Generating TF-IDF vectors...")
            self.case_tfidf = self.tfidf_vectorizer.transform(self.case_texts)
            
            print(f"✅ Indexed {len(self.case_texts)} cases")
    
    def search(self, query, top_k=10, source='both'):
        """
        Hybrid search across legislation and/or cases
        
        Args:
            query: Search query text
            top_k: Number of results to return
            source: 'legislation', 'cases', or 'both'
        
        Returns:
            list: Top-k results with scores and metadata
        """
        if not self.is_indexed:
            raise ValueError("Must index legislation before searching")
        
        results = []
        
        if source in ['legislation', 'both'] and self.legislation_embeddings is not None:
            leg_results = self._search_legislation(query, top_k)
            results.extend(leg_results)
        
        if source in ['cases', 'both'] and self.case_embeddings is not None:
            case_results = self._search_cases(query, top_k)
            results.extend(case_results)
        
        # Sort by hybrid score and return top-k
        results.sort(key=lambda x: x['hybrid_score'], reverse=True)
        return results[:top_k]
    
    def _search_legislation(self, query, top_k):
        """Search legislation sections"""
        # Get query embeddings
        query_embedding = self.embedding_model.encode([query], convert_to_numpy=True)
        query_tfidf = self.tfidf_vectorizer.transform([query])
        
        # Compute semantic similarity
        semantic_scores = cosine_similarity(query_embedding, self.legislation_embeddings)[0]
        
        # Compute TF-IDF similarity
        tfidf_scores = cosine_similarity(query_tfidf, self.legislation_tfidf)[0]
        
        # Compute hybrid scores
        hybrid_scores = (
            self.semantic_weight * semantic_scores + 
            self.tfidf_weight * tfidf_scores
        )
        
        # Get top results
        top_indices = np.argsort(hybrid_scores)[::-1][:top_k * 2]  # Get more for filtering
        
        results = []
        for idx in top_indices:
            if hybrid_scores[idx] > 0.1:  # Minimum threshold
                results.append({
                    'metadata': self.legislation_metadata[idx],
                    'text': self.legislation_texts[idx],
                    'semantic_score': float(semantic_scores[idx]),
                    'tfidf_score': float(tfidf_scores[idx]),
                    'hybrid_score': float(hybrid_scores[idx])
                })
        
        return results
    
    def _search_cases(self, query, top_k):
        """Search case law"""
        if self.case_embeddings is None or len(self.case_embeddings) == 0:
            return []
        
        # Get query embeddings
        query_embedding = self.embedding_model.encode([query], convert_to_numpy=True)
        query_tfidf = self.tfidf_vectorizer.transform([query])
        
        # Compute semantic similarity
        semantic_scores = cosine_similarity(query_embedding, self.case_embeddings)[0]
        
        # Compute TF-IDF similarity
        tfidf_scores = cosine_similarity(query_tfidf, self.case_tfidf)[0]
        
        # Compute hybrid scores
        hybrid_scores = (
            self.semantic_weight * semantic_scores + 
            self.tfidf_weight * tfidf_scores
        )
        
        # Get top results
        top_indices = np.argsort(hybrid_scores)[::-1][:top_k]
        
        results = []
        for idx in top_indices:
            if hybrid_scores[idx] > 0.1:  # Minimum threshold
                results.append({
                    'metadata': self.case_metadata[idx],
                    'text': self.case_texts[idx],
                    'semantic_score': float(semantic_scores[idx]),
                    'tfidf_score': float(tfidf_scores[idx]),
                    'hybrid_score': float(hybrid_scores[idx])
                })
        
        return results
    
    def search_legislation_only(self, query, top_k=10):
        """Search only legislation"""
        return self.search(query, top_k, source='legislation')
    
    def search_cases_only(self, query, top_k=5):
        """Search only cases"""
        return self.search(query, top_k, source='cases')
    
    def save_index(self, cache_dir):
        """
        Save indexed data to disk
        
        Args:
            cache_dir: Directory to save cache files
        """
        cache_path = Path(cache_dir)
        cache_path.mkdir(parents=True, exist_ok=True)
        
        print(f"Saving index to {cache_dir}...")
        
        # Save legislation data
        if self.legislation_embeddings is not None:
            np.save(cache_path / 'legislation_embeddings.npy', self.legislation_embeddings)
            with open(cache_path / 'legislation_metadata.pkl', 'wb') as f:
                pickle.dump({
                    'texts': self.legislation_texts,
                    'metadata': self.legislation_metadata
                }, f)
        
        # Save case data
        if self.case_embeddings is not None:
            np.save(cache_path / 'case_embeddings.npy', self.case_embeddings)
            with open(cache_path / 'case_metadata.pkl', 'wb') as f:
                pickle.dump({
                    'texts': self.case_texts,
                    'metadata': self.case_metadata
                }, f)
        
        # Save TF-IDF vectorizer
        with open(cache_path / 'tfidf_vectorizer.pkl', 'wb') as f:
            pickle.dump(self.tfidf_vectorizer, f)
        
        print("✅ Index saved successfully")
    
    def load_index(self, cache_dir):
        """
        Load indexed data from disk
        
        Args:
            cache_dir: Directory containing cache files
        
        Returns:
            bool: True if loaded successfully
        """
        cache_path = Path(cache_dir)
        
        if not cache_path.exists():
            return False
        
        print(f"Loading index from {cache_dir}...")
        
        try:
            # Load legislation data
            leg_embeddings_path = cache_path / 'legislation_embeddings.npy'
            leg_metadata_path = cache_path / 'legislation_metadata.pkl'
            
            if leg_embeddings_path.exists() and leg_metadata_path.exists():
                self.legislation_embeddings = np.load(leg_embeddings_path)
                with open(leg_metadata_path, 'rb') as f:
                    leg_data = pickle.load(f)
                    self.legislation_texts = leg_data['texts']
                    self.legislation_metadata = leg_data['metadata']
                print(f"   Loaded {len(self.legislation_texts)} legislation sections")
            
            # Load case data
            case_embeddings_path = cache_path / 'case_embeddings.npy'
            case_metadata_path = cache_path / 'case_metadata.pkl'
            
            if case_embeddings_path.exists() and case_metadata_path.exists():
                self.case_embeddings = np.load(case_embeddings_path)
                with open(case_metadata_path, 'rb') as f:
                    case_data = pickle.load(f)
                    self.case_texts = case_data['texts']
                    self.case_metadata = case_data['metadata']
                print(f"   Loaded {len(self.case_texts)} cases")
            
            # Load TF-IDF vectorizer
            tfidf_path = cache_path / 'tfidf_vectorizer.pkl'
            if tfidf_path.exists():
                with open(tfidf_path, 'rb') as f:
                    self.tfidf_vectorizer = pickle.load(f)
            
            # Regenerate TF-IDF matrices
            if self.legislation_texts:
                self.legislation_tfidf = self.tfidf_vectorizer.transform(self.legislation_texts)
            if self.case_texts:
                self.case_tfidf = self.tfidf_vectorizer.transform(self.case_texts)
            
            self.is_indexed = True
            print("✅ Index loaded successfully")
            return True
            
        except Exception as e:
            print(f"⚠️  Error loading index: {e}")
            return False

if __name__ == '__main__':
    print("=" * 80)
    print("Testing Hybrid Search Engine")
    print("=" * 80)
    print()
    
    # This is a basic test - full testing will be done in embeddings_index.py
    print("To fully test the hybrid search engine:")
    print("1. Run preprocess_legislation.py to create JSON database")
    print("2. Run embeddings_index.py to create and test the full index")
    print()

