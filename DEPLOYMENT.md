# Deployment Guide

## Understanding Deployment Options

### Scenario 1: GitHub (Code Sharing Only) 
**What happens:** People can see and download your code  
**What they CAN'T do:** Visit a live website  
**What they MUST do:** Run the full setup on their own computer

### Scenario 2: Cloud Deployment (Live Website)
**What happens:** Anyone can visit a URL and use it immediately  
**What you MUST do:** Deploy to a cloud service  
**Challenge:** Local LLM (Ollama) won't work on most free hosting

---

## Option A: Push to GitHub (For Portfolio/Code Sharing)

### What to Push
```bash
# First, create .gitignore (already done!)
git add .
git commit -m "Initial commit: Hong Kong Legal Expert System with RAG"
git push origin main
```

**Included in GitHub:**
- ✅ All source code (`engine/`, `knowledge_base/`, `webapp/`)
- ✅ Setup scripts (`run.sh`, `setup_rag.sh`, `preprocess_data.sh`)
- ✅ Requirements file (`requirements.txt`)
- ✅ Documentation (`README.md`)
- ❌ Generated files (JSON database, embeddings)
- ❌ Virtual environment
- ❌ LLaMA models

### For Others to Use Your Code:
They must follow README.md instructions:
```bash
git clone https://github.com/YOUR_USERNAME/IDAT_7215_Project.git
cd IDAT_7215_Project
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
./preprocess_data.sh     # Generates JSON + embeddings
./setup_rag.sh          # Downloads Ollama + LLaMA
./run.sh                # Runs on their localhost:8080
```

**Use case:** Class project submission, portfolio, code sharing

---

## Option B: Deploy Live Website (Public URL)

### Challenge: LLaMA requires significant resources

Most free hosting services **cannot** run LLaMA locally because:
- LLaMA 3B needs ~2GB RAM minimum
- LLaMA 8B needs ~4.7GB RAM
- Free tiers typically give 512MB-1GB RAM

### Solution 1: Use Cloud LLM API (Recommended for Deployment)

Replace local Ollama with an API service:

**Options:**
1. **OpenAI API** (GPT-4 mini ~$0.15/1M tokens)
   - Modify `engine/rag_engine.py` to use OpenAI instead of Ollama
   
2. **Moonshot Kimi API** (mentioned in your search)
   - Chinese company, good for HK/Asian markets
   - https://platform.moonshot.ai
   
3. **Anthropic Claude API** (~$0.25/1M tokens)

4. **Hugging Face Inference API** (Free tier available)

### Solution 2: Deploy with Larger Instance (Paid)

**Services that can handle LLaMA:**
- **Railway.app** ($5-20/month for 4-8GB RAM)
- **Render.com** ($7+/month)
- **DigitalOcean** ($12+/month droplet)
- **AWS/GCP** (Pay as you go)

**Deployment steps:**
1. Choose a service
2. Connect your GitHub repo
3. Service auto-detects Flask app
4. Configure:
   ```
   Build Command: ./preprocess_data.sh
   Start Command: gunicorn webapp.app:app
   ```
5. Install Ollama in Docker container
6. Pull LLaMA model on first deploy

**Cons:** Expensive, complex setup for a class project

---

## Recommended Approach for Your Project

### For Class Submission:
**Push to GitHub** with excellent README:
- ✅ Code is there for professor/classmates to see
- ✅ Include screenshots/demo video
- ✅ They can run it locally if they want
- ✅ No hosting costs

### For Demo Day/Portfolio:
**Option 1:** Record a demo video showing the RAG system working  
**Option 2:** Deploy rule-based mode only (works on free hosting) + note "RAG requires local setup"  
**Option 3:** Use API-based LLM for deployment (I can help modify the code)

---

## What's Already Working

Your current setup is PERFECT for:
- ✅ Running locally with full RAG features
- ✅ Demonstrating in class (run on your laptop)
- ✅ Showing in portfolio (GitHub repo + demo video)
- ✅ Academic project submission

---

## Next Steps

**Right now:**
1. Download and install Ollama from https://ollama.ai/download
2. Run `./setup_rag.sh` to download LLaMA
3. Test with `./run.sh`

**For GitHub (later):**
```bash
git init  # if not already done
git add .
git commit -m "Add RAG-powered Hong Kong Legal Expert System"
git remote add origin <your-github-repo-url>
git push -u origin main
```

**For deployment (optional, later):**
- Let me know if you want to deploy it online
- I can help modify it to use API-based LLM instead of local Ollama

---

## Quick Answer to Your Questions

**Q1: Will GitHub visitors access the RAG?**  
❌ No - GitHub just stores code. They must run it themselves.

**Q2: Do I need to push all code?**  
✅ Yes, push all .py files and scripts  
❌ No, don't push venv/, generated JSON, embeddings  
📄 `.gitignore` (already created) handles this automatically
