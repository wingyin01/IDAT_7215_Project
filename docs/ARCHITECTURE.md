# System Architecture

## Overview

The Hong Kong Legal Expert System is a three-layer architecture combining traditional expert system techniques with modern RAG (Retrieval-Augmented Generation) AI technology.

```
┌─────────────────────────────────────────────────────────┐
│                    Web Layer (Flask)                     │
│  - REST API endpoints                                    │
│  - HTML templates                                        │
│  - Session management                                    │
└─────────────────┬───────────────────────────────────────┘
                  │
┌─────────────────▼───────────────────────────────────────┐
│                    Engine Layer                          │
│  - RAG Engine (Retrieval + LLaMA)                       │
│  - Hybrid Search (Semantic + TF-IDF)                    │
│  - Rule Engine (Forward Chaining)                       │
│  - Case Matcher (Similarity Search)                     │
│  - Document Analyzer (NLP)                              │
└─────────────────┬───────────────────────────────────────┘
                  │
┌─────────────────▼───────────────────────────────────────┐
│                    Data Layer                            │
│  - JSON Legislation Database (52K+ sections)            │
│  - Embeddings Cache (Pre-computed vectors)              │
│  - Case Law Database (9 precedents)                     │
│  - Legal Rules (Forward chaining rules)                 │
└─────────────────────────────────────────────────────────┘
```

## Layer 1: Data Layer

### Legislation Database

**Format: JSON**
- **Why JSON?** Fast loading (2-5s) vs XML parsing (30-60s)
- **Source:** Official Hong Kong e-Legislation XML files
- **Processing:** One-time conversion via `preprocess_legislation.py`
- **Structure:**
  ```python
  {
    "ordinances": {
      "cap_210": {
        "chapter": "210",
        "title": "Theft Ordinance",
        "category": "Criminal Law",
        "sections": {
          "2": {
            "title": "Basic definition of theft",
            "text": "...",
            "penalty": "...",
            "embedding_text": "..."  # Optimized for semantic search
          }
        }
      }
    }
  }
  ```

**Key Files:**
- `knowledge_base/legislation_database.json` - Compiled legislation (generated)
- `knowledge_base/json_loader.py` - Fast JSON loader
- `knowledge_base/preprocess_legislation.py` - XML → JSON converter
- `knowledge_base/xml_parser.py` - XML parsing utilities (used during preprocessing)

### Embeddings Cache

**Purpose:** Pre-computed semantic vectors for fast retrieval

**Components:**
- `legislation_embeddings.npy` - 52,269 section embeddings (384-dim vectors)
- `case_embeddings.npy` - Case law embeddings
- `legislation_metadata.pkl` - Metadata for each section
- `tfidf_vectorizer.pkl` - TF-IDF model for keyword search

**Why Pre-compute?**
- Computing embeddings on-the-fly would take ~5 minutes per query
- Cache allows instant retrieval (<1 second)
- Generated once via `embeddings_index.py`

**Key Files:**
- `knowledge_base/embeddings_index.py` - Builds and caches embeddings
- `knowledge_base/cached_embeddings/` - Stored vectors (generated, git-ignored)

### Case Law Database

**Format:** Python objects defined in code

**Structure:**
```python
class CriminalCase:
    case_id: str
    case_name: str
    year: int
    court: str
    facts: str
    charges: List[str]
    outcome: str
    sentence: str
    legal_principles: List[str]
    keywords: List[str]
```

**Key Files:**
- `knowledge_base/all_cases_database.py` - 9 case precedents

### Legal Rules

**Format:** Forward chaining rules for inference

**Structure:**
```python
Rule(
    name="theft",
    conditions=["appropriates_property", "property_belongs_to_another", ...],
    conclusion="offence_theft",
    ordinance_ref="Cap. 210, s.2",
    penalty="10 years imprisonment"
)
```

