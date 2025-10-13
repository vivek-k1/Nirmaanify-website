from flask import Blueprint, request, jsonify
import json
import os
from datetime import datetime

training_bp = Blueprint('training', __name__)
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

@training_bp.route('/training', methods=['POST'])
def submit_internship_application():
    try:
        form_data = request.get_json()
        required_fields = ['name', 'email', 'phone', 'area', 'skills', 'duration', 'motivation']
        for field in required_fields:
            if not form_data.get(field):
                return jsonify({
                    'success': False,
                    'error': f'Missing required field: {field}'
                }), 400
        internship_submission = {
            'id': f'internship_{datetime.now().strftime("%Y%m%d_%H%M%S")}',
            'type': 'internship_application',
            'timestamp': datetime.now().isoformat(),
            'data': {
                'name': form_data['name'],
                'email': form_data['email'],
                'phone': form_data['phone'],
                'college': form_data.get('college', ''),
                'course': form_data.get('course', ''),
                'year': form_data.get('year', ''),
                'area': form_data['area'],
                'skills': form_data['skills'],
                'duration': form_data['duration'],
                'start_date': form_data.get('start-date', ''),
                'availability': form_data.get('availability', ''),
                'motivation': form_data['motivation']
            }
        }
        data = load_data()
        data['internships'].append(internship_submission)
        save_data(data)
        print(f"🎓 New internship application from: {form_data['name']} ({form_data['email']})")
        print(f"   Area: {form_data['area']}")
        print(f"   Duration: {form_data['duration']}")
        print(f"   College: {form_data.get('college', 'Not specified')}")
        
        return jsonify({
            'success': True,
            'message': 'Internship application submitted successfully!',
            'submission_id': internship_submission['id'],
            'timestamp': internship_submission['timestamp']
        }), 201
        
    except Exception as e:
        print(f"❌ Error processing internship application: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Internal server error',
            'message': 'Failed to process internship application submission'
        }), 500

@training_bp.route('/training/<submission_id>', methods=['GET'])
def get_internship_submission(submission_id):
    try:
        data = load_data()
        for internship in data['internships']:
            if internship['id'] == submission_id:
                return jsonify({
                    'success': True,
                    'data': internship
                })
        
        return jsonify({
            'success': False,
            'error': 'Internship submission not found'
        }), 404
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': 'Internal server error'
        }), 500

@training_bp.route('/training', methods=['GET'])
def get_all_internships():
    try:
        data = load_data()
        return jsonify({
            'success': True,
            'data': data['internships'],
            'count': len(data['internships'])
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': 'Internal server error'
        }), 500

@training_bp.route('/training/stats', methods=['GET'])
def get_internship_stats():
    try:
        data = load_data()
        internships = data['internships']
        area_counts = {}
        duration_counts = {}
        year_counts = {}
        for internship in internships:
            area = internship['data']['area']
            duration = internship['data']['duration']
            year = internship['data']['year']
            area_counts[area] = area_counts.get(area, 0) + 1
            duration_counts[duration] = duration_counts.get(duration, 0) + 1
            if year:
                year_counts[year] = year_counts.get(year, 0) + 1
        
        return jsonify({
            'success': True,
            'stats': {
                'total_applications': len(internships),
                'area_distribution': area_counts,
                'duration_distribution': duration_counts,
                'year_distribution': year_counts,
                'recent_applications': len([i for i in internships if i['timestamp'].startswith(datetime.now().strftime("%Y-%m-%d"))])
            }
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': 'Internal server error'
        }), 500

@training_bp.route('/training/areas', methods=['GET'])
def get_internship_areas():
    areas = [
        'frontend',
        'backend', 
        'mobile',
        'ui-ux',
        'devops',
        'data-science',
        'other'
    ]
    
    return jsonify({
        'success': True,
        'areas': areas
    })