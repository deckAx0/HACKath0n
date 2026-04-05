import os
from flask import Flask
from dotenv import load_dotenv
from file_upload import upload_bp 

load_dotenv()

app = Flask(__name__)

app.secret_key = os.getenv('SECRET_KEY', 'default_secret_key') 

app.config['MAX_FILE_SIZE'] = 50 * 1024 * 1024
app.config['UPLOAD_FOLDER'] = 'temp_uploads'

app.register_blueprint(upload_bp)

if __name__ == '__main__':     
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port) # DEBUG=True should be removed in production