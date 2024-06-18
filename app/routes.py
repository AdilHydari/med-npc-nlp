import logging
from flask import Flask, request, jsonify
from flask_cors import CORS

def setup_routes(app):
    CORS(app, resources={r"/api/*": {"origins": "http://localhost:3000"}})

    def generate_response(user_input):
        # Mock response generation
        responses = {
            "hello": "Hi there! How can I help you?",
            "how are you": "I'm a bot, but I'm functioning as expected!",
            "bye": "Goodbye! Have a great day!",
        }
        return responses.get(user_input.lower(), "I'm sorry, I don't understand that.")

    @app.route('/api/chatbot', methods=['POST'])
    def chatbot():
        user_input = request.json.get('userInput')
        response = generate_response(user_input)
        return jsonify(response=response)

