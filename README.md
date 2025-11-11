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
- **Case Law**: 9 case precedents with full analysis
- **Categories**: Criminal Law, Commercial Law, Employment Law, Property & Land, and more

## 🚀 Quick Start

### Prerequisites

- Python 3.9+
- 8GB RAM minimum (for LLaMA models)
- macOS or Linux

### Installation

1. **Clone and setup:**
```bash
cd IDAT_7215_Project
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
```

2. **Preprocess data (one-time, ~2-3 minutes):**
```bash
./preprocess_data.sh
```

This converts XML legislation to JSON and generates embeddings cache.

3. **Setup RAG (one-time, ~10-15 minutes):**
```bash
./setup_rag.sh
```

This installs Ollama and downloads the LLaMA model (choose 3B for testing or 8B for best quality).

4. **Run the application:**
```bash
./run.sh
```

Visit http://localhost:8080

## 📋 System Architecture

```
User Query
    ↓
[Hybrid Search Engine]
    ├─ Semantic Embeddings (sentence-transformers)
    ├─ TF-IDF Vectors
    └─ Hybrid Scoring (0.7 * semantic + 0.3 * tfidf)
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
- **XML Parser**: Extracts legislation from official HK e-Legislation portal
- **JSON Loader**: Fast loading (2-5s vs 30-60s for XML)
- **Embeddings Cache**: Pre-computed vectors (~200MB)

## 📁 Project Structure

```
IDAT_7215_Project/
├── engine/
│   ├── rule_engine.py          # Rule-based inference engine
│   ├── hybrid_search.py        # Semantic + TF-IDF search
│   ├── rag_engine.py           # RAG consultation pipeline
│   ├── case_matcher.py         # Case law matching
│   └── document_analyzer.py    # Document analysis
├── knowledge_base/
│   ├── preprocess_legislation.py   # XML → JSON converter
│   ├── json_loader.py              # Fast JSON loader
│   ├── embeddings_index.py         # Embedding generator
│   ├── legislation_database.json   # Processed knowledge base
│   ├── cached_embeddings/          # Pre-computed vectors
│   ├── hk_all_ordinances.py        # Ordinance loader
│   └── all_cases_database.py       # Case database
├── webapp/
│   ├── app.py                      # Flask application
│   ├── templates/                  # HTML templates
│   └── static/                     # CSS, JS, images
├── Legislation/                    # Raw XML files (3,085 files)
├── requirements.txt                # Python dependencies
├── preprocess_data.sh              # Data preprocessing script
├── setup_rag.sh                    # RAG setup script
└── run.sh                          # Application launcher
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

## 📊 Performance

### Loading Times
- **XML Parsing**: 30-60 seconds
- **JSON Loading**: 2-5 seconds (94% faster!)
- **Embeddings Loading**: <1 second (from cache)
- **RAG Query Response**: 3-8 seconds

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
python3 final_system_test.py
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
3. Run: `./preprocess_data.sh`

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
Update categories in `knowledge_base/all_ordinances_loader.py`.

## 📝 License

This project is for educational purposes (IDAT 7215). The legislation data is from official Hong Kong Government sources.

## 🆘 Troubleshooting

### "RAG engine not available"
- Ensure Ollama is running: `ollama serve`
- Check embeddings exist: `ls knowledge_base/cached_embeddings/`
- Run: `./setup_rag.sh`

### "Port 8080 already in use"
- The system will automatically kill the old process
- Or manually: `lsof -ti:8080 | xargs kill -9`

### Slow loading times
- Ensure JSON database exists: `ls knowledge_base/legislation_database.json`
- Rebuild if needed: `./preprocess_data.sh`

### Out of memory
- Use smaller model: `ollama pull llama3.2:3b`
- Reduce `top_k_legislation` in RAG engine

## 📧 Support

For issues or questions:
1. Check the troubleshooting section
2. Review system logs in terminal
3. Ensure all prerequisites are installed

## 🎓 Academic Context

This is a course project for IDAT 7215 - Expert Systems, demonstrating:
- Knowledge representation (rules, cases, legislation)
- Inference engines (forward chaining)
- Modern AI integration (RAG with LLaMA)
- Hybrid retrieval methods (semantic + keyword)
- Real-world application (Hong Kong legal system)

---

**Built with ❤️ for Hong Kong Legal Education**
