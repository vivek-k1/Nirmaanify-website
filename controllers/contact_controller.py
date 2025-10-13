from flask import Blueprint, request, jsonify
import json
import os
from datetime import datetime

contact_bp = Blueprint('contact', __name__)

# Data file path
DATA_FILE = 'data/submissions.json'

def load_data():
    """Load existing data from JSON file"""
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return {'contacts': [], 'services': [], 'internships': []}

def save_data(data):
    """Save data to JSON file"""
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

@contact_bp.route('/contact', methods=['POST'])
def submit_contact():
    try:
        # Get form data
        form_data = request.get_json()
        
        # Validate required fields
        required_fields = ['name', 'email', 'subject', 'message']
        for field in required_fields:
            if not form_data.get(field):
                return jsonify({
                    'success': False,
                    'error': f'Missing required field: {field}'
                }), 400
        
        # Create contact submission
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
        
        # Load existing data
        data = load_data()
        
        # Add new contact submission
        data['contacts'].append(contact_submission)
        
        # Save updated data
        save_data(data)
        
        # Log submission (for debugging)
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
    """Get a specific contact submission by ID"""
    try:
        data = load_data()
        
        # Find the submission
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
    """Get all contact submissions"""
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