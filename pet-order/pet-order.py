from flask import Flask, request, jsonify
import pymongo
import os
import requests
import random

# Initialize Flask app
app = Flask(__name__)

# MongoDB configuration
MONGO_HOST = os.getenv('MONGO_HOST')
MONGO_PORT = int(os.getenv('MONGO_PORT'))
DB_NAME = 'petorder'

# Connect to MongoDB
client = pymongo.MongoClient(f'mongodb://{MONGO_HOST}:{MONGO_PORT}/')
db = client[DB_NAME]

# Collection for transactions
transactions_collection = db['transactions']

# Pet store service URLs (using Docker Compose service names)
PET_STORE1_URL = 'http://pet-store1:8000'
PET_STORE2_URL = 'http://pet-store2:8000'

# Owner password for transaction access
OWNER_PASSWORD = 'LovesPetsL2M3n4'

def generate_purchase_id():
    """
    Generate a unique purchase ID.
    Uses MongoDB's auto-increment pattern.
    """
    highest = transactions_collection.find_one(sort=[("purchase-id", pymongo.DESCENDING)])
    if highest:
        return str(int(highest['purchase-id']) + 1)
    return "1"

def get_pet_type_id(store_url, pet_type_name):
    """
    Get the ID of a pet type by querying the pet store.
    
    Args:
        store_url (str): Base URL of the pet store service
        pet_type_name (str): Name of the pet type
        
    Returns:
        str or None: Pet type ID if found, None otherwise
    """
    try:
        response = requests.get(f'{store_url}/pet-types')
        if response.status_code == 200:
            pet_types = response.json()
            for pt in pet_types:
                if pt['type'].lower() == pet_type_name.lower():
                    return pt['id']
        return None
    except Exception as e:
        return None

def get_pets_of_type(store_url, pet_type_id):
    """
    Get all pets of a specific type from a store.
    
    Args:
        store_url (str): Base URL of the pet store service
        pet_type_id (str): ID of the pet type
        
    Returns:
        list: List of pets or empty list if error
    """
    try:
        response = requests.get(f'{store_url}/pet-types/{pet_type_id}/pets')
        if response.status_code == 200:
            return response.json()
        return []
    except Exception as e:
        return []

