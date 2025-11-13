#!/usr/bin/env python3
"""
Aircraft Job Card Database Web Application
Flask-based web interface
"""
from flask import Flask, render_template, request, jsonify, send_file
import os
import sys
from database import JobCardDatabase
from models import JobCard
import traceback

app = Flask(__name__)
app.config['SECRET_KEY'] = 'aircraft-jobcard-secret-key'

# Database file path
DB_PATH = '/vercel/sandbox/uploads/Aircraft_Jobcard_Database.xlsm'

# Global database instance
db = None


def init_database():
    """Initialize database"""
    global db
    try:
        if not os.path.exists(DB_PATH):
            raise FileNotFoundError(f"Database file not found at {DB_PATH}")
        
        db = JobCardDatabase(DB_PATH)
        print(f"Database loaded: {len(db.jobcards)} job cards, {len(db.aircraft)} aircraft")
        return True
    except Exception as e:
        print(f"Error initializing database: {e}")
        traceback.print_exc()
        return False


@app.route('/')
def index():
    """Main page"""
    return render_template('index.html')


@app.route('/api/jobcards', methods=['GET'])
def get_jobcards():
    """Get all job cards with optional filters"""
    try:
        check_type = request.args.get('check_type', '')
        aircraft = request.args.get('aircraft', '')
        search = request.args.get('search', '')
        
        jobcards = db.get_all_jobcards()
        
        # Apply filters
        if check_type and check_type != 'All':
            jobcards = [jc for jc in jobcards if jc.check_type == check_type]
        
        if aircraft and aircraft != 'All':
            jobcards = [jc for jc in jobcards if jc.get_aircraft_status(aircraft) is not None]
        
        if search:
            search = search.lower()
            jobcards = [jc for jc in jobcards if (
                search in jc.card_number.lower() or
                search in jc.task_reference.lower() or
                search in jc.task_title.lower() or
                search in jc.description.lower() or
                search in jc.zone.lower()
            )]
        
        # Convert to dict
        result = [jc.to_dict() for jc in jobcards]
        
        return jsonify({
            'success': True,
            'data': result,
            'total': len(result)
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/jobcards/<int:index>', methods=['GET'])
def get_jobcard(index):
    """Get single job card by index"""
    try:
        jobcards = db.get_all_jobcards()
        if 0 <= index < len(jobcards):
            return jsonify({
                'success': True,
                'data': jobcards[index].to_dict()
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Job card not found'
            }), 404
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/jobcards', methods=['POST'])
def add_jobcard():
    """Add new job card"""
    try:
        data = request.json
        jobcard = JobCard.from_dict(data)
        db.add_jobcard(jobcard)
        
        return jsonify({
            'success': True,
            'message': 'Job card added successfully'
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/jobcards/<int:index>', methods=['PUT'])
def update_jobcard(index):
    """Update job card"""
    try:
        data = request.json
        jobcard = JobCard.from_dict(data)
        db.update_jobcard(index, jobcard)
        
        return jsonify({
            'success': True,
            'message': 'Job card updated successfully'
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/jobcards/<int:index>', methods=['DELETE'])
def delete_jobcard(index):
    """Delete job card"""
    try:
        db.delete_jobcard(index)
        
        return jsonify({
            'success': True,
            'message': 'Job card deleted successfully'
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/save', methods=['POST'])
def save_database():
    """Save changes to database"""
    try:
        db.save_data()
        
        return jsonify({
            'success': True,
            'message': 'Changes saved successfully'
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/metadata', methods=['GET'])
def get_metadata():
    """Get metadata (check types, aircraft)"""
    try:
        return jsonify({
            'success': True,
            'data': {
                'check_types': db.get_check_types(),
                'aircraft': db.get_aircraft_regs(),
                'total_jobcards': len(db.get_all_jobcards())
            }
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/export', methods=['POST'])
def export_data():
    """Export filtered data to Excel"""
    try:
        data = request.json
        indices = data.get('indices', [])
        
        jobcards = db.get_all_jobcards()
        filtered_jobcards = [jobcards[i] for i in indices if 0 <= i < len(jobcards)]
        
        output_path = '/tmp/exported_jobcards.xlsx'
        db.export_filtered_data(filtered_jobcards, output_path)
        
        return send_file(output_path, as_attachment=True, download_name='jobcards_export.xlsx')
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


if __name__ == '__main__':
    if init_database():
        print("Starting Flask application...")
        app.run(host='0.0.0.0', port=5000, debug=True)
    else:
        print("Failed to initialize database")
        sys.exit(1)
