from flask import Blueprint, request, jsonify
import os
import ollama

main = Blueprint('main', __name__)

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'pdf', 'txt', 'doc', 'docx'}

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@main.route('/api/chatbot', methods=['POST'])
def chatbot_response():
    data = request.get_json()
    user_input = data.get('userInput')

    try:
        # Use Ollama's chat method to get response from the local GGUF model
        response = ollama.chat(model='meerkat-gguf', messages=[{'role': 'user', 'content': user_input}])
        bot_response = response['message']['content']
    except ollama.ResponseError as e:
        bot_response = f"An error occurred: {e.error} (status code: {e.status_code})"
    except Exception as e:
        bot_response = f"An unexpected error occurred: {str(e)}"

    return jsonify({"response": bot_response})

@main.route('/api/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"response": "No file part in the request"}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({"response": "No file selected for uploading"}), 400

    if file and allowed_file(file.filename):
        filename = file.filename
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)
        return jsonify({"response": f"File {filename} uploaded successfully!"})
    else:
        return jsonify({"response": "File type not allowed"}), 400

