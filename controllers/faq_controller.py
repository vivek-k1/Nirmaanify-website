import json
import os
import re
from flask import Blueprint, request, jsonify
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

faq_bp = Blueprint('faq', __name__)
FAQ_FILE = 'data/faqs.json'

class FAQRAGModel:
    def __init__(self):
        self.faqs = []
        self.vectorizer = TfidfVectorizer(
            lowercase=True,
            stop_words='english',
            ngram_range=(1, 2),
            max_features=1000
        )
        self.faq_vectors = None
        self.load_faqs()
        self.build_index()
    
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
    
    def build_index(self):
        if not self.faqs:
            return
        documents = []
        for faq in self.faqs:
            combined_text = f"{faq['question']} {faq['answer']} {' '.join(faq.get('keywords', []))}"
            documents.append(self.preprocess_text(combined_text))
        self.faq_vectors = self.vectorizer.fit_transform(documents)
    
    def search_faqs(self, query, top_k=3, threshold=0.1):
        if not self.faqs or self.faq_vectors is None:
            return []
        processed_query = self.preprocess_text(query)
        query_vector = self.vectorizer.transform([processed_query])
        similarities = cosine_similarity(query_vector, self.faq_vectors).flatten()
        top_indices = np.argsort(similarities)[::-1][:top_k]
        
        results = []
        for idx in top_indices:
            if similarities[idx] > threshold:
                faq = self.faqs[idx].copy()
                faq['similarity_score'] = float(similarities[idx])
                results.append(faq)
        
        return results
    
    def get_all_faqs(self):
        return self.faqs
    
    def get_faq_by_category(self, category):
        return [faq for faq in self.faqs if faq.get('category') == category]

rag_model = FAQRAGModel()

@faq_bp.route('/faq/search', methods=['POST'])
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
        'model_ready': rag_model.faq_vectors is not None
    })
