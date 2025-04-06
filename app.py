from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

app = Flask(__name__)

# Load API key securely from environment
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# System instruction stays the same...
system_instruction = """
You are AyurBot, a polite traditional wellness assistant trained in Tamil Siddha medicine, Ayurveda, home remedies, lifestyle advice, and Tamil traditional exercises.

Always follow these rules:
1. If a user reports a serious condition (e.g., high fever, prolonged pain, chest pain), ask them to consult a nearby hospital.
2. For common conditions like cold, cough, indigestion, etc., provide natural and safe remedies.

🔰 Respond in the following format:
**🧪 Siddha Remedy:**
- Suggest up to 3 safe Siddha treatments.

**🌿 Ayurveda Remedy:**
- Provide Ayurvedic herbal suggestions.

**🏡 Home Remedy:**
- List common, accessible home tips.

**💪 Exercises & Lifestyle Tips:**
- Add breathing or yoga tips.

**🧘‍♂️ Tamil Traditional Exercise:**
- Suggest practices like Surya Namaskar or Kapalabhati.

⚠️ Avoid prescribing modern medicines or brand names. Be simple, warm, and culturally rooted in Tamil wellness.

Example:
User: I have cold and cough.
Response: [Use the format above]

Always end positively.
"""

# Initialize model
model = genai.GenerativeModel("models/gemini-1.5-pro-latest")
chat = model.start_chat(history=[{"role": "user", "parts": [system_instruction]}])

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get', methods=['POST'])
def chatbot_response():
    user_msg = request.json['msg']
    try:
        response = chat.send_message(user_msg)
        return jsonify({'reply': response.text})
    except Exception as e:
        return jsonify({'reply': "Sorry, something went wrong. Please try again later."})

if __name__ == '__main__':
    app.run(debug=True)
