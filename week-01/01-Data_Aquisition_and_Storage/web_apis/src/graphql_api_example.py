import requests
import json

# 1. Define the single GraphQL endpoint
url = "https://countries.trevorblades.com/"

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
print("Querying GraphQL API for Switzerland...")
response = requests.post(url, json={'query': graphql_query})

# 4. Check for success and print the data
if response.status_code == 200:
    data = response.json()
    # json.dumps is used to "pretty-print" the JSON response
    print("\n--- Country Found! ---")
    print(json.dumps(data, indent=2))
else:
    print(f"Error making request: Status code {response.status_code}")

