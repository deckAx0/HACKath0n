import os
from flask import Flask, request
from dotenv import load_dotenv

load_dotenv()

# read 'SECRET_KEY' from environment variable
secret_key = os.getenv('SECRET_KEY')

app = Flask(__name__)
app.config['MAX_FILE_SIZE'] = 50 * 1024 * 1024  # 50 MB
app.config['UPLOAD_FOLDER'] = 'temp_uploads'

if __name__ == '__main__':    
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)