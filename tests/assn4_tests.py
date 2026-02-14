"""
Assignment 4 Pytest Tests for Pet Store Application

This module contains all the required pytest tests for validating
the Pet Store application as specified in Assignment #4.
"""

import requests
import pytest


# Base URLs for services
PET_STORE1_URL = "http://localhost:5001"
PET_STORE2_URL = "http://localhost:5002"
PET_ORDER_URL = "http://localhost:5003"

# Test data definitions as specified in the assignment
PET_TYPE1 = {"type": "Golden Retriever"}
PET_TYPE1_VAL = {
    "type": "Golden Retriever",
    "family": "Canidae",
    "genus": "Canis",
    "attributes": [],
    "lifespan": 12
}

PET_TYPE2 = {"type": "Australian Shepherd"}
PET_TYPE2_VAL = {
    "type": "Australian Shepherd",
    "family": "Canidae",
    "genus": "Canis",
    "attributes": ["Loyal", "outgoing", "and", "friendly"],
    "lifespan": 15
}

PET_TYPE3 = {"type": "Abyssinian"}
PET_TYPE3_VAL = {
    "type": "Abyssinian",
    "family": "Felidae",
    "genus": "Felis",
    "attributes": ["Intelligent", "and", "curious"],
    "lifespan": 13
}

PET_TYPE4 = {"type": "bulldog"}
PET_TYPE4_VAL = {
    "type": "bulldog",
    "family": "Canidae",
    "genus": "Canis",
    "attributes": ["Gentle", "calm", "and", "affectionate"],
    "lifespan": None
}

# Pet data
PET1_TYPE1 = {"name": "Lander", "birthdate": "14-05-2020"}
PET2_TYPE1 = {"name": "Lanky"}
PET3_TYPE1 = {"name": "Shelly", "birthdate": "07-07-2019"}
PET4_TYPE2 = {"name": "Felicity", "birthdate": "27-11-2011"}  # Fixed: DD-MM-YYYY
PET5_TYPE3 = {"name": "Muscles"}
PET6_TYPE3 = {"name": "Junior"}
PET7_TYPE4 = {"name": "Lazy", "birthdate": "07-08-2018"}
PET8_TYPE4 = {"name": "Lemon", "birthdate": "27-03-2020"}  # Fixed: DD-MM-YYYY

# Global variables to store IDs returned from POST requests
pet_type_ids = {}


def test_post_pet_type1_to_store1():
    """Test 1: POST PET_TYPE1 to pet-store #1"""
    response = requests.post(
        f"{PET_STORE1_URL}/pet-types",
        json=PET_TYPE1,
        headers={"Content-Type": "application/json"}
    )
    
    assert response.status_code == 201, f"Expected 201, got {response.status_code}"
    
    data = response.json()
    assert "id" in data, "Response should contain 'id' field"
    assert data["type"] == PET_TYPE1_VAL["type"]
    assert data["family"] == PET_TYPE1_VAL["family"]
    assert data["genus"] == PET_TYPE1_VAL["genus"]
    
    pet_type_ids["id_1"] = data["id"]


def test_post_pet_type2_to_store1():
    """Test 1: POST PET_TYPE2 to pet-store #1"""
    response = requests.post(
        f"{PET_STORE1_URL}/pet-types",
        json=PET_TYPE2,
        headers={"Content-Type": "application/json"}
    )
    
    assert response.status_code == 201, f"Expected 201, got {response.status_code}"
    
    data = response.json()
    assert "id" in data, "Response should contain 'id' field"
    assert data["type"] == PET_TYPE2_VAL["type"]
    assert data["family"] == PET_TYPE2_VAL["family"]
    assert data["genus"] == PET_TYPE2_VAL["genus"]
    
    pet_type_ids["id_2"] = data["id"]


def test_post_pet_type3_to_store1():
    """Test 1: POST PET_TYPE3 to pet-store #1"""
    response = requests.post(
        f"{PET_STORE1_URL}/pet-types",
        json=PET_TYPE3,
        headers={"Content-Type": "application/json"}
    )
    
    assert response.status_code == 201, f"Expected 201, got {response.status_code}"
    
    data = response.json()
    assert "id" in data, "Response should contain 'id' field"
    assert data["type"] == PET_TYPE3_VAL["type"]
    assert data["family"] == PET_TYPE3_VAL["family"]
    assert data["genus"] == PET_TYPE3_VAL["genus"]
    
    pet_type_ids["id_3"] = data["id"]


