import os
import uuid
from flask import Blueprint, request, current_app, jsonify, session
from werkzeug.utils import secure_filename
from core.parser import parse_file
import magic

upload_bp = Blueprint('upload', __name__)

ALLOWED_EXTENSION = {'bin'}
DEFAULT_MAX_SIZE = 50 * 1024 * 1024

def allowed_extension(filename):
    return '.' in filename and filename.rsplit('.', 1)[-1].lower() in ALLOWED_EXTENSION

@upload_bp.route('/api/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if not allowed_extension(file.filename):
        return jsonify({'error': 'File type not allowed'}), 400
    
    max_size = current_app.config.get('MAX_FILE_SIZE', DEFAULT_MAX_SIZE)

    file.seek(0, os.SEEK_END)
    file_length = file.tell()
    file.seek(0, 0)

    if file_length > max_size:
        return jsonify({'error': f'File size exceeds maximum limit: {max_size // (1024 * 1024)} MB'}), 400
    
    file.read(2048) 
    file.seek(0)

    real_mime = magic.from_buffer(file.read(2048), mime=True)
    
    if real_mime not in ['application/octet-stream', 'application/x-binary']:
        return jsonify({'error': 'Invalid file type'}), 400

    old_file = session.get('uploaded_file')
    if old_file:
        old_path = os.path.join(current_app.config['UPLOAD_FOLDER'], secure_filename(old_file))
        if os.path.exists(old_path):
            try:
                os.remove(old_path)
            except OSError:
                pass

    unique_filename = f"{uuid.uuid4()}.bin"
    save_path = os.path.join(current_app.config['UPLOAD_FOLDER'], unique_filename)

    try:     
        os.makedirs(current_app.config['UPLOAD_FOLDER'], exist_ok=True)
        file.save(save_path)
        session['uploaded_file'] = unique_filename
    except Exception as e:
        return jsonify({'error': f'Failed to save file: {str(e)}'}), 500

    return jsonify({'message': 'File uploaded successfully'}), 200

@upload_bp.route('/api/parse', methods=['GET'])
def give_parsed_data():
    filename = session.get('uploaded_file')

    if not filename:
        return jsonify({'error': 'No file to parse'}), 400

    filename = secure_filename(filename)
    file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)

    if not os.path.exists(file_path):
        session.pop('uploaded_file', None)
        return jsonify({'error': 'File not found'}), 404

    try:
        parsed_data = parse_file(file_path)
        return jsonify({'parsed_data': parsed_data}), 200
    except Exception as e:
        return jsonify({'error': f'Failed to parse file: {str(e)}'}), 500
    finally:
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
            except OSError:
                pass
        session.pop('uploaded_file', None)
