from flask import Flask, request, jsonify
from flask_cors import CORS  # <-- ADD THIS
import google.generativeai as genai
import os
from dotenv import load_dotenv

app = Flask(__name__)
CORS(app)  # <-- ALLOW ALL ORIGINS (during dev)

# --- Gemini Configuration ---
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-2.0-flash")

# --- Helper Functions ---
def classify_format(input_str: str) -> str:
    prompt = f"""
You are an AI assistant that receives a raw text.
Classify the format of the message into ONLY one of the following:
- JSON
- Email 
- PDF
- Unknown

... [omitted for brevity]
"""
    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        print(f"Error classifying format: {e}")
        return "Unknown"

def classify_intent(input_str: str) -> str:
    prompt = f"""
You are an AI assistant that receives raw business communication text.
Classify the **intent** of the message into ONLY one of the following:
- Complaint
- RFQ
- Invoice
- Order Placement

... [omitted for brevity]
"""
    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        print(f"Error classifying intent: {e}")
        return "Unknown"

def classify_input(input_str: str):
    input_type = classify_format(input_str)
    intent = classify_intent(input_str)
    return {
        "format": input_type,
        "intent": intent
    }

@app.route("/classify", methods=['POST'])
def classify_route():
    input_str = request.get_data(as_text=True)
    result = classify_input(input_str)
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True, port=5004)
