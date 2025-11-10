"""
IDAT7215 Hong Kong Legal Expert System - Web Application
Flask-based web interface for comprehensive legal consultation covering all HK law
"""

import sys
import os

# Add project root to Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from flask import Flask, render_template, request, jsonify
from engine.rule_engine import InferenceEngine, analyze_case
from engine.case_matcher import CaseMatcher
from engine.document_analyzer import DocumentAnalyzer
from engine.explanation import generate_legal_advice_disclaimer

# Import comprehensive knowledge base with ALL HK law
from knowledge_base import hk_all_ordinances as hk_ordinances
from knowledge_base import all_cases_database as case_database

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hk-criminal-law-expert-system-2024'

# Initialize components
case_matcher = CaseMatcher()
document_analyzer = DocumentAnalyzer()

@app.route('/')
def index():
    """Home page"""
    return render_template('index.html')

@app.route('/consultation')
def consultation():
    """Legal consultation page"""
    return render_template('consultation.html')

@app.route('/case-search')
def case_search():
    """Case search page"""
    return render_template('case_search.html')

@app.route('/document-analysis')
def document_analysis():
    """Document analysis page"""
    return render_template('document_analysis.html')

@app.route('/api/analyze', methods=['POST'])
def api_analyze():
    """
    API endpoint for legal analysis
    Accepts facts and returns legal opinion
    """
    try:
        data = request.json
        facts = data.get('facts', [])
        
        if not facts:
            return jsonify({'error': 'No facts provided'}), 400
        
        # Run inference
        engine = analyze_case(facts)
        
        # Get results
        offences = engine.get_offences()
        defenses = engine.get_defenses()
        explanation = engine.explain()
        summary = engine.get_summary()
        
        return jsonify({
            'success': True,
            'offences': [
                {
                    'name': o['offence'],
                    'ordinance_ref': o['ordinance_ref'],
                    'penalty': o['penalty']
                } for o in offences
            ],
            'defenses': [
                {
                    'name': d.name,
                    'effect': d.effect,
                    'explanation': d.explanation
                } for d in defenses
            ],
            'explanation': explanation,
            'summary': summary,
            'disclaimer': generate_legal_advice_disclaimer()
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/search-cases', methods=['POST'])
def api_search_cases():
    """
    API endpoint for case search
    Finds similar cases based on facts
    """
    try:
        data = request.json
        query_text = data.get('query', '')
        top_n = data.get('top_n', 5)
        
        if not query_text:
            return jsonify({'error': 'No query provided'}), 400
        
        # Find similar cases
        similar_cases = case_matcher.find_similar_cases(query_text, top_n)
        
        results = []
        for case, similarity in similar_cases:
            results.append({
                'case_name': case.case_name,
                'year': case.year,
                'court': case.court,
                'facts': case.facts[:300] + '...' if len(case.facts) > 300 else case.facts,
                'charges': case.charges,
                'outcome': case.outcome,
                'sentence': case.sentence,
                'legal_principles': case.legal_principles,
                'similarity': f"{similarity:.1%}"
            })
        
        return jsonify({
            'success': True,
            'results': results,
            'total': len(results)
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/analyze-document', methods=['POST'])
def api_analyze_document():
    """
    API endpoint for document analysis
    Extracts facts and identifies legal issues
    """
    try:
        data = request.json
        document_text = data.get('text', '')
        
        if not document_text:
            return jsonify({'error': 'No document text provided'}), 400
        
        # Analyze document
        analysis = document_analyzer.analyze_document(document_text)
        
        # Extract facts for inference
        extracted_facts = document_analyzer.extract_for_inference(document_text)
        
        # Run inference if facts found
        inference_results = None
        if extracted_facts:
            engine = analyze_case(extracted_facts)
            offences = engine.get_offences()
            inference_results = {
                'offences': [
                    {
                        'name': o['offence'],
                        'ordinance_ref': o['ordinance_ref'],
                        'penalty': o['penalty']
                    } for o in offences
                ],
                'explanation': engine.explain()
            }
        
        return jsonify({
            'success': True,
            'analysis': {
                'summary': analysis['summary'],
                'offences': analysis['offences'],
                'facts': analysis['facts'],
                'parties': analysis['parties'],
                'dates': analysis['dates'],
                'amounts': analysis['amounts'],
                'locations': analysis['locations'],
                'legal_issues': analysis['legal_issues']
            },
            'extracted_facts': extracted_facts,
            'inference_results': inference_results
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/ordinances')
def api_ordinances():
    """Get list of available ordinances"""
    try:
        ordinances = hk_ordinances.list_all_ordinances()
        return jsonify({
            'success': True,
            'ordinances': ordinances[:100]  # Return first 100 for performance
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/categories')
def api_categories():
    """Get legal categories summary"""
    try:
        categories = hk_ordinances.get_categories_summary()
        return jsonify({
            'success': True,
            'categories': categories
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/ordinance/<chapter>')
def api_ordinance_detail(chapter):
    """Get details of a specific ordinance"""
    try:
        cap_key = f'cap_{chapter}'
        if cap_key in hk_ordinances.ALL_ORDINANCES:
            ordinance = hk_ordinances.ALL_ORDINANCES[cap_key]
            info = {
                'chapter': ordinance.get('chapter'),
                'title': ordinance.get('full_title', ''),
                'num_sections': len(ordinance.get('sections', {}))
            }
            return jsonify({
                'success': True,
                'ordinance': info
            })
        else:
            return jsonify({'error': 'Ordinance not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/ordinance/<chapter>/<section>')
def api_ordinance_section(chapter, section):
    """Get specific section of an ordinance"""
    try:
        section_data = hk_ordinances.get_ordinance_section(chapter, section)
        if section_data:
            return jsonify({
                'success': True,
                'section': section_data
            })
        else:
            return jsonify({'error': 'Section not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/cases')
def api_all_cases():
    """Get all cases"""
    try:
        all_cases = case_database.ALL_CASES
        results = []
        for case in all_cases:
            results.append({
                'case_id': case.case_id,
                'case_name': case.case_name,
                'year': case.year,
                'outcome': case.outcome,
                'keywords': case.keywords[:5]  # First 5 keywords
            })
        return jsonify({
            'success': True,
            'cases': results,
            'total': len(results)
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/case/<case_id>')
def api_case_detail(case_id):
    """Get details of a specific case"""
    try:
        case = case_database.get_case_by_id(case_id)
        if case:
            return jsonify({
                'success': True,
                'case': case.to_dict()
            })
        else:
            return jsonify({'error': 'Case not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/stats')
def api_stats():
    """Get system statistics"""
    try:
        return jsonify({
            'success': True,
            'stats': {
                'total_ordinances': hk_ordinances.TOTAL_ORDINANCES,
                'total_sections': hk_ordinances.TOTAL_SECTIONS,
                'total_cases': case_database.TOTAL_CASES,
                'categories': hk_ordinances.get_categories_summary()
            }
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500

if __name__ == '__main__':
    print("\n" + "="*70)
    print("IDAT7215 Hong Kong Legal Expert System")
    print("="*70)
    print(f"Loaded {hk_ordinances.TOTAL_SECTIONS} sections from {hk_ordinances.TOTAL_ORDINANCES} ordinances")
    print(f"\nCategories:")
    for cat, info in sorted(hk_ordinances.STATS['categories'].items(), key=lambda x: x[1]['sections'], reverse=True)[:5]:
        print(f"  {cat}: {info['count']} ordinances, {info['sections']} sections")
    print(f"Case database: {case_database.TOTAL_CASES} cases")
    print("="*70)
    print("\nStarting web server...")
    print("Access the system at: http://localhost:8080")
    print("="*70 + "\n")
    
    app.run(debug=True, host='0.0.0.0', port=8080)