def test_post_pet_type1_to_store2():
    """Test 2: POST PET_TYPE1 to pet-store #2"""
    response = requests.post(
        f"{PET_STORE2_URL}/pet-types",
        json=PET_TYPE1,
        headers={"Content-Type": "application/json"}
    )
    
    assert response.status_code == 201, f"Expected 201, got {response.status_code}"
    
    data = response.json()
    assert "id" in data, "Response should contain 'id' field"
    assert data["type"] == PET_TYPE1_VAL["type"]
    assert data["family"] == PET_TYPE1_VAL["family"]
    assert data["genus"] == PET_TYPE1_VAL["genus"]
    
    pet_type_ids["id_4"] = data["id"]


def test_post_pet_type2_to_store2():
    """Test 2: POST PET_TYPE2 to pet-store #2"""
    response = requests.post(
        f"{PET_STORE2_URL}/pet-types",
        json=PET_TYPE2,
        headers={"Content-Type": "application/json"}
    )
    
    assert response.status_code == 201, f"Expected 201, got {response.status_code}"
    
    data = response.json()
    assert "id" in data, "Response should contain 'id' field"
    assert data["type"] == PET_TYPE2_VAL["type"]
    assert data["family"] == PET_TYPE2_VAL["family"]
    assert data["genus"] == PET_TYPE2_VAL["genus"]
    
    pet_type_ids["id_5"] = data["id"]


def test_post_pet_type4_to_store2():
    """Test 2: POST PET_TYPE4 to pet-store #2"""
    response = requests.post(
        f"{PET_STORE2_URL}/pet-types",
        json=PET_TYPE4,
        headers={"Content-Type": "application/json"}
    )
    
    assert response.status_code == 201, f"Expected 201, got {response.status_code}"
    
    data = response.json()
    assert "id" in data, "Response should contain 'id' field"
    assert data["type"] == PET_TYPE4_VAL["type"]
    assert data["family"] == PET_TYPE4_VAL["family"]
    assert data["genus"] == PET_TYPE4_VAL["genus"]
    
    pet_type_ids["id_6"] = data["id"]


def test_all_ids_unique():
    """Test 1 & 2: Verify all returned IDs are unique within each store"""
    # IDs from store #1 (id_1, id_2, id_3)
    store1_ids = [pet_type_ids["id_1"], pet_type_ids["id_2"], pet_type_ids["id_3"]]
    assert len(store1_ids) == len(set(store1_ids)), "Store #1 IDs should be unique"
    
    # IDs from store #2 (id_4, id_5, id_6)
    store2_ids = [pet_type_ids["id_4"], pet_type_ids["id_5"], pet_type_ids["id_6"]]
    assert len(store2_ids) == len(set(store2_ids)), "Store #2 IDs should be unique"


def test_post_pets_to_store1_type1():
    """Test 3: POST 2 pets to pet-store #1 for PET_TYPE1"""
    id_1 = pet_type_ids["id_1"]
    
    # POST PET1_TYPE1
    response1 = requests.post(
        f"{PET_STORE1_URL}/pet-types/{id_1}/pets",
        json=PET1_TYPE1,
        headers={"Content-Type": "application/json"}
    )
    assert response1.status_code == 201, f"Expected 201, got {response1.status_code}"
    
    # POST PET2_TYPE1
    response2 = requests.post(
        f"{PET_STORE1_URL}/pet-types/{id_1}/pets",
        json=PET2_TYPE1,
        headers={"Content-Type": "application/json"}
    )
    assert response2.status_code == 201, f"Expected 201, got {response2.status_code}"


