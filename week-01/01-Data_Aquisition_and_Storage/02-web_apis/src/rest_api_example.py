import requests
import json

# The book we want to find more information about
book_title = "A Light in the Attic"

# 1. Define the API endpoint and the query parameters
#    The 'q' parameter is for the query string.
base_url = "https://www.googleapis.com/books/v1/volumes"
params = {"q": book_title}

# 2. Make the GET request to the API
print(f"Searching for '{book_title}'...")
response = requests.get(base_url, params=params)

# 3. Check for a successful response and parse the JSON
if response.status_code == 200:
    data = response.json()
    
    # Let's look at the first book found
    if 'items' in data and len(data['items']) > 0:
        first_book = data['items'][0]['volumeInfo']
        
        print("\n--- Book Found! ---")
        print(f"Title: {first_book.get('title')}")
        # The 'get' method is used to safely access keys that might not exist
        print(f"Authors: {first_book.get('authors', ['N/A'])}")
        print(f"Published Date: {first_book.get('publishedDate', 'N/A')}")
        print(f"Page Count: {first_book.get('pageCount', 'N/A')}")
    else:
        print("No books found with that title.")
else:
    print(f"Error making request: Status code {response.status_code}")
