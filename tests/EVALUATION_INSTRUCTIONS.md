# System Accuracy Evaluation Guide

## 🎯 Purpose

This evaluation system measures **actual accuracy** of your Hong Kong Legal Expert System components, giving you **real numbers** instead of estimates for your PPT and report.

---

## 📁 Files

1. **`scripts/evaluate_accuracy.py`** - Main evaluation script
2. **`tests/accuracy_test_cases.json`** - Test data (customize this!)
3. **`evaluation_results.txt`** - Output results (auto-generated)

---

## 🚀 Quick Start (3 Steps)

### Step 1: Customize Test Cases

Edit `tests/accuracy_test_cases.json` and add your own test cases:

```json
{
  "nlp_tests": [
    {
      "query": "Your test query here",
      "expected_facts": ["fact1", "fact2"],
      "expected_entities": {"amount": 5000}
    }
  ],
  "search_tests": [
    {
      "query": "search query",
      "relevant_sections": ["Cap210_s2", "Cap210_s9"]
    }
  ]
}
```

**Important:** 
- Use **actual section IDs** from your legislation database
- Use **actual case names** from your case database
- Add 20-50 test cases per category for reliable results

### Step 2: Run Evaluation

```bash
cd /Users/wingyin/Documents/GitHub/IDAT_7215_Project
python scripts/evaluate_accuracy.py
```

### Step 3: View Results

Results will be printed to console and saved to `evaluation_results.txt`:

```
SYSTEM ACCURACY EVALUATION REPORT
==================================================

① NLP Fact Extraction: 82.3%
   Correct: 37/45 facts

② Hybrid Search Precision@5: 87.1%
   Test cases: 20

⑤ Enhanced Rule Engine:
   Manual (Tier 1): 98.5% (20/20)
   Auto (Tier 2): 74.2% (23/31)
   Fallback (Tier 3): 58.3% (7/12)

⑥ Case Matching MAP: 71.8%
   Test cases: 15
```

---

## 📊 What Gets Measured

### ① NLP Processing
- **Metric:** Fact extraction accuracy
- **Calculation:** `correct_facts / total_expected_facts`
- **Example:** If expected 10 facts, extracted 8 correctly → 80%

### ② Hybrid Search
- **Metric:** Precision@5
- **Calculation:** `relevant_docs_in_top5 / 5`
- **Example:** Query returns 3 relevant in top 5 → 60%

### ③④ Semantic + TF-IDF
- Measured as part of Hybrid Search

### ⑤ Enhanced Rule Engine
- **Tier 1 (Manual):** % matching correct manual rules
- **Tier 2 (Auto):** % matching correct auto-generated rules  
- **Tier 3 (Fallback):** % returning relevant fallback results

### ⑥ Case Matching
- **Metric:** Mean Average Precision (MAP)
- **Calculation:** Average of precision scores at each relevant result

### ⑦ Risk Assessment
- Would need historical case outcomes to measure
- Currently not included in automated evaluation

### ⑧ RAG Pipeline
- Requires expert human evaluation
- Currently not included in automated evaluation

---

## 📝 How to Add Test Cases

### NLP Tests

```json
{
  "query": "Person stole laptop worth HK$50,000",
  "expected_facts": [
    "appropriates_property",
    "acts_dishonestly", 
    "property_has_value",
    "high_value_property"
  ],
  "expected_entities": {
    "amount": 50000,
    "property_type": "laptop"
  },
  "notes": "Simple theft scenario"
}
```

**How to create:**
1. Write a test query
2. Run it through your NLP analyzer manually
3. Verify which facts SHOULD be extracted
4. Add to test file

### Search Tests

```json
{
  "query": "theft ordinance Hong Kong",
  "relevant_sections": ["Cap210_s2", "Cap210_s9", "Cap210_s25"],
  "notes": "Should retrieve Theft Ordinance sections"
}
```

**How to create:**
1. Think of a search query
2. Manually find which sections are truly relevant
3. Get their section IDs from your database
4. Add to test file

**Finding Section IDs:**
```python
# Run this to find section IDs
from knowledge_base.json_loader import ALL_ORDINANCES

for cap, ord_data in ALL_ORDINANCES.items():
    if "theft" in ord_data.get('title', '').lower():
        print(f"{cap}: {ord_data['title']}")
        for sec_id, section in ord_data.get('sections', {}).items():
            print(f"  - {sec_id}: {section.get('title', '')}")
```

### Rule Engine Tests

```json
{
  "facts": ["appropriates_property", "acts_dishonestly"],
  "query": "theft of property",
  "expected_match": true,
  "expected_tier": 1,
  "notes": "Should match manual theft rule"
}
```

**Tier values:**
- `1` = Should match manual rule
- `2` = Should match auto-generated rule
- `3` = Should fall back to search