def test_post_pets_to_store1_type3():
    """Test 4: POST 2 pets to pet-store #1 for PET_TYPE3"""
    id_3 = pet_type_ids["id_3"]
    
    # POST PET5_TYPE3
    response1 = requests.post(
        f"{PET_STORE1_URL}/pet-types/{id_3}/pets",
        json=PET5_TYPE3,
        headers={"Content-Type": "application/json"}
    )
    assert response1.status_code == 201, f"Expected 201, got {response1.status_code}"
    
    # POST PET6_TYPE3
    response2 = requests.post(
        f"{PET_STORE1_URL}/pet-types/{id_3}/pets",
        json=PET6_TYPE3,
        headers={"Content-Type": "application/json"}
    )
    assert response2.status_code == 201, f"Expected 201, got {response2.status_code}"


def test_post_pet_to_store2_type1():
    """Test 5: POST 1 pet to pet-store #2 for PET_TYPE1"""
    id_4 = pet_type_ids["id_4"]
    
    response = requests.post(
        f"{PET_STORE2_URL}/pet-types/{id_4}/pets",
        json=PET3_TYPE1,
        headers={"Content-Type": "application/json"}
    )
    assert response.status_code == 201, f"Expected 201, got {response.status_code}"


def test_post_pet_to_store2_type2():
    """Test 6: POST 1 pet to pet-store #2 for PET_TYPE2"""
    id_5 = pet_type_ids["id_5"]
    
    response = requests.post(
        f"{PET_STORE2_URL}/pet-types/{id_5}/pets",
        json=PET4_TYPE2,
        headers={"Content-Type": "application/json"}
    )
    assert response.status_code == 201, f"Expected 201, got {response.status_code}"


def test_post_pets_to_store2_type4():
    """Test 7: POST 2 pets to pet-store #2 for PET_TYPE4"""
    id_6 = pet_type_ids["id_6"]
    
    # POST PET7_TYPE4
    response1 = requests.post(
        f"{PET_STORE2_URL}/pet-types/{id_6}/pets",
        json=PET7_TYPE4,
        headers={"Content-Type": "application/json"}
    )
    assert response1.status_code == 201, f"Expected 201, got {response1.status_code}"
    
    # POST PET8_TYPE4
    response2 = requests.post(
        f"{PET_STORE2_URL}/pet-types/{id_6}/pets",
        json=PET8_TYPE4,
        headers={"Content-Type": "application/json"}
    )
    assert response2.status_code == 201, f"Expected 201, got {response2.status_code}"


def test_get_pet_type2_from_store1():
    """Test 8: GET /pet-types/{id2} from pet-store #1"""
    id_2 = pet_type_ids["id_2"]
    
    response = requests.get(f"{PET_STORE1_URL}/pet-types/{id_2}")
    
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    
    data = response.json()
    assert data["type"] == PET_TYPE2_VAL["type"]
    assert data["family"] == PET_TYPE2_VAL["family"]
    assert data["genus"] == PET_TYPE2_VAL["genus"]
    assert data["attributes"] == PET_TYPE2_VAL["attributes"]
    assert data["lifespan"] == PET_TYPE2_VAL["lifespan"]


def test_get_pets_for_type4_from_store2():
    """Test 9: GET /pet-types/{id6}/pets from pet-store #2"""
    id_6 = pet_type_ids["id_6"]
    
    response = requests.get(f"{PET_STORE2_URL}/pet-types/{id_6}/pets")
    
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    # assert response.status_code == 404, f"Expected 200, got {response.status_code}"
    
    data = response.json()
    assert isinstance(data, list), "Response should be a list"
    assert len(data) == 2, "Should return 2 pets"
    
    # Check that the returned pets match PET7_TYPE4 and PET8_TYPE4
    pet_names = [pet["name"] for pet in data]
    assert PET7_TYPE4["name"].lower() in pet_names
    assert PET8_TYPE4["name"].lower() in pet_names
    
    # Verify pet data fields
    for pet in data:
        assert "name" in pet
        assert "birthdate" in pet
        if pet["name"] == PET7_TYPE4["name"].lower():
            assert pet["birthdate"] == PET7_TYPE4["birthdate"]
        elif pet["name"] == PET8_TYPE4["name"].lower():
            assert pet["birthdate"] == PET8_TYPE4["birthdate"]





# - Tester test file -

# import pytest
# import requests
# import json

# # Base URLs for the pet store instances
# PET_STORE_1_URL = "http://localhost:5001"
# PET_STORE_2_URL = "http://localhost:5002"
# PET_ORDER_URL = "http://localhost:5003"