def is_pet_deleted(store_url, pet_type_id, pet_name):
    """
    Delete a pet from the store.
    
    Args:
        store_url (str): Base URL of the pet store service
        pet_type_id (str): ID of the pet type
        pet_name (str): Name of the pet to delete
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        response = requests.delete(f'{store_url}/pet-types/{pet_type_id}/pets/{pet_name}')
        return response.status_code == 204
    except Exception as e:
        return False

def find_and_choose_pet(pet_type_name, store_number=None, pet_name=None):
    """
    Find and choose a pet based on criteria.
    
    Args:
        pet_type_name (str): Type of pet to find
        store_number (int, optional): Specific store (1 or 2)
        pet_name (str, optional): Specific pet name
        
    Returns:
        tuple: (store_number, pet_type_id, chosen_pet_name) or (None, None, None) if not found
    """
    stores = {
        1: PET_STORE1_URL,
        2: PET_STORE2_URL
    }
    
    # Case 1: Store and pet name are specified
    if store_number and pet_name:
        store_url = stores.get(store_number)
        if not store_url:
            return None, None, None
        
        pet_type_id = get_pet_type_id(store_url, pet_type_name)
        if not pet_type_id:
            return None, None, None
        
        pets = get_pets_of_type(store_url, pet_type_id)
        for pet in pets:
            if pet['name'].lower() == pet_name.lower():
                return store_number, pet_type_id, pet['name']
        return None, None, None
    
    # Case 2: Only store is specified
    if store_number:
        store_url = stores.get(store_number)
        if not store_url:
            return None, None, None
        
        pet_type_id = get_pet_type_id(store_url, pet_type_name)
        if not pet_type_id:
            return None, None, None
        
        pets = get_pets_of_type(store_url, pet_type_id)
        if pets:
            chosen_pet = random.choice(pets)
            return store_number, pet_type_id, chosen_pet['name']
        return None, None, None
    
    # Case 3: No store specified - search both stores
    available_pets = []
    for store_num, store_url in stores.items():
        pet_type_id = get_pet_type_id(store_url, pet_type_name)
        if pet_type_id:
            pets = get_pets_of_type(store_url, pet_type_id)
            for pet in pets:
                available_pets.append((store_num, pet_type_id, pet['name']))
    
    if available_pets:
        chosen = random.choice(available_pets)
        return chosen
    
    return None, None, None

def error_400(message="Malformed data"):
    """Return standard 400 Bad Request response."""
    return jsonify({"error": message}), 400

def error_401():
    """Return standard 401 Unauthorized response."""
    return jsonify({"error": "Unauthorized"}), 401

def error_415():
    """Return standard 415 Unsupported Media Type response."""
    return jsonify({"error": "Expected application/json media type"}), 415

@app.route('/purchases', methods=['POST'])
def create_purchase():
    """
    Handle POST requests to /purchases endpoint.
    
    Process a pet purchase request.
    """
    try:
        if request.content_type != 'application/json':
            return error_415()
        
        data = request.get_json()
        
        # Validate required fields
        if not data or 'purchaser' not in data or 'pet-type' not in data:
            return error_400()
        
        purchaser = data['purchaser']
        pet_type = data['pet-type']
        store = data.get('store')
        pet_name = data.get('pet-name')
        
        # Validate store number if provided
        if store is not None:
            if store not in [1, 2]:
                return error_400()
        
        # pet-name can only be provided if store is provided
        if pet_name and not store:
            return error_400()
        
        # Find and choose a pet
        chosen_store, pet_type_id, chosen_pet_name = find_and_choose_pet(
            pet_type, store, pet_name
        )
        
        # Check if a pet was found
        if not chosen_store or not pet_type_id or not chosen_pet_name:
            return error_400("No pet of this type is available")
        
        # Delete the pet from the store
        stores = {1: PET_STORE1_URL, 2: PET_STORE2_URL}
        store_url = stores[chosen_store]
        
        if not is_pet_deleted(store_url, pet_type_id, chosen_pet_name):
            return error_400("Failed to complete purchase")
        
        # Generate purchase ID
        purchase_id = generate_purchase_id()
        
        # Create transaction record
        transaction = {
            'purchaser': purchaser,
            'pet-type': pet_type,
            'store': chosen_store,
            'purchase-id': purchase_id
        }
        
        # Store transaction in MongoDB
        transactions_collection.insert_one(transaction)
        
        # Create purchase response (includes pet-name)
        purchase_response = {
            'purchaser': purchaser,
            'pet-type': pet_type,
            'store': chosen_store,
            'pet-name': chosen_pet_name,
            'purchase-id': purchase_id
        }
        
        return jsonify(purchase_response), 201
        
    except Exception as e:
        return error_400()

@app.route('/transactions', methods=['GET'])
def get_transactions():
    """
    Handle GET requests to /transactions endpoint.
    
    Returns all transactions (owner access only).
    Supports query string filtering.
    """
    try:
        # Check authorization
        owner_pc = request.headers.get('OwnerPC')
        if owner_pc != OWNER_PASSWORD:
            return error_401()
        
        # Build MongoDB query based on query parameters
        query = {}
        
        store_filter = request.args.get('store')
        if store_filter:
            try:
                query['store'] = int(store_filter)
            except ValueError:
                return jsonify([]), 200
        
        pet_type_filter = request.args.get('pet-type')
        if pet_type_filter:
            query['pet-type'] = {'$regex': f'^{pet_type_filter}$', '$options': 'i'}
        
        purchaser_filter = request.args.get('purchaser')
        if purchaser_filter:
            query['purchaser'] = {'$regex': f'^{purchaser_filter}$', '$options': 'i'}
        
        purchase_id_filter = request.args.get('purchase-id')
        if purchase_id_filter:
            query['purchase-id'] = purchase_id_filter
        
        # Fetch transactions from MongoDB
        transactions = list(transactions_collection.find(query))
        
        # Remove MongoDB _id from response
        for transaction in transactions:
            transaction.pop('_id', None)
        
        return jsonify(transactions), 200
        
    except Exception as e:
        return jsonify([]), 200

# @app.route('/kill', methods=['GET'])
# def kill_container():
#     """
#     Handle GET requests to /kill endpoint.
    
#     Kills the container for testing restart functionality.
#     """
#     os._exit(1)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)