### Case Matching Tests

```json
{
  "query": "theft laptop workplace employee",
  "relevant_cases": ["HKCA 123/2020", "HKDC 456/2019"],
  "notes": "Should match workplace theft cases"
}
```

**Finding Case Names:**
```python
from knowledge_base.all_cases_database import ALL_CASES

for case in ALL_CASES[:10]:
    print(f"{case.case_name}: {case.facts[:100]}...")
```

---

## 🎯 Recommended Test Set Size

For reliable accuracy measurements:

| Component | Minimum | Recommended | Why |
|-----------|---------|-------------|-----|
| NLP | 20 cases | 50 cases | Cover different offense types |
| Search | 15 queries | 30 queries | Cover different legal areas |
| Rule Engine | 20 scenarios | 40 scenarios | Test each tier separately |
| Case Matching | 10 queries | 20 queries | Limited by case database size |

**Total time to create:** 2-4 hours (but gives you real numbers!)

---

## 📈 Using Results in Your PPT

### Before (Estimated):
```
"NLP Processing: ~85% accuracy (estimated)"
```

### After (Measured):
```
"NLP Processing: 82.3% accuracy (measured on 45 test cases)"
```

### Copy to PPT:

Use the auto-generated table from `evaluation_results.txt`:

```
| Component         | Measured Accuracy | Test Cases |
|-------------------|-------------------|------------|
| NLP Processing    | 82.3%            | 45         |
| Hybrid Search     | 87.1%            | 20         |
| Rule Tier 1       | 98.5%            | 20         |
| Rule Tier 2       | 74.2%            | 31         |
| Case Matching     | 71.8%            | 15         |
```

---

## 🐛 Troubleshooting

### Error: "No legislation loaded"
- Make sure you've run `preprocess_legislation.py` first
- Check that `legislation_database.json` exists

### Error: "Module not found"
- Run from project root: `python scripts/evaluate_accuracy.py`
- Check your Python path

### Low accuracy scores?
- **Normal!** Real systems rarely achieve 95%+
- 70-85% is actually very good for NLP/search tasks
- Use this as baseline to improve

### Want to test RAG accuracy?
- Requires manual expert evaluation
- Create 20 queries, get RAG responses
- Have legal expert rate: Correct/Partially Correct/Incorrect
- Calculate: `accuracy = correct / total`

---

## 💡 Tips for Better Results

### For NLP Tests:
- Include edge cases (typos, unusual phrasing)
- Test different offense types
- Include queries with multiple facts

### For Search Tests:
- Use both broad and specific queries
- Test synonyms ("theft" vs "steal")
- Include multi-word legal terms

### For Rule Tests:
- Test boundary conditions (e.g., value exactly $10,000)
- Include scenarios that should NOT match
- Test each tier separately

### For Case Tests:
- Use realistic query language
- Include both criminal and civil cases
- Test different similarity levels

---

## 📊 Interpreting Results

### Good Accuracy Ranges:

| Component | Excellent | Good | Fair | Needs Work |
|-----------|-----------|------|------|------------|
| NLP | >85% | 75-85% | 65-75% | <65% |
| Search | >80% | 70-80% | 60-70% | <60% |
| Manual Rules | >95% | 90-95% | 80-90% | <80% |
| Auto Rules | >75% | 65-75% | 55-65% | <55% |
| Case Matching | >75% | 65-75% | 55-65% | <55% |

**Remember:** Even professional systems rarely exceed 90% on complex NLP tasks!

---

## 🔄 Iterative Improvement

1. **Run initial evaluation** → Get baseline
2. **Identify weakest component** → Focus improvement
3. **Modify system** → Improve rules, patterns, etc.
4. **Re-run evaluation** → Measure improvement
5. **Repeat** until satisfied

Example improvement cycle:
```
Initial:  NLP 72% → Improve patterns → Retest: 82%
Initial:  Search 68% → Adjust weights → Retest: 87%
```

---

## ✅ Final Checklist

Before your presentation:

- [ ] Added 20+ test cases per component
- [ ] Run `python scripts/evaluate_accuracy.py`
- [ ] Results saved to `evaluation_results.txt`
- [ ] Copied accuracy table to PPT
- [ ] Can explain how you measured accuracy
- [ ] Know your system's strengths and weaknesses

---

## 📞 Quick Reference

**Run evaluation:**
```bash
python scripts/evaluate_accuracy.py
```

**View results:**
```bash
cat evaluation_results.txt
```

**Add test cases:**
```bash
# Edit this file
open tests/accuracy_test_cases.json
```

---

**Created:** November 18, 2025  
**Purpose:** Get real accuracy numbers for PPT/report  
**Time required:** 2-4 hours to create comprehensive test set  
**Benefit:** Real data > estimates!
