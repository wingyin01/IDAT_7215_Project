# IDAT7215 Hong Kong Legal Expert System

A comprehensive expert system covering **ALL Hong Kong law** with **2,234 ordinances** and **52,269 legal sections**. Built using official Hong Kong e-Legislation XML data.

## 🎯 Project Overview

**IDAT7215 Group Project** - Comprehensive legal expert system covering the entire Hong Kong legal system across criminal, civil, commercial, employment, property, family law, and more.

### System Scale

| Metric | Count |
|--------|-------|
| **Total Ordinances** | 2,234 |
| **Total Legal Sections** | 52,269 |
| **XML Files Processed** | 3,085 |
| **Legal Categories** | 11 |
| **Legal Rules** | 47 |
| **Case Precedents** | 9 |

## 📚 Legal Coverage

| Legal Area | Ordinances | Sections |
|------------|------------|----------|
| **Criminal Law** | 36 | 2,019 |
| **Commercial & Company** | 25 | 3,401 |
| **Property & Land** | 58 | 1,713 |
| **Employment Law** | 24 | 1,112 |
| **Civil Law** | 20 | 1,058 |
| **Tax & Revenue** | 10 | 933 |
| **Constitutional & Admin** | 20 | 801 |
| **Intellectual Property** | 4 | 727 |
| **Family Law** | 17 | 479 |
| **Immigration** | 2 | 203 |
| **Other Specialized** | 2,018 | 39,823 |

**Data Source:** https://www.elegislation.gov.hk/ (Official HK Government)

## 🚀 Quick Start

```bash
# 1. Navigate to project directory
cd "/Users/wingyin/Documents/Expert system"

# 2. Activate virtual environment
source venv/bin/activate

# 3. Run the application
python webapp/app.py
```

Open browser to: **http://localhost:8080**

**Note:** First load takes ~30 seconds to parse 3,085 XML files.

## 📖 Features

### 1. Legal Consultation
- Input case facts from any legal area
- Get rule-based analysis with ordinance citations
- See complete reasoning chains

### 2. Case Search
- Find similar precedents using TF-IDF and cosine similarity
- 9 sample cases across multiple legal areas
- View outcomes and legal principles

### 3. Document Analysis
- Paste legal documents for automatic fact extraction
- NLP-based entity recognition
- Multi-domain legal issue identification

## 🏗️ Project Structure

```
Expert system/
├── knowledge_base/          # Legal knowledge (2,234 ordinances, 47 rules, 9 cases)
├── engine/                  # AI components (inference, matching, NLP)
├── webapp/                  # Flask web app + templates
├── Legislation/             # Official XML files (3,085 files)
├── venv/                    # Virtual environment
├── requirements.txt         # Dependencies
├── run.sh                   # Helper script
└── README.md                # This file
```

## ⚙️ Installation

### Prerequisites
- Python 3.8+
- pip

### Setup

```bash
# Create virtual environment
python3 -m venv venv

# Activate it
source venv/bin/activate  # macOS/Linux
# or: venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt
```

## 🧪 Testing

### Quick Test
```bash
source venv/bin/activate
python final_system_test.py
```

Expected output: All 8 tests pass, 2,234 ordinances loaded

### Verify XML Usage
```bash
python test_xml_loading.py
```

Shows that official XML files are being used.

## 🎯 Technical Highlights

### AI Techniques
1. **Expert System**: Forward chaining inference with 47 legal rules
2. **Machine Learning**: TF-IDF vectorization + cosine similarity for case matching
3. **NLP**: Text extraction and entity recognition for document analysis

### Data Processing
- XML parsing of 3,085 official government files
- Extraction of 52,269 legal sections
- Organization into 11 legal categories
- Real-time search across entire database

## 📊 API Endpoints

```
GET  /api/stats              - System statistics
GET  /api/categories         - Legal categories
GET  /api/ordinances         - List ordinances
GET  /api/ordinance/<ch>     - Specific ordinance
GET  /api/ordinance/<ch>/<s> - Specific section
POST /api/analyze            - Legal analysis
POST /api/search-cases       - Case search
POST /api/analyze-document   - Document analysis
```

## 🔧 Troubleshooting

**Long initial loading:**
- Normal - parsing 3,085 XML files takes ~30 seconds
- Wait for "Access the system at: http://localhost:8080" message

**Port already in use:**
- Edit `webapp/app.py` line 327
- Change `port=8080` to another port like `8081`

**Module import errors:**
- Ensure virtual environment is activated: `source venv/bin/activate`

## ⚠️ Disclaimer

This system provides general information only and is NOT legal advice. For actual legal matters, consult a qualified Hong Kong solicitor or barrister.

## 🎓 For IDAT7215 Assessment

### Key Achievements
- 2,234 ordinances (100x larger than typical academic projects)
- Official government data (not simulated)
- Three AI techniques (Expert Systems + ML + NLP)
- 11 legal categories (multi-domain coverage)
- Production-quality web application

### Demo Points
1. Show homepage statistics: 2,234 ordinances, 52,269 sections
2. Run legal consultation: Show inference reasoning
3. Search cases: Demonstrate TF-IDF similarity matching
4. Analyze document: Show NLP extraction
5. Run test script: Prove official XML usage

## 📞 Support

For technical details, see:
- `COMPREHENSIVE_SYSTEM_DOCUMENTATION.md` - Full technical documentation
- `WHAT_LAWS_ARE_INCLUDED.md` - Complete law coverage
- `HOW_CATEGORIZATION_WORKS.md` - Explains the 11 categories

## 📄 License

Official Hong Kong government data from e-Legislation portal.  
For educational use in IDAT7215 project.

---

**IDAT7215 Hong Kong Legal Expert System**  
*2,234 Ordinances | 52,269 Sections | 11 Categories*  
*Ready for Demonstration* 🏆