# # Pet Type Payloads
# PET_TYPE1 = {
#     "type": "Golden Retriever"
# }

# PET_TYPE2 = {
#     "type": "Australian Shepherd"
# }

# PET_TYPE3 = {
#     "type": "Abyssinian"
# }

# PET_TYPE4 = {
#     "type": "bulldog"
# }

# # Expected Pet Type Values
# PET_TYPE1_VAL = {
#     "type": "Golden Retriever",
#     "family": "Canidae",
#     "genus": "Canis",
#     "attributes": [],
#     "lifespan": 12
# }

# PET_TYPE2_VAL = {
#     "type": "Australian Shepherd",
#     "family": "Canidae",
#     "genus": "Canis",
#     "attributes": ["Loyal", "outgoing", "and", "friendly"],
#     "lifespan": 15
# }

# PET_TYPE3_VAL = {
#     "type": "Abyssinian",
#     "family": "Felidae",
#     "genus": "Felis",
#     "attributes": ["Intelligent", "and", "curious"],
#     "lifespan": 13
# }

# PET_TYPE4_VAL = {
#     "type": "bulldog",
#     "family": "Canidae",
#     "genus": "Canis",
#     "attributes": ["Gentle", "calm", "and", "affectionate"],
#     "lifespan": None
# }

# # Pet Payloads
# PET1_TYPE1 = {
#     "name": "Lander",
#     "birthdate": "14-05-2020"
# }

# PET2_TYPE1 = {
#     "name": "Lanky"
# }

# PET3_TYPE1 = {
#     "name": "Shelly",
#     "birthdate": "07-07-2019"
# }

# PET4_TYPE2 = {
#     "name": "Felicity",
#     "birthdate": "27-11-2011"
# }

# PET5_TYPE3 = {
#     "name": "Muscles"
# }

# PET6_TYPE3 = {
#     "name": "Junior"
# }

# PET7_TYPE4 = {
#     "name": "Lazy",
#     "birthdate": "07-08-2018"
# }

# PET8_TYPE4 = {
#     "name": "Lemon",
#     "birthdate": "27-03-2020"
# }

# # Global variables to store IDs
# pet_type_ids = {}


# class TestPetStoreSetup:
#     """Test 1-2: POST pet-types to both stores and verify unique IDs and correct values"""
    
#     def test_01_post_pet_types_to_store1(self):
#         """Test 1: POST 3 pet-types to pet-store #1 (PET_TYPE1, PET_TYPE2, PET_TYPE3)"""
#         global pet_type_ids
        
#         # POST PET_TYPE1
#         response1 = requests.post(f"{PET_STORE_1_URL}/pet-types", json=PET_TYPE1)
#         assert response1.status_code == 201, f"Expected 201, got {response1.status_code}"
#         data1 = response1.json()
#         id_1 = data1["id"]
#         assert data1["family"] == PET_TYPE1_VAL["family"]
#         assert data1["genus"] == PET_TYPE1_VAL["genus"]
        
#         # POST PET_TYPE2
#         response2 = requests.post(f"{PET_STORE_1_URL}/pet-types", json=PET_TYPE2)
#         assert response2.status_code == 201, f"Expected 201, got {response2.status_code}"
#         data2 = response2.json()
#         id_2 = data2["id"]
#         assert data2["family"] == PET_TYPE2_VAL["family"]
#         assert data2["genus"] == PET_TYPE2_VAL["genus"]
        
#         # POST PET_TYPE3
#         response3 = requests.post(f"{PET_STORE_1_URL}/pet-types", json=PET_TYPE3)
#         assert response3.status_code == 201, f"Expected 201, got {response3.status_code}"
#         data3 = response3.json()
#         id_3 = data3["id"]
#         assert data3["family"] == PET_TYPE3_VAL["family"]
#         assert data3["genus"] == PET_TYPE3_VAL["genus"]
        
#         # Verify all IDs are unique
#         assert id_1 != id_2 != id_3, "IDs must be unique"
        
#         # Store IDs for later tests
#         pet_type_ids['id_1'] = id_1
#         pet_type_ids['id_2'] = id_2
#         pet_type_ids['id_3'] = id_3
    
