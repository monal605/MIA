from flask import Flask, request, jsonify
from pymongo import MongoClient

app = Flask(__name__)

# --- MongoDB Configuration ---
MONGO_URI = "mongodb://localhost:27017/"  # Replace with your MongoDB URI
DATABASE_NAME = "MIA"
COLLECTION_NAME = "goods"

@app.route('/update_stock', methods=['POST'])
def update_stock():
    """
    Updates the quantity_available of multiple goods in the MongoDB database.
    Expects a JSON payload where each key is the product name and the value is the quantity to subtract.
    Example: {"wireless mouse": 2, "keyboard": 1, "monitor": 3}
    """
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Invalid JSON payload"}), 400

        client = MongoClient(MONGO_URI)
        db = client[DATABASE_NAME]
        collection = db[COLLECTION_NAME]

        results = []  # Store results for each product update

        for product_name, quantity_to_subtract in data.items():
            try:
                quantity_to_subtract = int(quantity_to_subtract)  # Ensure quantity is an integer
            except ValueError:
                results.append({"product": product_name, "error": "Quantity must be an integer"})
                continue  # Skip to the next product

            # Find the good by name
            good = collection.find_one({'name': product_name})
            if not good:
                results.append({"product": product_name, "error": f"Good with name '{product_name}' not found"})
                continue  # Skip to the next product

            # Update the quantity_available
            current_quantity = good.get('quantity_available', 0)  # Default to 0 if not present
            new_quantity = current_quantity - quantity_to_subtract

            if new_quantity < 0:
                results.append({"product": product_name, "error": "Insufficient stock"})
                continue  # Skip to the next product

            result = collection.update_one(
                {'name': product_name},
                {'$set': {'quantity_available': new_quantity}}
            )

            if result.modified_count == 0:
                results.append({"product": product_name, "message": "Stock already up to date."})
            else:
                results.append({"product": product_name, "message": f"Stock updated successfully. New quantity: {new_quantity}"})

        return jsonify({"results": results}), 200  # Return all results

    except Exception as e:
        print(f"An error occurred: {e}")
        return jsonify({"error": f"An error occurred: {e}"}), 500
    finally:
        if 'client' in locals():
            client.close()

if __name__ == '__main__':
    app.run(debug=True, port=5002)