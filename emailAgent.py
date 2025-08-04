from flask import Flask, request, jsonify
import requests
import google.generativeai as genai
import os
from dotenv import load_dotenv

app = Flask(__name__)

# --- Gemini Configuration ---
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-2.0-flash")

# --- Routes ---

@app.route('/json/Complaint', methods=['POST'])
def complaint_route():
    """
    Handles Complaint POST requests.
    Sends the request body to http://127.0.0.1:5004/memory and returns a message.
    """
    try:
        complaint_data = request.get_json()
        if not complaint_data:
            return jsonify({"error": "Invalid JSON payload"}), 400

        # Send the complaint data to the memory endpoint
        memory_url = "http://127.0.0.1:5003/memory"
        memory_response = requests.post(memory_url, json=complaint_data)

        if memory_response.status_code == 201 or memory_response.status_code == 200:
            return jsonify({"message": "Complaint data sent to memory successfully"}), 200
        else:
            return jsonify({"error": f"Failed to send complaint data to memory: {memory_response.text}"}), 500

    except Exception as e:
        print(f"Error processing complaint: {e}")
        return jsonify({"error": f"An error occurred: {e}"}), 500

@app.route('/json/RFQ', methods=['GET'])
def rfq_route():
    """
    Handles RFQ GET requests.
    Analyzes the request body text against available stock using Gemini.
    """
    try:
        rfq_text = request.get_data(as_text=True)
        if not rfq_text:
            return jsonify({"error": "No RFQ text provided in the request body"}), 400

        # Get stock information from the goods endpoint
        goods_url = "http://127.0.0.1:5001/goods"
        goods_response = requests.get(goods_url)

        if goods_response.status_code == 200:
            stock = goods_response.json()
        else:
            return jsonify({"error": f"Failed to retrieve stock information: {goods_response.text}"}), 500

        # Analyze the RFQ against the stock using Gemini
        prompt = f"""
You are a stock availability analyst.
Here is the RFQ: {rfq_text}
Here is the available stock: {stock}
Analyze whether the RFQ is possible given the available stock.
If yes, provide a suitable message. If not, provide the reason why it is not possible.
"""
        gemini_response = model.generate_content(prompt)
        analysis_result = gemini_response.text.strip()

        return jsonify({"analysis_result": analysis_result}), 200

    except Exception as e:
        print(f"Error processing RFQ: {e}")
        return jsonify({"error": f"An error occurred: {e}"}), 500

@app.route('/json/Invoice/<collection_name>', methods=['GET'])
def invoice_route(collection_name):
    """
    Handles Invoice GET requests.
    Forwards the request to http://127.0.0.1:5000/get/<collection_name> and returns the response.
    """
    try:
        get_url = f"http://127.0.0.1:5000/get/{collection_name}"
        get_response = requests.get(get_url)

        if get_response.status_code == 200:
            return jsonify(get_response.json()), 200
        else:
            return jsonify({"error": f"Failed to retrieve invoice data: {get_response.text}"}), 500

    except Exception as e:
        print(f"Error processing invoice request: {e}")
        return jsonify({"error": f"An error occurred: {e}"}), 500

@app.route('/json/OrderPlacement', methods=['POST'])
def order_placement_route():
    """
    Handles Order Placement POST requests.
    Sends the request body to http://127.0.0.1:5003/memory and returns a message.
    """
    try:
        order_data = request.get_json()
        if not order_data:
            return jsonify({"error": "Invalid JSON payload"}), 400

        # Send the order data to the memory endpoint
        memory_url = "http://127.0.0.1:5003/memory"
        memory_response = requests.post(memory_url, json=order_data)

        if memory_response.status_code == 200 or memory_response.status_code == 201:
            return jsonify({"message": "Order placement data sent to memory successfully"}), 200
        else:
            return jsonify({"error": f"Failed to send order placement data to memory: {memory_response.text}"}), 500

    except Exception as e:
        print(f"Error processing order placement: {e}")
        return jsonify({"error": f"An error occurred: {e}"}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5005)  # Use a different port