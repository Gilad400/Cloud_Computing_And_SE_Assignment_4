from flask import Flask, request, jsonify, make_response
import json
import pymongo
import requests
import os
import uuid
import re
from datetime import datetime

# Initialize Flask app
app = Flask(__name__)

MONGO_HOST = os.getenv('MONGO_HOST')
MONGO_PORT = int(os.getenv('MONGO_PORT'))

# Get the store ID from environment variable (1 or 2)
STORE_ID = os.getenv('STORE_ID')
DB_NAME = f'petstore{STORE_ID}'

# Connect to MongoDB
client = pymongo.MongoClient(f'mongodb://{MONGO_HOST}:{MONGO_PORT}/')
db = client[DB_NAME]

# Collections
pet_types_collection = db['pet_types']
pets_collection = db['pets']
pictures_collection = db['pictures']

# API Ninjas configuration
NINJA_API_KEY = os.getenv('NINJA_API_KEY')
NINJA_API_URL = 'https://api.api-ninjas.com/v1/animals'

def generate_unique_id():
    """
    Generate a unique string ID for pet types using MongoDB's auto-increment pattern.
    Returns a string representation of an incrementing integer.
    """
    # Find the highest existing ID
    highest = pet_types_collection.find_one(sort=[("_id", pymongo.DESCENDING)])
    if highest:
        return str(int(highest['_id']) + 1)
    return "1"

def is_pet_name_exists(pet_type_id, pet_name_input):
    """
    Check if a pet exists (case-insensitive).
    
    Args:
        pet_type_id (str): The pet type ID
        pet_name_input (str): The pet name from URL/input (any case)
        
    Returns:
        bool: True if pet exists, False otherwise
    """
    pet = pets_collection.find_one({
        'pet_type_id': pet_type_id,
        'name': pet_name_input.lower()
    })
    return pet is not None

def parse_lifespan(lifespan_str):
    """
    Parse lifespan string from API response and extract numeric value.
    
    Args:
        lifespan_str (str): Lifespan string like "up to 41 years" or "12 years"
        
    Returns:
        int or None: Numeric lifespan value or None if parsing fails
    """
    if not lifespan_str:
        return None
    
    # Extract numbers from the string using regex
    numbers = re.findall(r'\d+', lifespan_str)
    if numbers:
        return min(int(num) for num in numbers)
    
    return None

def parse_attributes(attribute_str):
    """
    Parse attribute string into array of words, removing punctuation.
    
    Args:
        attribute_str (str): Attribute string like "Very active and intelligent"
        
    Returns:
        list: Array of words from the string
    """
    if not attribute_str:
        return []
    
    # Remove punctuation and split into words
    words = re.findall(r'\b[a-zA-Z]+\b', attribute_str)

    return words

def get_animal_type_data_from_ninjaApi(animal_type):
    """
    Fetch animal data from API Ninjas Animals API.
    
    Args:
        animal_type (str): The type of animal to search for
        
    Returns:
        dict or None: Animal data or None if not found/error occurred
    """
    try:
        headers = {'X-Api-Key': NINJA_API_KEY}
        params = {'name': animal_type}
        
        response = requests.get(NINJA_API_URL, headers=headers, params=params)
        
        if response.status_code != 200:
            raise Exception(str(response.status_code))
            
        animals_data = response.json()
        
        if not animals_data:
            return None
            
        for animal in animals_data:
            if animal.get('name', '').lower() == animal_type.lower():
                return animal
                
        return None
        
    except Exception as e:
        print(f"Error fetching animal data: {e}")
        return None

def download_picture(picture_url):
    """
    Download picture from URL and store it in MongoDB.
    
    Args:
        picture_url (str): URL of the picture to download
        
    Returns:
        str or None: Generated filename or None if failed
    """
    try:
        response = requests.get(picture_url, timeout=30)
        if response.status_code == 200:
            filename = f"{uuid.uuid4().hex}.jpg"
            
            # Store picture data in MongoDB
            pictures_collection.insert_one({
                '_id': filename,
                'data': response.content
            })
            
            return filename
    except Exception as e:
        print(f"Error downloading picture: {e}")
    
    return None

