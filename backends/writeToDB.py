from pymongo import MongoClient
from flask import Flask, request, jsonify
from datetime import datetime

app = Flask(__name__)

# MongoDB Configuration
MONGO_URI = "mongodb://localhost:27017/"  # Replace with your MongoDB URI if different
DATABASE_NAME = "MIA"

@app.route('/memory', methods=['POST'])
def place_order():
    try:
        data = request.get_json()

        # Extract collection name and order data
        collection_name = data.get('order_id')
        # if not collection_name:
        #     collection_name = data.get('oollection')
        
        if not collection_name:
            return jsonify({'error': 'order id is required'}), 400
        
        # Create a copy of the data and remove the 'collection' key
        order_data = data.copy()
        order_data.pop('order_id')
        # order_data.pop('collection')

        # Connect to MongoDB
        client = MongoClient(MONGO_URI)
        db = client[DATABASE_NAME]
        collection = db[collection_name]

        # Convert date strings to datetime objects (if they exist and are valid)
        date_fields = ["requested_delivery_date", "submitted_at"]
        for field in date_fields:
            if field in order_data and isinstance(order_data[field], str):
                try:
                    order_data[field] = datetime.fromisoformat(order_data[field].rstrip("Z"))  # Handle potential "Z" timezone suffix
                except ValueError:
                    return jsonify({'error': f'Invalid date format for {field}.  Use ISO format.'}), 400


        # Insert the order data into the specified collection
        result = collection.insert_one(order_data)

        return jsonify({'message': 'written', 'inserted_id': str(result.inserted_id)}), 201

    except Exception as e:
        print(f"An error occurred: {e}")
        return jsonify({'error': str(e)}), 500
    finally:
        if 'client' in locals():
            client.close()

if __name__ == '__main__':
    app.run(debug=True,port='5003')