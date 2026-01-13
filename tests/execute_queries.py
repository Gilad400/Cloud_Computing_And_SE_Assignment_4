"""
Execute queries from query.txt and write results to response.txt

This script reads the query.txt file, executes the queries, and writes
the results to response.txt in the format specified in the assignment.
"""

import requests
import json
import sys
import os


# Base URLs for services
PET_STORE1_URL = "http://localhost:5001"
PET_STORE2_URL = "http://localhost:5002"
PET_ORDER_URL = "http://localhost:5003"


def execute_query(query_string):
    """
    Execute a query entry and return the formatted result.
    
    Args:
        query_string (str): Query in format "query: <pet-store-num>,<query-string>;"
        
    Returns:
        str: Formatted response
    """
    try:
        # Parse the query string
        # Format: "query: <pet-store-num>,<query-string>;"
        query_string = query_string.strip()
        if not query_string.startswith("query:"):
            return None
        
        # Remove "query:" prefix and trailing semicolon
        query_content = query_string[6:].strip()
        if query_content.endswith(";"):
            query_content = query_content[:-1].strip()
        
        # Split by comma to get store number and query parameters
        parts = query_content.split(",", 1)
        if len(parts) != 2:
            return f"400\nNONE\n;"
        
        store_num = parts[0].strip()
        query_params = parts[1].strip()
        
        # Determine store URL
        if store_num == "1":
            store_url = PET_STORE1_URL
        elif store_num == "2":
            store_url = PET_STORE2_URL
        else:
            return f"400\nNONE\n;"
        
        # Execute GET request
        url = f"{store_url}/pet-types?{query_params}"
        response = requests.get(url)
        
        # Format response
        if response.status_code == 200:
            payload = json.dumps(response.json(), indent=2)
            return f"{response.status_code}\n{payload}\n;"
        else:
            return f"{response.status_code}\nNONE\n;"
    
    except Exception as e:
        print(f"Error executing query: {e}")
        return f"400\nNONE\n;"


def execute_purchase(purchase_string):
    """
    Execute a purchase entry and return the formatted result.
    
    Args:
        purchase_string (str): Purchase in format "purchase: <json-purchase>;"
        
    Returns:
        str: Formatted response
    """
    try:
        # Parse the purchase string
        # Format: "purchase: <json-purchase>;"
        purchase_string = purchase_string.strip()
        if not purchase_string.startswith("purchase:"):
            return None
        
        # Remove "purchase:" prefix
        json_content = purchase_string[9:].strip()
        
        # Find the JSON content (everything before the last semicolon)
        if json_content.endswith(";"):
            json_content = json_content[:-1].strip()
        
        # Parse JSON
        purchase_data = json.loads(json_content)
        
        # Execute POST request
        response = requests.post(
            f"{PET_ORDER_URL}/purchases",
            json=purchase_data,
            headers={"Content-Type": "application/json"}
        )
        
        # Format response
        if response.status_code == 201:
            payload = json.dumps(response.json(), indent=2)
            return f"{response.status_code}\n{payload}\n;"
        else:
            return f"{response.status_code}\nNONE\n;"
    
    except Exception as e:
        print(f"Error executing purchase: {e}")
        return f"400\nNONE\n;"


def main():
    """Main function to execute queries from query.txt"""
    query_file = "query.txt"
    response_file = "response.txt"
    
    # Check if query.txt exists
    if not os.path.exists(query_file):
        print(f"Error: {query_file} not found")
        # Create empty response file
        with open(response_file, "w") as f:
            f.write("")
        return
    
    # Read query.txt
    with open(query_file, "r") as f:
        content = f.read()
    
    # Split by semicolons to get individual entries
    entries = content.split(";")
    
    results = []
    
    for entry in entries:
        entry = entry.strip()
        if not entry:
            continue
        
        # Add back the semicolon for parsing
        entry = entry + ";"
        
        # Determine entry type and execute
        if entry.strip().startswith("query:"):
            result = execute_query(entry)
            if result:
                results.append(result)
        elif entry.strip().startswith("purchase:"):
            result = execute_purchase(entry)
            if result:
                results.append(result)
    
    # Write results to response.txt
    with open(response_file, "w") as f:
        f.write("\n".join(results))
    
    print(f"Query execution completed. Results written to {response_file}")


if __name__ == "__main__":
    main()