def is_validate_date(date_string):
    """
    Validate date string in DD-MM-YYYY format.
    
    Args:
        date_string (str): Date string to validate
        
    Returns:
        bool: True if valid, False otherwise
    """
    try:
        datetime.strptime(date_string, '%d-%m-%Y')
        return True
    except ValueError:
        return False

def compare_dates(date1, date2):
    """
    Compare two date strings in DD-MM-YYYY format.
    
    Args:
        date1 (str): First date
        date2 (str): Second date
        
    Returns:
        int: -1 if date1 < date2, 0 if equal, 1 if date1 > date2
    """
    try:
        d1 = datetime.strptime(date1, '%d-%m-%Y')
        d2 = datetime.strptime(date2, '%d-%m-%Y')
        
        if d1 < d2:
            return -1
        elif d1 > d2:
            return 1
        else:
            return 0
    except ValueError:
        return 0

# Error response helpers
def error_400():
    """Return standard 400 Bad Request response."""
    return jsonify({"error": "Malformed data"}), 400

def error_404():
    """Return standard 404 Not Found response."""
    return jsonify({"error": "Not found"}), 404

def error_415():
    """Return standard 415 Unsupported Media Type response."""
    return jsonify({"error": "Expected application/json media type"}), 415

def error_500(message="Internal server error"):
    """Return standard 500 Internal Server Error response."""
    return jsonify({"server error": "API response code " + message}), 500


@app.route('/pet-types', methods=['GET'])
def get_pet_types():
    """
    Handle GET requests to /pet-types endpoint.
    
    Returns a list of all pet types with optional query filtering.
    Supported filters: type, family, genus, lifespan, id, hasAttribute
    """
    try:
        # Get query parameters for filtering
        type_filter = request.args.get('type')
        family_filter = request.args.get('family') 
        genus_filter = request.args.get('genus')
        lifespan_filter = request.args.get('lifespan')
        id_filter = request.args.get('id')
        has_attribute = request.args.get('hasAttribute')
        
        # Start with all pet types from MongoDB
        result = list(pet_types_collection.find())
	
	# Convert MongoDB _id to id for each document
        for item in result:
            item['id'] = item.pop('_id')
        
        # Apply filters
        if type_filter:
            result = [pt for pt in result if pt['type'].lower() == type_filter.lower()]
            
        if family_filter:
            result = [pt for pt in result if pt['family'].lower() == family_filter.lower()]
            
        if genus_filter:
            result = [pt for pt in result if pt['genus'].lower() == genus_filter.lower()]
            
        if lifespan_filter:
            try:
                lifespan_val = int(lifespan_filter)
                result = [pt for pt in result if pt['lifespan'] == lifespan_val]
            except ValueError:
                return error_400()
                
        if id_filter:
            result = [pt for pt in result if pt['id'] == id_filter]
            
        if has_attribute:
            result = [pt for pt in result 
                        if any(attr.lower() == has_attribute.lower() for attr in pt['attributes'])]
        
        return jsonify(result), 200
        
    except Exception as e:
        return error_400() 
    
@app.route('/pet-types', methods=['POST'])
def create_pet_type():
    """
    Handle POST requests to /pet-types endpoint.
    
    Creates a new pet type using data from API Ninjas Animals API.
    Requires JSON payload with 'type' field.
    Returns the created pet type with taxonomical information.
    """
    try:
        if request.content_type != 'application/json':
            return error_415()
        
        data = request.get_json()
        if not data or 'type' not in data:
            return error_400()
        
        animal_type = data['type']
        
        # Check if this pet type already exists (case-insensitive)
        existing = pet_types_collection.find_one({
            'type': {'$regex': f'^{animal_type}$', '$options': 'i'}
        })
        if existing:
            return error_400()
        
        try:
            animal_data = get_animal_type_data_from_ninjaApi(animal_type)
            if not animal_data:
                return error_400()
        except Exception as e:
            return error_500(str(e))
        
        pet_type_id = generate_unique_id()

        attributes = []
        characteristics = animal_data.get('characteristics', {})
    
        if 'temperament' in characteristics and characteristics['temperament']:
            attributes = parse_attributes(characteristics['temperament'])
        elif 'group_behavior' in characteristics and characteristics['group_behavior']:
            attributes = parse_attributes(characteristics['group_behavior'])
        
        lifespan = None
        if 'lifespan' in characteristics and characteristics['lifespan']:
            lifespan = parse_lifespan(characteristics['lifespan'])
        
        taxonomy = animal_data.get('taxonomy', {})
        family = taxonomy.get('family', '')
        genus = taxonomy.get('genus', '')
        
        # Create pet type object
        pet_type = {
            '_id': pet_type_id,
            'type': animal_type,
            'family': family,
            'genus': genus,
            'attributes': attributes,
            'lifespan': lifespan,
            'pets': []
        }
        
        # Insert into MongoDB
        pet_types_collection.insert_one(pet_type)
        
        # Prepare response (convert _id to id)
        response_data = pet_type.copy()
        response_data['id'] = response_data.pop('_id')
        
        return jsonify(response_data), 201
        
    except Exception as e:
        return error_400()

