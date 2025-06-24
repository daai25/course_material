# Tutorial: Acquiring Data with APIs

So far, we have extracted data by scraping HTML. This is effective, but it relies on the website's layout. If the layout changes, our scraper breaks. A more robust and polite way to get data is to use an **API** (Application Programming Interface).

An API is a way for computer programs to talk to each other. When a website offers an API, they are providing a structured way for you to request their data.

## Part 1: Using a REST API (Google Books)

**REST** (Representational State Transfer) is the most common style of API. Think of it like ordering from a restaurant menu. The menu has a list of specific dishes (called **endpoints**), and you make a request for one of them.

We will use the Google Books API to get more information about one of the books we scraped, "A Light in the Attic".

### Step 1: Install the `requests` library

To make API calls in Python, we use the popular `requests` library. If you don't have it, open your terminal and install it:
```bash
pip install requests
```

### Step 2: Make the API call

Create a new Python file called `api_test.py` and add the following code:
```python
import requests
import json

# The book we want to find more information about
book_title = "A Light in the Attic"

# 1. Define the API endpoint and the query parameters
#    The 'q' parameter is for the query string.
base_url = "[https://www.googleapis.com/books/v1/volumes](https://www.googleapis.com/books/v1/volumes)"
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

```
Run this script from your terminal: `python api_test.py`. You will see it fetches and prints additional details about the book, straight from Google's database!

---

## Part 2: Using a GraphQL API

**GraphQL** is a newer way to build and use APIs. The main difference is that with GraphQL, you don't have lots of different endpoints. There's usually just **one** endpoint.

Instead of a fixed menu, you give the server a detailed "shopping list" specifying exactly which data fields you want back. This can be more efficient as you don't get extra data you don't need.

We'll use a public GraphQL API for country data to see how it works.

### Step 1: Define a GraphQL Query

Our "shopping list" is called a **query**. Let's say we want to find Switzerland and get its name, capital city, and currency. The query looks like this:

```graphql
query {
  country(code: "CH") {
    name
    capital
    currency
  }
}
```
Notice how we are asking for specific fields: `name`, `capital`, and `currency`.

### Step 2: Make the API call in Python

Let's modify our `api_test.py` file to query the GraphQL API.
```python
import requests
import json

# 1. Define the single GraphQL endpoint
url = "[https://countries.trevorblades.com/](https://countries.trevorblades.com/)"

# 2. Define the GraphQL query as a multi-line string
#    We ask for the name, capital, currency, and emoji for Switzerland (CH).
graphql_query = """
query {
  country(code: "CH") {
    name
    capital
    currency
    emoji
  }
}
"""

# 3. Make a POST request, sending our query in the JSON body
print("\nQuerying GraphQL API for Switzerland...")
response = requests.post(url, json={'query': graphql_query})

# 4. Check for success and print the data
if response.status_code == 200:
    data = response.json()
    # json.dumps is used to "pretty-print" the JSON response
    print(json.dumps(data, indent=2))
else:
    print(f"Error making request: Status code {response.status_code}")
```
When you run this, you will see a response like this:
```json
{
  "data": {
    "country": {
      "name": "Switzerland",
      "capital": "Bern",
      "currency": "CHF",
      "emoji": "🇨🇭"
    }
  }
}
```
Notice that the response mirrors the shape of our query perfectly. We got *exactly* what we asked for, and nothing more. That's the power of GraphQL!

By working through these two examples, you now have hands-on experience with the two most important API styles used today.
                
