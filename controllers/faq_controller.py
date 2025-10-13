import json
import os
import re
from flask import Blueprint, request, jsonify

faq_bp = Blueprint('faq', __name__)
FAQ_FILE = 'data/faqs.json'

class FAQRAGModel:
    def __init__(self):
        self.faqs = []
        self.load_faqs()
    
    def load_faqs(self):
        try:
            with open(FAQ_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.faqs = data.get('faqs', [])
        except FileNotFoundError:
            self.faqs = []
    
    def preprocess_text(self, text):
        text = re.sub(r'[^a-zA-Z0-9\s]', '', text.lower())
        return text.strip()
    
    def simple_similarity(self, query, text):
        """Simple keyword-based similarity scoring"""
        query_words = set(self.preprocess_text(query).split())
        text_words = set(self.preprocess_text(text).split())
        
        if not query_words or not text_words:
            return 0
        
        intersection = query_words.intersection(text_words)
        union = query_words.union(text_words)
        
        return len(intersection) / len(union) if union else 0
    
    def search_faqs(self, query, top_k=3, threshold=0.1):
        if not self.faqs:
            return []
        
        results = []
        for faq in self.faqs:
            combined_text = f"{faq['question']} {faq['answer']} {' '.join(faq.get('keywords', []))}"
            similarity = self.simple_similarity(query, combined_text)
            
            if similarity > threshold:
                faq_copy = faq.copy()
                faq_copy['similarity_score'] = similarity
                results.append(faq_copy)
        
        # Sort by similarity score and return top_k
        results.sort(key=lambda x: x['similarity_score'], reverse=True)
        return results[:top_k]
    
    def get_all_faqs(self):
        return self.faqs
    
    def get_faq_by_category(self, category):
        return [faq for faq in self.faqs if faq.get('category') == category]

rag_model = FAQRAGModel()

@faq_bp.route('/api/faq/search', methods=['POST'])
def search_faq():
    try:
        data = request.get_json()
        query = data.get('query', '').strip()
        
        if not query:
            return jsonify({
                'success': False,
                'error': 'Query is required'
            }), 400
        results = rag_model.search_faqs(query, top_k=3)
        
        return jsonify({
            'success': True,
            'query': query,
            'results': results,
            'total_results': len(results)
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@faq_bp.route('/faq/all', methods=['GET'])
def get_all_faqs():
    try:
        faqs = rag_model.get_all_faqs()
        return jsonify({
            'success': True,
            'faqs': faqs,
            'total': len(faqs)
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@faq_bp.route('/faq/category/<category>', methods=['GET'])
def get_faqs_by_category(category):
    try:
        faqs = rag_model.get_faq_by_category(category)
        return jsonify({
            'success': True,
            'category': category,
            'faqs': faqs,
            'total': len(faqs)
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@faq_bp.route('/faq/health', methods=['GET'])
def faq_health():
        return jsonify({
            'success': True,
            'status': 'healthy',
            'total_faqs': len(rag_model.get_all_faqs()),
            'model_ready': True
        })