@app.route('/pet-types/<pet_type_id>', methods=['GET'])
def get_pet_type(pet_type_id):
    """
    Handle GET requests to /pet-types/{id} endpoint.
    
    Returns a specific pet type by ID.
    
    Args:
        pet_type_id (str): The ID of the pet type to retrieve
        
    Returns:
        JSON response with pet type data or 404 if not found
    """
    try:
        pet_type = pet_types_collection.find_one({'_id': pet_type_id})
        
        if not pet_type:
            return error_404()
        
        # Convert _id to id for response
        pet_type['id'] = pet_type.pop('_id')
        
        return jsonify(pet_type), 200
        
    except Exception as e:
        return error_500(str(e))


@app.route('/pet-types/<pet_type_id>', methods=['DELETE'])
def delete_pet_type(pet_type_id):
    """
    Handle DELETE requests to /pet-types/{id} endpoint.
    
    Deletes a specific pet type by ID (only if no pets exist for this type).
    
    Args:
        pet_type_id (str): The ID of the pet type to delete
        
    Returns:
        204 No Content on success, 400 if pets exist, 404 if not found
    """
    try:
        pet_type = pet_types_collection.find_one({'_id': pet_type_id})
        
        if not pet_type:
            return error_404()
        
        # Check if pet type has any pets
        if pet_type['pets']:
            return error_400()
        
        # Delete the pet type
        pet_types_collection.delete_one({'_id': pet_type_id})
        
        return '', 204
        
    except Exception as e:
        return error_500(str(e))

@app.route('/pet-types/<pet_type_id>/pets', methods=['GET'])
def get_pets(pet_type_id):
    """
    Handle GET requests to /pet-types/{id}/pets endpoint.
    
    Returns a list of pets for a specific pet type with optional date filtering.
    Supports query parameters: birthdateGT, birthdateLT
    
    Args:
        pet_type_id (str): The ID of the pet type
        
    Returns:
        JSON array of pets or 404 if pet type not found
    """
    # Check if pet type exists
    pet_type = pet_types_collection.find_one({'_id': pet_type_id})
    if not pet_type:
        return error_404()
    
    try:
        # Build MongoDB query
        query = {'pet_type_id': pet_type_id}
        
        birthdate_gt = request.args.get('birthdateGT')
        birthdate_lt = request.args.get('birthdateLT')
        
        # Validate date formats
        if birthdate_gt and not is_validate_date(birthdate_gt):
            return error_400()
        if birthdate_lt and not is_validate_date(birthdate_lt):
            return error_400()
        
        # Fetch all pets for this type
        pets_list = list(pets_collection.find(query))
        
        # Apply date filtering if provided
        if birthdate_gt or birthdate_lt:
            filtered_pets = []
            for pet in pets_list:
                if pet['birthdate'] == 'NA':
                    continue
                
                include_pet = True
                
                if birthdate_gt and compare_dates(pet['birthdate'], birthdate_gt) <= 0:
                    include_pet = False
                
                if birthdate_lt and compare_dates(pet['birthdate'], birthdate_lt) >= 0:
                    include_pet = False
                
                if include_pet:
                    filtered_pets.append(pet)
            
            pets_list = filtered_pets
        
        # Remove MongoDB _id and pet_type_id from response
        for pet in pets_list:
            pet.pop('_id', None)
            pet.pop('pet_type_id', None)
        return jsonify(pets_list), 200
        
    except Exception as e:
        return error_400()