**Key Files:**
- `knowledge_base/all_legal_rules.py` - Criminal law rules
- `knowledge_base/defenses.py` - Legal defenses

## Layer 2: Engine Layer

### RAG Engine (`engine/rag_engine.py`)

**Purpose:** Intelligent legal consultation using AI

**Workflow:**
```
User Query
    ↓
[1. Hybrid Search]
    ├─ Semantic: Query → Embedding → Vector similarity
    └─ TF-IDF: Query → Keywords → Lexical matching
    ↓
[2. Retrieve Top-K]
    ├─ Top 10 legislation sections
    └─ Top 5 case precedents
    ↓
[3. Build Context]
    - Format sources into structured prompt
    ↓
[4. LLaMA Generation]
    - Model: llama3.1:8b or llama3.2:3b
    - Provider: Ollama (local inference)
    ↓
Legal Advice + Citations
```

**Key Components:**
- `retrieve_context()` - Finds relevant sources
- `build_context()` - Formats for LLM
- `generate_advice()` - Calls Ollama API
- `consult()` - Full pipeline

### Hybrid Search (`engine/hybrid_search.py`)

**Purpose:** Combine semantic understanding with keyword matching

**Algorithm:**
```
final_score = 0.7 × semantic_score + 0.3 × tfidf_score
```

**Why Hybrid?**
- Semantic embeddings capture meaning but may miss specific terms
- TF-IDF ensures exact keyword matches are prioritized
- Combination provides best of both worlds

**Technical Details:**
- **Semantic Model:** sentence-transformers/all-MiniLM-L6-v2 (80MB)
  - 384-dimensional embeddings
  - Cosine similarity for matching
- **TF-IDF:** scikit-learn vectorizer
  - 1,000 max features
  - 1-2 gram n-grams
  - English stop words removed

### Rule Engine (`engine/rule_engine.py`)

**Purpose:** Traditional expert system inference

**Algorithm:** Forward chaining
```
Given: Set of facts
Repeat:
  1. Find rules where all conditions match known facts
  2. Apply rule → Add conclusion to facts
  3. Continue until no more rules apply
```

**Use Cases:**
- Fast fact-based analysis
- Deterministic outcomes
- No AI required

**Key Components:**
- `InferenceEngine` class
- `analyze_case()` function
- Rule matching and firing

### Case Matcher (`engine/case_matcher.py`)

**Purpose:** Find similar legal precedents

**Algorithm:**
- TF-IDF vectorization of case facts
- Cosine similarity ranking
- Returns top-N most similar cases

### Document Analyzer (`engine/document_analyzer.py`)

**Purpose:** Extract legal facts from natural language

**Features:**
- Entity extraction (parties, dates, amounts, locations)
- Keyword-based fact identification
- Legal issue identification
- Integration with rule engine

## Layer 3: Web Layer

### Flask Application (`webapp/app.py`)

**REST API Endpoints:**

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/rag-consultation` | POST | RAG-powered legal consultation |
| `/api/rag-status` | GET | Check RAG availability |
| `/api/analyze` | POST | Rule-based analysis |
| `/api/search-cases` | POST | Search case law |
| `/api/analyze-document` | POST | Document analysis |
| `/api/ordinances` | GET | List ordinances |
| `/api/ordinance/<chapter>/<section>` | GET | Get specific section |
| `/api/stats` | GET | System statistics |

**Web Pages:**
- `/` - Home page
- `/consultation` - Expert consultation interface
- `/case-search` - Case law search
- `/document-analysis` - Document analyzer

## Data Flow Examples

### Example 1: RAG Consultation

```
User: "What are penalties for theft in Hong Kong?"
    ↓
1. Hybrid Search Engine
   - Semantic: Embeds query → Searches 52K sections
   - TF-IDF: Extracts "penalties" + "theft"
   - Combines scores → Top 10 sections
   - Also retrieves: Top 5 similar cases
    ↓
