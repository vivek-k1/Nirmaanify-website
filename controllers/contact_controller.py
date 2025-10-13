from flask import Blueprint, request, jsonify
import json
import os
from datetime import datetime

contact_bp = Blueprint('contact', __name__)
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

@contact_bp.route('/contact', methods=['POST'])
def submit_contact():
    try:
        form_data = request.get_json()
        required_fields = ['name', 'email', 'subject', 'message']
        for field in required_fields:
            if not form_data.get(field):
                return jsonify({
                    'success': False,
                    'error': f'Missing required field: {field}'
                }), 400
        contact_submission = {
            'id': f'contact_{datetime.now().strftime("%Y%m%d_%H%M%S")}',
            'type': 'contact',
            'timestamp': datetime.now().isoformat(),
            'data': {
                'name': form_data['name'],
                'email': form_data['email'],
                'phone': form_data.get('phone', ''),
                'subject': form_data['subject'],
                'message': form_data['message'],
                'urgency': form_data.get('urgency', ''),
                'budget': form_data.get('budget', '')
            }
        }
        data = load_data()
        data['contacts'].append(contact_submission)
        save_data(data)
        print(f"📧 New contact submission from: {form_data['name']} ({form_data['email']})")
        print(f"   Subject: {form_data['subject']}")
        print(f"   Urgency: {form_data.get('urgency', 'Not specified')}")
        
        return jsonify({
            'success': True,
            'message': 'Contact form submitted successfully!',
            'submission_id': contact_submission['id'],
            'timestamp': contact_submission['timestamp']
        }), 201
        
    except Exception as e:
        print(f"❌ Error processing contact form: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Internal server error',
            'message': 'Failed to process contact form submission'
        }), 500

@contact_bp.route('/contact/<submission_id>', methods=['GET'])
def get_contact_submission(submission_id):
    try:
        data = load_data()
        for contact in data['contacts']:
            if contact['id'] == submission_id:
                return jsonify({
                    'success': True,
                    'data': contact
                })
        
        return jsonify({
            'success': False,
            'error': 'Contact submission not found'
        }), 404
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': 'Internal server error'
        }), 500

@contact_bp.route('/contact', methods=['GET'])
def get_all_contacts():
    try:
        data = load_data()
        return jsonify({
            'success': True,
            'data': data['contacts'],
            'count': len(data['contacts'])
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': 'Internal server error'
        }), 500