@app.route('/pet-types/<pet_type_id>/pets', methods=['POST'])
def create_pet(pet_type_id):
    """
    Handle POST requests to /pet-types/{id}/pets endpoint.
    
    Creates a new pet for a specific pet type.
    
    Args:
        pet_type_id (str): The ID of the pet type to add the pet to
        
    Returns:
        JSON response with created pet data or appropriate error
    """
    # Check if pet type exists
    pet_type = pet_types_collection.find_one({'_id': pet_type_id})
    if not pet_type:
        return error_404()
    
    try:
        if request.content_type != 'application/json':
            return error_415()
        
        data = request.get_json()
        if not data or 'name' not in data:
            return error_400()
        
        pet_name_lower = data['name'].lower()
        
        if is_pet_name_exists(pet_type_id, pet_name_lower):
            return error_400()
        
        # Process and validate birthdate
        birthdate = data.get('birthdate', 'NA')
        if birthdate != 'NA':
            if not isinstance(birthdate, str) or not is_validate_date(birthdate):
                return error_400()
        
        # Process picture URL if provided
        picture_filename = 'NA'
        picture_url = data.get('picture-url')
        if picture_url:
            picture_filename = download_picture(picture_url)
            if not picture_filename:
                picture_filename = 'NA'  
        
        pet = {
            'name': pet_name_lower,
            'birthdate': birthdate,
            'picture': picture_filename,
            'pet_type_id': pet_type_id
        }
        
        # Insert into MongoDB
        pets_collection.insert_one(pet)
        
        # Update pet type's pets list
        pet_types_collection.update_one(
            {'_id': pet_type_id},
            {'$push': {'pets': pet_name_lower}}
        )
        
        # Prepare response (remove MongoDB fields)
        response_data = {
            'name': pet['name'],
            'birthdate': pet['birthdate'],
            'picture': pet['picture']
        }
        
        return jsonify(response_data), 201
        
    except Exception as e:
        return error_400()

@app.route('/pet-types/<pet_type_id>/pets/<pet_name>', methods=['GET'])
def get_pet(pet_type_id, pet_name):
    """
    Handle GET requests to /pet-types/{id}/pets/{name} endpoint.
    
    Returns a specific pet by name within a pet type.
    
    Args:
        pet_type_id (str): The ID of the pet type
        pet_name (str): The name of the pet to retrieve
        
    Returns:
        JSON response with pet data or 404 if not found
    """
    # Check if pet type exists
    pet_type = pet_types_collection.find_one({'_id': pet_type_id})
    if not pet_type:
        return error_404()
    
    pet_name_lower = pet_name.lower() 
    
    if not is_pet_name_exists(pet_type_id, pet_name_lower):
        return error_404()
    
    try:
        pet = pets_collection.find_one({
            'pet_type_id': pet_type_id,
            'name': pet_name_lower
        })
        
        if not pet:
            return error_404()
        
        # Prepare response (remove MongoDB fields)
        response_data = {
            'name': pet['name'],
            'birthdate': pet['birthdate'],
            'picture': pet['picture']
        }
        
        return jsonify(response_data), 200
        
    except Exception as e:
        return error_500(str(e))