2. Retrieved Context
   - Cap. 210, s.2: Basic definition of theft
   - Cap. 210, s.9: Theft → 10 years imprisonment
   - HKSAR v. Chan (2019): Theft case precedent
    ↓
3. LLaMA Prompt
   [Context: Retrieved legislation + cases]
   User Question: What are penalties for theft?
   Instructions: Provide professional legal advice...
    ↓
4. LLaMA Response
   "In Hong Kong, theft is defined under Cap. 210, s.2...
    The penalty is imprisonment for up to 10 years...
    [Citations and disclaimer]"
```

### Example 2: Rule-Based Analysis

```
User Facts: 
  - Person took property
  - Property belonged to someone else
  - Acted dishonestly
  - Intended to permanently deprive owner
    ↓
1. Inference Engine
   - Loads rules from all_legal_rules.py
   - Matches facts against rule conditions
   - Finds: THEFT rule matches all conditions
   - Fires rule → Concludes: theft offense
    ↓
2. Output
   - Offense: Theft (Cap. 210, s.2)
   - Penalty: 10 years imprisonment
   - Reasoning chain shown
```

## Performance Characteristics

### Loading Times

| Component | Time | Notes |
|-----------|------|-------|
| XML Parsing | 30-60s | OLD - No longer used |
| JSON Loading | 2-5s | ✅ Current method |
| Embeddings Load | <1s | From cache |
| RAG Query | 3-8s | Includes LLM inference |
| Rule Analysis | <0.1s | Deterministic |

### Resource Usage

| Component | Size/RAM |
|-----------|----------|
| JSON Database | ~50-100 MB |
| Embeddings Cache | ~200 MB |
| Legislation Embeddings | 384-dim × 52K = ~80 MB |
| sentence-transformers Model | ~80 MB |
| LLaMA 3.2 3B | ~2 GB RAM |
| LLaMA 3.1 8B | ~4.7 GB RAM |

## Design Decisions

### Why JSON instead of XML?

**Problem:** XML parsing was taking 30-60 seconds on startup

**Solution:** One-time preprocessing to JSON

**Benefits:**
- 10-20x faster loading
- Smaller file size (structured format)
- Easier to work with in Python
- Pre-computed embedding_text fields

**Trade-off:** Must regenerate JSON when legislation updates (infrequent)

### Why Hybrid Search?

**Problem:** Pure semantic search missed exact legal terms

**Solution:** Combine semantic + TF-IDF with 70/30 weighting

**Benefits:**
- Semantic: Understands "What are my tenant rights?" → landlord/tenant law
- TF-IDF: Ensures "theft" queries prioritize Cap. 210
- Weighted combination balances both

### Why Local LLM (Ollama)?

**Benefits:**
- No API costs
- Data privacy (sensitive legal queries)
- No internet required
- Full control over model

**Trade-offs:**
- Requires GPU/significant RAM
- Slower than cloud APIs
- Manual model management

**Alternative:** Code can be modified to use OpenAI/Anthropic APIs (see `DEPLOYMENT.md`)

### Why Pre-compute Embeddings?

**Problem:** Computing 52K embeddings takes ~5-10 minutes

**Solution:** Generate once, cache to disk

**Benefits:**
- Query-time speed: instant retrieval
- Embeddings rarely change (legislation updates infrequent)

**Process:**
```bash
# One-time setup (takes 5-10 minutes)
./scripts/preprocess_data.sh

# Queries are instant after this
python query.py "legal question"
```

## Extensibility

### Adding New Legislation

1. Place new XML files in `Legislation/` folders
2. Run: `./scripts/preprocess_data.sh`
3. Rebuilds JSON database and embeddings

### Adding New Cases

Edit `knowledge_base/all_cases_database.py`:
```python
CriminalCase(
    case_id="new_case",
    case_name="...",
    # ... fill in details
)
```

### Adding New Rules

Edit `knowledge_base/all_legal_rules.py`:
```python
Rule(
    name="new_offense",
    conditions=["fact1", "fact2"],
    conclusion="offense_name",
    ordinance_ref="Cap. X, s.Y",
    penalty="..."
)
```

### Using Different LLM

Modify `engine/rag_engine.py`:
```python
# Replace Ollama calls with:
import openai
response = openai.chat.completions.create(...)
```

## CLI Interface

New in this version: `query.py` provides direct Python access without web server

**Usage:**
```bash
# Show system stats
python query.py

