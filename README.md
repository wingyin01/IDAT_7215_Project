# Hong Kong Legal Expert System with RAG

An intelligent legal consultation system powered by Retrieval-Augmented Generation (RAG), combining Hong Kong legislation, case law, and LLaMA AI for expert legal guidance.

## 🌟 Features

### Dual Consultation Modes

1. **Rule-Based Analysis** 
   - Fast fact-based analysis using forward chaining inference
   - Identifies criminal offences and potential defenses
   - Based on predefined legal rules

2. **Expert Mode (RAG)** 🚀
   - AI-powered consultation using LLaMA
   - Semantic search across 52,269 legislation sections
   - Hybrid scoring (semantic embeddings + TF-IDF)
   - Citations from actual legislation and case law
   - Natural language question answering

### Knowledge Base

- **Legislation**: 2,234 Hong Kong ordinances with 52,269 sections
- **Case Law**: 29 real criminal appeal cases (Court of Appeal, 2018-2025)
- **Categories**: Criminal Law, Commercial Law, Employment Law, Property & Land, and more

### ⚖️ Copyright & Data Sources

**Legislation**: From official HK e-Legislation portal (https://www.elegislation.gov.hk)
- XML files processed into JSON for performance
- All data from official Hong Kong Government sources

**Case Law**: From official HK Judiciary database (https://legalref.judiciary.hk)
- 29 real criminal appeal cases manually downloaded
- Used for educational/research purposes under fair use
- Processed into structured format for case matching algorithms
- **Note**: Cases are criminal law only; system focuses on this area

## 🚀 Quick Start

### Prerequisites

- Python 3.9+
- 8GB RAM minimum (for LLaMA models)
- macOS or Linux

### Installation

1. **Clone the repository:**
```bash
git clone https://github.com/yourusername/IDAT_7215_Project.git
cd IDAT_7215_Project
```

2. **Setup Python environment:**
```bash
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
```

3. **⚠️ REQUIRED: Preprocess data (one-time, ~5-10 minutes):**
```bash
./scripts/preprocess_data.sh
```

**This step is mandatory!** It will:
- Convert 3,085 XML legislation files to fast-loading JSON (~2-3 mins)
- Generate embeddings for 52,269 legislation sections (~3-5 mins)
- Generate embeddings for 29 real criminal cases (~1 min)
- Create search indices (~200MB cache)

**Note**: The generated files are too large for GitHub and must be built locally.

3. **Setup RAG (one-time, ~10-15 minutes):**
```bash
./scripts/setup_rag.sh
```

This installs Ollama and downloads the LLaMA model (choose 3B for testing or 8B for best quality).

4. **Run the application:**
```bash
./scripts/run.sh
```

Visit http://localhost:8080

## 💻 CLI Usage

New! Use the system directly from command line without starting the web server:

### Show System Statistics
```bash
python query.py
```

### Quick Legal Query (RAG Mode)
```bash
python query.py "What are the penalties for theft?"
```

### Rule-Based Analysis
```bash
python query.py --mode rule "Person stole property worth HK$5000"
```

### Search Case Law
```bash
python query.py --mode cases "theft from store" --top-k 5
```

### Available Modes
- `rag` (default) - AI-powered consultation using LLaMA
- `rule` - Traditional rule-based analysis
- `cases` - Search case law precedents
- `stats` - Display system statistics

## 📋 System Architecture

```
User Query
    ↓
[Hybrid Search Engine]
    ├─ Semantic Embeddings (sentence-transformers)
    ├─ TF-IDF Vectors
    └─ Hybrid Scoring (0.7 × semantic + 0.3 × tfidf)
    ↓
[Retrieved Context]
    ├─ Top-10 Legislation Sections
    └─ Top-5 Case Precedents
    ↓
[LLaMA Model]
    ├─ Context: Retrieved sources
    ├─ Prompt: Legal consultation template
    └─ Generation: Expert advice
    ↓
[Response]
    ├─ Legal Advice
    ├─ Source Citations
    └─ Disclaimer
```

For detailed architecture documentation, see [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)

## 🛠️ Technical Stack

### Backend
- **Flask**: Web framework
- **sentence-transformers**: Semantic embeddings (all-MiniLM-L6-v2)
- **scikit-learn**: TF-IDF vectorization
- **Ollama**: LLaMA model inference
- **NLTK**: Natural language processing

### AI Models
- **Embeddings**: all-MiniLM-L6-v2 (~80MB)
- **LLM**: LLaMA 3.1 8B or LLaMA 3.2 3B

### Data Processing
- **JSON Database**: Fast loading (2-5s) vs XML parsing (30-60s)
- **Embeddings Cache**: Pre-computed vectors (~200MB)
- **XML Parser**: One-time preprocessing from official HK e-Legislation

## 📁 Project Structure

```
IDAT_7215_Project/
├── README.md                    # This file
├── requirements.txt             # Python dependencies
├── query.py                     # CLI interface
│
├── docs/                        # Documentation
│   ├── ARCHITECTURE.md          # Detailed system design
│   └── DEPLOYMENT.md            # Deployment guide
│
├── scripts/                     # Setup scripts
│   ├── preprocess_data.sh       # Data preprocessing
│   ├── setup_rag.sh             # RAG setup
│   └── run.sh                   # Application launcher
│
├── tests/                       # Test files
│   ├── test_system.py           # System tests
│   └── test_json_loader.py      # Loader tests
│
├── engine/                      # Processing engines
│   ├── rag_engine.py            # RAG consultation pipeline
│   ├── hybrid_search.py         # Semantic + TF-IDF search
│   ├── rule_engine.py           # Rule-based inference
│   ├── case_matcher.py          # Case law matching
│   └── document_analyzer.py     # Document analysis
│
├── knowledge_base/              # Knowledge base
│   ├── json_loader.py           # Fast JSON loader
│   ├── preprocess_legislation.py # XML → JSON converter
│   ├── embeddings_index.py      # Embedding generator
│   ├── all_cases_database.py    # Case database
│   └── all_legal_rules.py       # Legal rules
│
├── webapp/                      # Web application
│   ├── app.py                   # Flask application
│   ├── templates/               # HTML templates
│   └── static/                  # CSS, JS, images
│
├── Legislation/                 # Raw XML files (3,085 files)
└── venv/                        # Virtual environment
```

## 🔧 API Endpoints

### RAG Consultation
```
POST /api/rag-consultation
Body: {"query": "What are the penalties for theft?", "stream": false}
Response: {
  "success": true,
  "advice": "...",
  "legislation_count": 10,
  "cases_count": 5,
  "citations": {...}
}
```

### RAG Status
```
GET /api/rag-status
Response: {
  "available": true,
  "ollama_installed": true,
  "indexed": true
}
```

### Rule-Based Analysis
```
POST /api/analyze
Body: {"facts": ["appropriates_property", "property_belongs_to_another", ...]}
```

### Case Search
```
POST /api/search-cases
Body: {"query": "theft", "top_n": 5}
```

For complete API documentation, see [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)

## 📊 Performance

### Loading Times
- **JSON Loading**: 2-5 seconds (optimized!) ⚡
- **Embeddings Loading**: <1 second (from cache)
- **RAG Query Response**: 3-8 seconds
- **Rule-Based Analysis**: <0.1 seconds

### Resource Usage
- **JSON Database**: ~50-100MB
- **Embeddings Cache**: ~200MB
- **LLaMA 3.2 3B**: ~2GB RAM
- **LLaMA 3.1 8B**: ~4.7GB RAM

## 🧪 Testing

### Test Preprocessing
```bash
python3 -m knowledge_base.preprocess_legislation
```

### Test Embeddings
```bash
python3 -m knowledge_base.embeddings_index
```

### Test RAG Engine
```bash
python3 -m engine.rag_engine
```

### Test Full System
```bash
python tests/test_system.py
```

## 📖 Usage Examples

### Expert Mode (RAG)

**Question**: "What are the legal requirements for starting a company in Hong Kong?"

**Response**: 
- Analyzes Cap. 622 (Companies Ordinance)
- Retrieves relevant sections about company registration
- Cites case precedents about company formation
- Provides step-by-step guidance with legal citations

### Rule-Based Mode

**Input Facts**: 
- Person entered store
- Took items worth HK$5,000
- Left without paying
- Had intent to permanently deprive

**Output**:
- Identifies: Theft (Cap. 210, s.2)
- Maximum Penalty: 10 years imprisonment
- Detailed reasoning chain

### CLI Examples

```bash
# Quick consultation
python query.py "Can I sue my employer for wrongful termination?"

# Analyze a scenario
python query.py --mode rule "Person assaulted another causing bodily harm"

# Find similar cases
python query.py --mode cases "employment discrimination" --top-k 3
```

## ⚠️ Important Notes

### Legal Disclaimer
This system provides general legal information, NOT legal advice. For specific legal matters, consult a qualified Hong Kong solicitor.

### Data Currency
Legislation data is from the official HK e-Legislation portal (last updated: 2024-2025). Laws may have changed since the data was collected.

### System Limitations
- RAG responses depend on LLaMA model quality
- Semantic search may miss edge cases
- Case database is limited (9 cases currently)
- Not a substitute for professional legal counsel

## 🔄 Maintenance

### Update Legislation Data
1. Download new XML files from https://www.elegislation.gov.hk
2. Place in `Legislation/` directory
3. Run: `./scripts/preprocess_data.sh`

### Rebuild Embeddings
```bash
python3 -m knowledge_base.embeddings_index --rebuild
```

### Update LLaMA Model
```bash
ollama pull llama3.1:8b  # or llama3.2:3b
```

## 🤝 Contributing

### Adding New Cases
Edit `knowledge_base/all_cases_database.py` and add cases using the `CriminalCase` class.

### Adding New Rules
Edit `knowledge_base/all_legal_rules.py` and add rules using the `Rule` class.

### Improving Categorization
Update categories in `knowledge_base/preprocess_legislation.py`.

## 🆘 Troubleshooting

### "RAG engine not available"
- Ensure Ollama is running: `ollama serve`
- Check embeddings exist: `ls knowledge_base/cached_embeddings/`
- Run: `./scripts/setup_rag.sh`

### "Port 8080 already in use"
- The system will automatically kill the old process
- Or manually: `lsof -ti:8080 | xargs kill -9`

### Slow loading times
- Ensure JSON database exists: `ls knowledge_base/legislation_database.json`
- If missing, run: `./scripts/preprocess_data.sh`
- System should load in 2-5 seconds (not 30-60 seconds)

### Out of memory
- Use smaller model: `ollama pull llama3.2:3b`
- Reduce `top_k_legislation` in RAG engine configuration

## 📧 Support

For issues or questions:
1. Check the troubleshooting section above
2. Review [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) for technical details
3. Review [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md) for deployment options
4. Check system logs in terminal

## 🎓 Academic Context

This is a course project for IDAT 7215 - Expert Systems, demonstrating:
- Knowledge representation (rules, cases, legislation)
- Inference engines (forward chaining)
- Modern AI integration (RAG with LLaMA)
- Hybrid retrieval methods (semantic + keyword)
- Real-world application (Hong Kong legal system)

## 📝 License

This project is for educational purposes (IDAT 7215). The legislation data is from official Hong Kong Government sources.

---

**Built with ❤️ for Hong Kong Legal Education**

## 🚀 Quick Command Reference

```bash
# Initial Setup
./scripts/preprocess_data.sh      # Convert XML to JSON (one-time)
./scripts/setup_rag.sh             # Install Ollama + LLaMA (one-time)

# Run Application
./scripts/run.sh                   # Start web server
python query.py                    # CLI interface

# Testing
python tests/test_system.py        # Run tests

# Maintenance
python3 -m knowledge_base.embeddings_index --rebuild  # Rebuild embeddings
```
