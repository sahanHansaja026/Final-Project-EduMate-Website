from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_message = data.get("message", "").lower()

    # Very basic ML-like response logic (can replace with real ML model later)
    if "hello" in user_message:
        reply = "Hi there! How can I help you with your learning?"
    elif "assignment" in user_message:
        reply = "Please upload your assignment under the module section."
    elif "video" in user_message:
        reply = "You can find lecture videos in your module content."
    else:
        reply = "I'm here to assist with your learning management questions!"

    return jsonify({"reply": reply})

if __name__ == '__main__':
    app.run(port=5000, debug=True)