# RAG consultation
python query.py "What are penalties for theft?"

# Rule-based analysis
python query.py --mode rule "Person stole property"

# Case search
python query.py --mode cases "theft from store"
```

## Testing

See `tests/` folder for:
- `test_system.py` - Comprehensive system tests
- `test_json_loader.py` - JSON loader validation

Run tests:
```bash
python tests/test_system.py
```

## Directory Structure

```
IDAT_7215_Project/
├── README.md                    # Main documentation
├── requirements.txt             # Python dependencies
├── query.py                     # CLI interface
│
├── docs/                        # Documentation
│   ├── ARCHITECTURE.md          # This file
│   └── DEPLOYMENT.md            # Deployment guide
│
├── scripts/                     # Setup scripts
│   ├── preprocess_data.sh       # XML → JSON conversion
│   ├── setup_rag.sh             # Install Ollama + LLaMA
│   └── run.sh                   # Start web server
│
├── tests/                       # Test files
│   ├── test_system.py           # System tests
│   └── test_json_loader.py      # Loader tests
│
├── engine/                      # Processing engines
│   ├── rag_engine.py            # RAG pipeline
│   ├── hybrid_search.py         # Hybrid search
│   ├── rule_engine.py           # Forward chaining
│   ├── case_matcher.py          # Case similarity
│   └── document_analyzer.py     # NLP extraction
│
├── knowledge_base/              # Data layer
│   ├── json_loader.py           # Fast JSON loader ✅
│   ├── preprocess_legislation.py # XML → JSON converter
│   ├── xml_parser.py            # XML parsing utilities
│   ├── embeddings_index.py      # Embedding generator
│   ├── all_cases_database.py    # Case precedents
│   ├── all_legal_rules.py       # Inference rules
│   ├── defenses.py              # Legal defenses
│   ├── legislation_database.json # Compiled data (generated)
│   └── cached_embeddings/       # Vector cache (generated)
│
├── webapp/                      # Web interface
│   ├── app.py                   # Flask application
│   ├── templates/               # HTML templates
│   └── static/                  # CSS, JS, images
│
├── Legislation/                 # Source XML files
│   ├── hkel_c_leg_cap_1_cap_300_en/
│   ├── hkel_c_leg_cap_301_cap_600_en/
│   └── hkel_c_leg_cap_601_cap_end_en/
│
└── venv/                        # Virtual environment
```

## Technology Stack

### Backend
- **Python 3.9+**
- **Flask** - Web framework
- **sentence-transformers** - Semantic embeddings
- **scikit-learn** - TF-IDF, ML utilities
- **NLTK** - Natural language processing
- **numpy** - Numerical operations

### AI/ML
- **Ollama** - Local LLM serving
- **LLaMA 3.1 8B** or **LLaMA 3.2 3B** - Language model
- **all-MiniLM-L6-v2** - Sentence embedding model

### Data Processing
- **JSON** - Primary data format
- **pickle** - Python object serialization
- **numpy** - Efficient array storage

## Future Enhancements

1. **Real-time legislation updates** - Monitor e-Legislation portal
2. **Expanded case database** - More precedents
3. **Multilingual support** - Chinese language support
4. **Advanced NER** - Better entity extraction
5. **Fine-tuned embeddings** - Domain-specific legal embeddings
6. **Vector database** - Replace numpy with Pinecone/Weaviate for scale
7. **API authentication** - Secure the REST API
8. **Containerization** - Docker deployment