#     def test_02_post_pet_types_to_store2(self):
#         """Test 2: POST 3 pet-types to pet-store #2 (PET_TYPE1, PET_TYPE2, PET_TYPE4)"""
#         global pet_type_ids
        
#         # POST PET_TYPE1
#         response4 = requests.post(f"{PET_STORE_2_URL}/pet-types", json=PET_TYPE1)
#         assert response4.status_code == 201, f"Expected 201, got {response4.status_code}"
#         data4 = response4.json()
#         id_4 = data4["id"]
#         assert data4["family"] == PET_TYPE1_VAL["family"]
#         assert data4["genus"] == PET_TYPE1_VAL["genus"]
        
#         # POST PET_TYPE2
#         response5 = requests.post(f"{PET_STORE_2_URL}/pet-types", json=PET_TYPE2)
#         assert response5.status_code == 201, f"Expected 201, got {response5.status_code}"
#         data5 = response5.json()
#         id_5 = data5["id"]
#         assert data5["family"] == PET_TYPE2_VAL["family"]
#         assert data5["genus"] == PET_TYPE2_VAL["genus"]
        
#         # POST PET_TYPE4
#         response6 = requests.post(f"{PET_STORE_2_URL}/pet-types", json=PET_TYPE4)
#         assert response6.status_code == 201, f"Expected 201, got {response6.status_code}"
#         data6 = response6.json()
#         id_6 = data6["id"]
#         assert data6["family"] == PET_TYPE4_VAL["family"]
#         assert data6["genus"] == PET_TYPE4_VAL["genus"]
        
#         # Verify all IDs are unique
#         assert id_4 != id_5 != id_6, "IDs must be unique"
        
#         # Store IDs for later tests
#         pet_type_ids['id_4'] = id_4
#         pet_type_ids['id_5'] = id_5
#         pet_type_ids['id_6'] = id_6


# class TestPetCreation:
#     """Tests 3-7: POST pets to various pet-types"""
    
#     def test_03_post_pets_to_store1_type1(self):
#         """Test 3: POST 2 pets to pet-store #1 pet-type id_1 (Golden Retriever)"""
#         id_1 = pet_type_ids['id_1']
        
#         # POST PET1_TYPE1
#         response1 = requests.post(f"{PET_STORE_1_URL}/pet-types/{id_1}/pets", json=PET1_TYPE1)
#         assert response1.status_code == 201, f"Expected 201, got {response1.status_code}"
        
#         # POST PET2_TYPE1
#         response2 = requests.post(f"{PET_STORE_1_URL}/pet-types/{id_1}/pets", json=PET2_TYPE1)
#         assert response2.status_code == 201, f"Expected 201, got {response2.status_code}"
    
#     def test_04_post_pets_to_store1_type3(self):
#         """Test 4: POST 2 pets to pet-store #1 pet-type id_3 (Abyssinian)"""
#         id_3 = pet_type_ids['id_3']
        
#         # POST PET5_TYPE3
#         response1 = requests.post(f"{PET_STORE_1_URL}/pet-types/{id_3}/pets", json=PET5_TYPE3)
#         assert response1.status_code == 201, f"Expected 201, got {response1.status_code}"
        
#         # POST PET6_TYPE3
#         response2 = requests.post(f"{PET_STORE_1_URL}/pet-types/{id_3}/pets", json=PET6_TYPE3)
#         assert response2.status_code == 201, f"Expected 201, got {response2.status_code}"
    
#     def test_05_post_pet_to_store2_type1(self):
#         """Test 5: POST 1 pet to pet-store #2 pet-type id_4 (Golden Retriever)"""
#         id_4 = pet_type_ids['id_4']
        
#         # POST PET3_TYPE1
#         response = requests.post(f"{PET_STORE_2_URL}/pet-types/{id_4}/pets", json=PET3_TYPE1)
#         assert response.status_code == 201, f"Expected 201, got {response.status_code}"
    
#     def test_06_post_pet_to_store2_type2(self):
#         """Test 6: POST 1 pet to pet-store #2 pet-type id_5 (Australian Shepherd)"""
#         id_5 = pet_type_ids['id_5']
        