@app.route('/pet-types/<pet_type_id>/pets/<pet_name>', methods=['DELETE'])
def delete_pet(pet_type_id, pet_name):
    """
    Handle DELETE requests to /pet-types/{id}/pets/{name} endpoint.
    
    Deletes a specific pet by name and removes associated picture.
    
    Args:
        pet_type_id (str): The ID of the pet type
        pet_name (str): The name of the pet to delete
        
    Returns:
        204 No Content on success or 404 if not found
    """
    # Check if pet type exists
    pet_type = pet_types_collection.find_one({'_id': pet_type_id})
    if not pet_type:
        return error_404()
    
    pet_name_lower = pet_name.lower()
    
    if not is_pet_name_exists(pet_type_id, pet_name_lower):
        return error_404()
    
    try:
        # Get pet data before deletion
        pet = pets_collection.find_one({
            'pet_type_id': pet_type_id,
            'name': pet_name_lower
        })
        
        # Delete associated picture if exists
        if pet and pet['picture'] != 'NA':
            pictures_collection.delete_one({'_id': pet['picture']})
        
        # Delete pet from MongoDB
        pets_collection.delete_one({
            'pet_type_id': pet_type_id,
            'name': pet_name_lower
        })
        
        # Remove pet name from pet type's pets list
        pet_types_collection.update_one(
            {'_id': pet_type_id},
            {'$pull': {'pets': pet_name_lower}}
        )
        
        return '', 204
        
    except Exception as e:
        return error_500(str(e))


@app.route('/pet-types/<pet_type_id>/pets/<pet_name>', methods=['PUT'])
def update_pet(pet_type_id, pet_name):
    """
    Handle PUT requests to /pet-types/{id}/pets/{name} endpoint.
    
    Updates a specific pet's information including birthdate and picture.
    
    Args:
        pet_type_id (str): The ID of the pet type
        pet_name (str): The name of the pet to update
        
    Returns:
        JSON response with updated pet data or appropriate error
    """
    # Check if pet type exists
    pet_type = pet_types_collection.find_one({'_id': pet_type_id})
    if not pet_type:
        return error_404()
    
    pet_name_lower = pet_name.lower()

    if not is_pet_name_exists(pet_type_id, pet_name_lower):
        return error_404()
    
    try:
        if request.content_type != 'application/json':
            return error_415()
        
        data = request.get_json()
        if not data or 'name' not in data:
            return error_400()
        
        # Name in payload must match URL parameter
        payload_name_lower = data['name'].lower()
        if payload_name_lower != pet_name_lower:
            return error_400()
        
        # Get current pet data
        current_pet = pets_collection.find_one({
            'pet_type_id': pet_type_id,
            'name': pet_name_lower
        })
        
        if not current_pet:
            return error_404()
        
        # Process and validate birthdate update
        birthdate = data.get('birthdate', 'NA')
        if birthdate != 'NA':
            if not isinstance(birthdate, str) or not is_validate_date(birthdate):
                return error_400()
        
        # Process picture update
        picture_filename = 'NA'
        picture_url = data.get('picture-url')
        if picture_url:
            new_filename = download_picture(picture_url)
            if new_filename:
                # Delete old picture if exists
                if picture_filename != 'NA':
                    pictures_collection.delete_one({'_id': picture_filename})
                picture_filename = new_filename
        else:
            # No picture-url provided, delete old picture
            if current_pet['picture'] != 'NA':
                pictures_collection.delete_one({'_id': current_pet['picture']})
        
        # Update pet in MongoDB
        updated_pet = {
            'name': pet_name_lower,
            'birthdate': birthdate,
            'picture': picture_filename,
            'pet_type_id': pet_type_id
        }
        
        pets_collection.update_one(
            {'pet_type_id': pet_type_id, 'name': pet_name_lower},
            {'$set': updated_pet}
        )
        
        # Prepare response
        response_data = {
            'name': updated_pet['name'],
            'birthdate': updated_pet['birthdate'],
            'picture': updated_pet['picture']
        }
        
        return jsonify(response_data), 200
        
    except Exception as e:
        return error_400()

@app.route('/pictures/<filename>', methods=['GET'])
def get_picture(filename):
    """
    Handle requests to /pictures/{file-name} endpoint.
    
    GET: Return picture file by filename
    """
    try:
        picture = pictures_collection.find_one({'_id': filename})
        
        if not picture:
            return error_404()
        
        image_data = picture['data']
        
        # Determine content type
        content_type = 'image/jpeg'
        if filename.lower().endswith('.png'):
            content_type = 'image/png'
        
        response = make_response(image_data)
        response.headers['Content-Type'] = content_type
        
        return response
        
    except Exception as e:
        return error_500(str(e))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
