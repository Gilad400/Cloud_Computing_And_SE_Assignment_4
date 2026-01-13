"""
Populate database with test data for query job

This script populates the pet store databases with the same data
used in the pytest tests, preparing for the query job execution.
"""

import requests
import sys


# Base URLs for services
PET_STORE1_URL = "http://localhost:5001"
PET_STORE2_URL = "http://localhost:5002"

# Test data definitions
PET_TYPE1 = {"type": "Golden Retriever"}
PET_TYPE2 = {"type": "Australian Shepherd"}
PET_TYPE3 = {"type": "Abyssinian"}
PET_TYPE4 = {"type": "bulldog"}

# Pet data
PET1_TYPE1 = {"name": "Lander", "birthdate": "14-05-2020"}
PET2_TYPE1 = {"name": "Lanky"}
PET3_TYPE1 = {"name": "Shelly", "birthdate": "07-07-2019"}
PET4_TYPE2 = {"name": "Felicity", "birthdate": "27-11-2011"}  # Fixed: DD-MM-YYYY
PET5_TYPE3 = {"name": "Muscles"}
PET6_TYPE3 = {"name": "Junior"}
PET7_TYPE4 = {"name": "Lazy", "birthdate": "08-07-2018"}
PET8_TYPE4 = {"name": "Lemon", "birthdate": "27-03-2020"}  # Fixed: DD-MM-YYYY


def post_pet_type(store_url, pet_type):
    """POST a pet type to a store and return the ID"""
    response = requests.post(
        f"{store_url}/pet-types",
        json=pet_type,
        headers={"Content-Type": "application/json"}
    )
    if response.status_code == 201:
        return response.json()["id"]
    else:
        print(f"Error posting pet type to {store_url}: {response.status_code}")
        return None


def post_pet(store_url, pet_type_id, pet_data):
    """POST a pet to a pet type"""
    response = requests.post(
        f"{store_url}/pet-types/{pet_type_id}/pets",
        json=pet_data,
        headers={"Content-Type": "application/json"}
    )
    if response.status_code != 201:
        print(f"Error posting pet to {store_url}: {response.status_code}")
        return False
    return True


def main():
    """Populate the database with test data"""
    print("Populating database with test data...")
    
    # POST pet types to store 1
    print("Posting pet types to store 1...")
    id_1 = post_pet_type(PET_STORE1_URL, PET_TYPE1)
    id_2 = post_pet_type(PET_STORE1_URL, PET_TYPE2)
    id_3 = post_pet_type(PET_STORE1_URL, PET_TYPE3)
    
    # POST pet types to store 2
    print("Posting pet types to store 2...")
    id_4 = post_pet_type(PET_STORE2_URL, PET_TYPE1)
    id_5 = post_pet_type(PET_STORE2_URL, PET_TYPE2)
    id_6 = post_pet_type(PET_STORE2_URL, PET_TYPE4)
    
    if not all([id_1, id_2, id_3, id_4, id_5, id_6]):
        print("Error: Failed to create all pet types")
        sys.exit(1)
    
    print(f"Created pet types with IDs: {id_1}, {id_2}, {id_3}, {id_4}, {id_5}, {id_6}")
    
    # POST pets to store 1
    print("Posting pets to store 1...")
    post_pet(PET_STORE1_URL, id_1, PET1_TYPE1)
    post_pet(PET_STORE1_URL, id_1, PET2_TYPE1)
    post_pet(PET_STORE1_URL, id_3, PET5_TYPE3)
    post_pet(PET_STORE1_URL, id_3, PET6_TYPE3)
    
    # POST pets to store 2
    print("Posting pets to store 2...")
    post_pet(PET_STORE2_URL, id_4, PET3_TYPE1)
    post_pet(PET_STORE2_URL, id_5, PET4_TYPE2)
    post_pet(PET_STORE2_URL, id_6, PET7_TYPE4)
    post_pet(PET_STORE2_URL, id_6, PET8_TYPE4)
    
    print("Database population completed successfully!")


if __name__ == "__main__":
    main()

