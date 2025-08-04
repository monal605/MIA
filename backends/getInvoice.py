from flask import Flask, request, jsonify
from pymongo import MongoClient
import requests
import google.generativeai as genai
import os
from dotenv import load_dotenv

app = Flask(__name__)

# --- MongoDB Configuration ---
MONGO_URI = "mongodb://localhost:27017/"  # Replace if needed
DATABASE_NAME = "MIA"

# --- Gemini Configuration ---
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-2.0-flash")

# --- Helper Functions ---
def get_order_details_from_db(collection_name):
    """Retrieves an order placement document from the specified collection."""
    try:
        client = MongoClient(MONGO_URI)
        db = client[DATABASE_NAME]
        collection = db[collection_name]
        order = collection.find_one({"type": "Order Placement"}) 
        
        if order == None:
            order = collection.find_one({"type": "order placement"})
         #Finds the first document where type is order placement
        if order:
            order["_id"] = str(order["_id"])  # Convert ObjectId to string
        return order
    except Exception as e:
        print(f"Error retrieving order details: {e}")
        return None
    finally:
        if 'client' in locals():
            client.close()

def get_goods_data():
    """Calls the /goods API and returns the data."""
    try:
        response = requests.get("http://127.0.0.1:5001/goods")
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error calling /goods API: {e}")
        return None

def generate_total_bill(order_details, goods_data):
    """Generates the total bill using the Gemini model."""
    if not order_details or not goods_data:
        return "Could not retrieve necessary data to generate the bill."

    prompt = f"""
You are a billing assistant.  Here are the order details:
{order_details}

Here is the pricing information for the items (price per unit):
{goods_data}

Calculate the total bill, including all details such as customer name,
email, products (name and quantity), requested delivery date, status,
submitted date, and the complete price breakdown.  Provide a clear and
concise summary.
"""
    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        print(f"Error generating bill with Gemini: {e}")
        return "Error generating the total bill."

# --- API Endpoint ---
@app.route("/get/<collection_name>", methods=['GET'])
def process_order(collection_name):
    """
    Processes the order by retrieving data, calling the /goods API,
    and generating the total bill using Gemini.
    """
    order_details = get_order_details_from_db(collection_name)
    goods_data = get_goods_data()
    # print(collection_name)
    # print(order_details)
    # print(goods_data)
    total_bill = generate_total_bill(order_details, goods_data)

    return jsonify({"total_bill": total_bill})

# --- Main ---
if __name__ == '__main__':
    app.run(debug=True, port=5000) 