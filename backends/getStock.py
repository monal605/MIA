from pymongo import MongoClient
from flask import Flask, jsonify

app = Flask(__name__)

# MongoDB Configuration (Consider moving to a config file or environment variables)
MONGO_URI = "mongodb://localhost:27017/"
DATABASE_NAME = "MIA"
COLLECTION_NAME = "goods"

def get_all_goods():
    """Retrieves all goods from MongoDB."""
    try:
        client = MongoClient(MONGO_URI)
        db = client[DATABASE_NAME]
        collection = db[COLLECTION_NAME]
        goods = list(collection.find())
        for good in goods:
            if "_id" in good:
                good["_id"] = str(good["_id"])
        return goods
    except Exception as e:
        print(f"An error occurred: {e}")
        return []
    finally:
        if 'client' in locals():
            client.close()

@app.route('/goods', methods=['GET'])
def get_goods_route():
    goods = get_all_goods()
    return jsonify(goods)  # Return as JSON

if __name__ == '__main__':
    app.run(debug=True,port=5001) # Development server.  Use a production WSGI server for deployment.