#         # POST PET4_TYPE2
#         response = requests.post(f"{PET_STORE_2_URL}/pet-types/{id_5}/pets", json=PET4_TYPE2)
#         assert response.status_code == 201, f"Expected 201, got {response.status_code}"
    
#     def test_07_post_pets_to_store2_type4(self):
#         """Test 7: POST 2 pets to pet-store #2 pet-type id_6 (bulldog)"""
#         id_6 = pet_type_ids['id_6']
        
#         # POST PET7_TYPE4
#         response1 = requests.post(f"{PET_STORE_2_URL}/pet-types/{id_6}/pets", json=PET7_TYPE4)
#         assert response1.status_code == 201, f"Expected 201, got {response1.status_code}"
        
#         # POST PET8_TYPE4
#         response2 = requests.post(f"{PET_STORE_2_URL}/pet-types/{id_6}/pets", json=PET8_TYPE4)
#         assert response2.status_code == 201, f"Expected 201, got {response2.status_code}"


# class TestPetTypeRetrieval:
#     """Test 8: GET specific pet-type and verify all fields"""
    
#     def test_08_get_pet_type_from_store1(self):
#         """Test 8: GET /pet-types/{id_2} from pet-store #1 and verify all fields"""
#         id_2 = pet_type_ids['id_2']
        
#         response = requests.get(f"{PET_STORE_1_URL}/pet-types/{id_2}")
#         assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        
#         data = response.json()
        
#         # Verify all fields match PET_TYPE2_VAL
#         assert data["type"].lower() == PET_TYPE2_VAL["type"].lower()
#         assert data["family"] == PET_TYPE2_VAL["family"]
#         assert data["genus"] == PET_TYPE2_VAL["genus"]
#         assert data["attributes"] == PET_TYPE2_VAL["attributes"]
#         assert data["lifespan"] == PET_TYPE2_VAL["lifespan"]


# class TestPetsRetrieval:
#     """Test 9: GET pets of a specific type and verify"""
    
#     def test_09_get_pets_from_store2_type4(self):
#         """Test 9: GET /pet-types/{id_6}/pets from pet-store #2 and verify pets"""
#         id_6 = pet_type_ids['id_6']
        
#         response = requests.get(f"{PET_STORE_2_URL}/pet-types/{id_6}/pets")
#         assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        
#         data = response.json()
        
#         # Verify it's an array with 2 pets
#         assert isinstance(data, list), "Response should be an array"
#         assert len(data) == 2, f"Expected 2 pets, got {len(data)}"
        
#         # Extract pet names
#         pet_names = [pet["name"].lower() for pet in data]
        
#         # Verify both pets are present
#         assert "lazy" in pet_names, "Pet 'Lazy' should be in the list"
#         assert "lemon" in pet_names, "Pet 'Lemon' should be in the list"
        
#         # Verify birthdates
#         for pet in data:
#             if pet["name"].lower() == "lazy":
#                 assert pet["birthdate"] == PET7_TYPE4["birthdate"]
#             elif pet["name"].lower() == "lemon":
#                 assert pet["birthdate"] == PET8_TYPE4["birthdate"]


# class TestQueryStrings:
#     """Test 10: Additional test for query string functionality"""
    
#     def test_10_query_by_family(self):
#         """Test 10: GET /pet-types with query string family=Canidae from both stores"""
        
#         # Query store 1
#         response1 = requests.get(f"{PET_STORE_1_URL}/pet-types?family=Canidae")
#         assert response1.status_code == 200, f"Expected 200, got {response1.status_code}"
#         data1 = response1.json()
#         assert isinstance(data1, list), "Response should be an array"
#         # Store 1 should have 2 Canidae types (Golden Retriever, Australian Shepherd)
#         assert len(data1) == 2, f"Expected 2 Canidae types in store 1, got {len(data1)}"
        
#         # Query store 2
#         response2 = requests.get(f"{PET_STORE_2_URL}/pet-types?family=Canidae")
#         assert response2.status_code == 200, f"Expected 200, got {response2.status_code}"
#         data2 = response2.json()
#         assert isinstance(data2, list), "Response should be an array"
#         # Store 2 should have 3 Canidae types (Golden Retriever, Australian Shepherd, bulldog)
#         assert len(data2) == 3, f"Expected 3 Canidae types in store 2, got {len(data2)}"

