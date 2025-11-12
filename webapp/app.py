"""
IDAT7215 Hong Kong Legal Expert System - Web Application
Flask-based web interface for comprehensive legal consultation covering all HK law
"""

import sys
import os

# Add project root to Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from flask import Flask, render_template, request, jsonify, Response, stream_with_context
from engine.rule_engine import InferenceEngine, analyze_case
from engine.case_matcher import CaseMatcher
from engine.document_analyzer import DocumentAnalyzer
from engine.explanation import generate_legal_advice_disclaimer

# Import enhanced analyzer for better analysis
try:
    from engine.enhanced_analyzer import get_enhanced_analyzer
    ENHANCED_AVAILABLE = True
except:
    ENHANCED_AVAILABLE = False

# Import comprehensive knowledge base with ALL HK law (using fast JSON loader)
from knowledge_base import json_loader as hk_ordinances
from knowledge_base import all_cases_database as case_database

# Import RAG engine
try:
    from engine.rag_engine import RAGLegalEngine
    RAG_AVAILABLE = True
    print("✅ RAG engine available")
except Exception as e:
    RAG_AVAILABLE = False
    print(f"⚠️  RAG engine not available: {e}")

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hk-criminal-law-expert-system-2024'

# Initialize components
case_matcher = CaseMatcher()
document_analyzer = DocumentAnalyzer()

# Initialize RAG engine (lazy loading)
rag_engine = None
def get_rag_engine():
    """Get or initialize RAG engine"""
    global rag_engine
    if rag_engine is None and RAG_AVAILABLE:
        try:
            print("Initializing RAG engine...")
            rag_engine = RAGLegalEngine()
        except Exception as e:
            print(f"Failed to initialize RAG engine: {e}")
            return None
    return rag_engine

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

@app.route('/api/rag-consultation', methods=['POST'])
def api_rag_consultation():
    """
    RAG-powered legal consultation endpoint
    Uses hybrid search + LLaMA for intelligent advice
    """
    try:
        data = request.json
        query = data.get('query', '')
        stream = data.get('stream', False)
        
        if not query:
            return jsonify({'error': 'No query provided'}), 400
        
        # Check if RAG is available
        engine = get_rag_engine()
        if engine is None:
            return jsonify({
                'error': 'RAG engine not available',
                'message': 'Please ensure Ollama is running and embeddings are generated'
            }), 503
        
        # Stream response
        if stream:
            def generate():
                try:
                    result = engine.consult(query, stream=True)
                    
                    # Send sources first
                    import json
                    sources_data = {
                        'type': 'sources',
                        'legislation_count': len(result['sources']['legislation']),
                        'cases_count': len(result['sources']['cases']),
                        'citations': engine.get_source_citations(result['sources'])
                    }
                    yield f"data: {json.dumps(sources_data)}\n\n"
                    
                    # Stream advice
                    for chunk in result['advice']:
                        chunk_data = {
                            'type': 'advice',
                            'content': chunk
                        }
                        yield f"data: {json.dumps(chunk_data)}\n\n"
                    
                    # Send completion
                    yield f"data: {json.dumps({'type': 'done'})}\n\n"
                    
                except Exception as e:
                    error_data = {
                        'type': 'error',
                        'message': str(e)
                    }
                    yield f"data: {json.dumps(error_data)}\n\n"
            
            return Response(
                stream_with_context(generate()),
                mimetype='text/event-stream',
                headers={
                    'Cache-Control': 'no-cache',
                    'X-Accel-Buffering': 'no'
                }
            )
        
        # Non-streaming response
        else:
            result = engine.consult(query, stream=False)
            
            # Get citations
            citations = engine.get_source_citations(result['sources'])
            
            return jsonify({
                'success': True,
                'query': result['query'],
                'advice': result['advice'],
                'legislation_count': result['legislation_count'],
                'cases_count': result['cases_count'],
                'citations': citations,
                'disclaimer': generate_legal_advice_disclaimer()
            })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/rag-status')
def api_rag_status():
    """Check if RAG engine is available"""
    engine = get_rag_engine()
    return jsonify({
        'available': engine is not None,
        'ollama_installed': RAG_AVAILABLE,
        'indexed': engine.search_engine.is_indexed if engine else False
    })

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

@app.route('/api/analyze-enhanced', methods=['POST'])
def api_analyze_enhanced():
    """
    Enhanced legal analysis with semantic search and context awareness
    """
    try:
        if not ENHANCED_AVAILABLE:
            return jsonify({'error': 'Enhanced analyzer not available'}), 503
        
        data = request.json
        text = data.get('text', '')
        
        if not text:
            return jsonify({'error': 'No text provided'}), 400
        
        # Run enhanced analysis
        analyzer = get_enhanced_analyzer()
        result = analyzer.analyze(text)
        
        return jsonify(result)
    
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

@app.route('/api/category/<category_name>')
def api_category_ordinances(category_name):
    """Get all ordinances in a specific category"""
    try:
        ordinances_list = []
        
        # Get all ordinances
        for cap_key, ordinance in hk_ordinances.ALL_ORDINANCES.items():
            if ordinance.get('category') == category_name:
                ordinances_list.append({
                    'chapter': ordinance.get('chapter', ''),
                    'title': ordinance.get('title', ''),
                    'num_sections': len(ordinance.get('sections', {})),
                    'category': category_name
                })
        
        # Sort by chapter number
        ordinances_list.sort(key=lambda x: int(x['chapter']) if x['chapter'].isdigit() else 9999)
        
        return jsonify({
            'success': True,
            'category': category_name,
            'ordinances': ordinances_list,
            'total': len(ordinances_list)
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/category/<category_name>')
def category_browser(category_name):
    """Category browser page"""
    return render_template('category_browser.html', category=category_name)

@app.route('/ordinance/<chapter>')
def ordinance_detail_page(chapter):
    """Ordinance detail webpage"""
    return render_template('ordinance_detail.html', chapter=chapter)

@app.route('/api/ordinance/<chapter>')
def api_ordinance_detail(chapter):
    """Get details of a specific ordinance"""
    try:
        cap_key = f'cap_{chapter}'
        if cap_key in hk_ordinances.ALL_ORDINANCES:
            ordinance = hk_ordinances.ALL_ORDINANCES[cap_key]
            info = {
                'chapter': ordinance.get('chapter'),
                'title': ordinance.get('title', ''),
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

@app.route('/api/ordinance/<chapter>/sections')
def api_ordinance_sections(chapter):
    """Get all sections of an ordinance"""
    try:
        cap_key = f'cap_{chapter}'
        if cap_key in hk_ordinances.ALL_ORDINANCES:
            ordinance = hk_ordinances.ALL_ORDINANCES[cap_key]
            sections = ordinance.get('sections', {})
            
            sections_list = []
            for num, data in sections.items():
                sections_list.append({
                    'number': num,
                    'title': data.get('title', ''),
                    'text': data.get('text', ''),
                    'penalty': data.get('penalty', '')
                })
            
            # Sort by section number
            sections_list.sort(key=lambda x: int(x['number']) if x['number'].isdigit() else 9999)
            
            return jsonify({
                'success': True,
                'sections': sections_list
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

