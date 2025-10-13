from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import json
from datetime import datetime

from controllers.contact_controller import contact_bp
from controllers.services_controller import services_bp
from controllers.training_controller import training_bp

app = Flask(__name__, static_folder='.', template_folder='.')
CORS(app)

app.config['SECRET_KEY'] = 'nirmaanify-secret-key-2025'
app.config['JSON_AS_ASCII'] = False

# Data file path
DATA_FILE = 'data/submissions.json'

app.register_blueprint(contact_bp, url_prefix='/api')
app.register_blueprint(services_bp, url_prefix='/api')
app.register_blueprint(training_bp, url_prefix='/api')

# Ensure data directory exists
os.makedirs('data', exist_ok=True)

# Initialize data file if it doesn't exist
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump({'contacts': [], 'services': [], 'internships': []}, f, ensure_ascii=False, indent=2)

def load_data():
    """Load existing data from JSON file"""
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return {'contacts': [], 'services': [], 'internships': []}

def get_database_stats():
    """Get statistics from JSON data"""
    data = load_data()
    return {
        'total_contacts': len(data.get('contacts', [])),
        'total_services': len(data.get('services', [])),
        'total_internships': len(data.get('internships', [])),
        'total_submissions': len(data.get('contacts', [])) + len(data.get('services', [])) + len(data.get('internships', []))
    }

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/<path:filename>')
def serve_static(filename):
    return send_from_directory('.', filename)

@app.route('/api/health')
def health_check():
    return jsonify({
        'status': 'healthy',
        'message': 'Nirmaanify API is running',
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/submissions')
def get_submissions():
    try:
        data = load_data()
        
        return jsonify({
            'success': True,
            'data': data,
            'counts': {
                'contacts': len(data.get('contacts', [])),
                'services': len(data.get('services', [])),
                'internships': len(data.get('internships', []))
            }
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/stats')
def get_stats():
    """Get statistics from JSON data"""
    try:
        stats = get_database_stats()
        return jsonify({
            'success': True,
            'stats': stats
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'success': False,
        'error': 'Endpoint not found',
        'message': 'The requested endpoint does not exist'
    }), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        'success': False,
        'error': 'Internal server error',
        'message': 'Something went wrong on our end'
    }), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') != 'production'
    
    print("🚀 Starting Nirmaanify Flask Server...")
    print(f"📱 Website will be available at: http://localhost:{port}")
    print("🔧 API endpoints available at: http://localhost:5000/api")
    print("📊 View submissions at: http://localhost:5000/api/submissions")
    print("💚 Health check at: http://localhost:5000/api/health")
    print("\n" + "="*50)
    
    app.run(
        host='0.0.0.0',
        port=port,
        debug=debug,
        threaded=True
    )


app = app
