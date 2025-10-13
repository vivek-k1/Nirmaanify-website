from flask import Blueprint, request, jsonify
import json
import os
from datetime import datetime

services_bp = Blueprint('services', __name__)
DATA_FILE = 'data/submissions.json'

def load_data():
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return {'contacts': [], 'services': [], 'internships': []}

def save_data(data):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

@services_bp.route('/services', methods=['POST'])
def submit_service_request():
    try:
        form_data = request.get_json()
        required_fields = ['name', 'email', 'service', 'project-details']
        for field in required_fields:
            if not form_data.get(field):
                return jsonify({
                    'success': False,
                    'error': f'Missing required field: {field}'
                }), 400
        service_submission = {
            'id': f'service_{datetime.now().strftime("%Y%m%d_%H%M%S")}',
            'type': 'service_request',
            'timestamp': datetime.now().isoformat(),
            'data': {
                'name': form_data['name'],
                'email': form_data['email'],
                'company': form_data.get('company', ''),
                'service': form_data['service'],
                'project_details': form_data['project-details'],
                'budget': form_data.get('budget', ''),
                'timeline': form_data.get('timeline', '')
            }
        }
        data = load_data()
        data['services'].append(service_submission)
        save_data(data)
        print(f"🔧 New service request from: {form_data['name']} ({form_data['email']})")
        print(f"   Service: {form_data['service']}")
        print(f"   Company: {form_data.get('company', 'Not specified')}")
        print(f"   Budget: {form_data.get('budget', 'Not specified')}")
        
        return jsonify({
            'success': True,
            'message': 'Service request submitted successfully!',
            'submission_id': service_submission['id'],
            'timestamp': service_submission['timestamp']
        }), 201
        
    except Exception as e:
        print(f"❌ Error processing service request: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Internal server error',
            'message': 'Failed to process service request submission'
        }), 500

@services_bp.route('/services/<submission_id>', methods=['GET'])
def get_service_submission(submission_id):
    try:
        data = load_data()
        for service in data['services']:
            if service['id'] == submission_id:
                return jsonify({
                    'success': True,
                    'data': service
                })
        
        return jsonify({
            'success': False,
            'error': 'Service submission not found'
        }), 404
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': 'Internal server error'
        }), 500

@services_bp.route('/services', methods=['GET'])
def get_all_services():
    try:
        data = load_data()
        return jsonify({
            'success': True,
            'data': data['services'],
            'count': len(data['services'])
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': 'Internal server error'
        }), 500

@services_bp.route('/services/stats', methods=['GET'])
def get_service_stats():
    try:
        data = load_data()
        services = data['services']
        service_counts = {}
        budget_counts = {}
        for service in services:
            service_type = service['data']['service']
            budget = service['data']['budget']
            service_counts[service_type] = service_counts.get(service_type, 0) + 1
            if budget:
                budget_counts[budget] = budget_counts.get(budget, 0) + 1
        
        return jsonify({
            'success': True,
            'stats': {
                'total_requests': len(services),
                'service_distribution': service_counts,
                'budget_distribution': budget_counts,
                'recent_requests': len([s for s in services if s['timestamp'].startswith(datetime.now().strftime("%Y-%m-%d"))])
            }
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': 'Internal server error'
        }), 500