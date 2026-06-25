# =============================================================================
# REST_API.py
# Author  : Pavan Shetty H S
# Date    : July 2024
# Topic   : Consuming REST APIs using the requests library
# =============================================================================
#
# Notes from Pavan:
# This was my first time calling a REAL API over the internet and
# genuinely getting back live data, not test fixtures. Felt surreal --
# like the program was actually "alive" and talking to something outside
# my own machine for the first time. requests library makes this almost
# too easy compared to what I expected (vague memories of complicated
# socket programming from a networking course).
# =============================================================================

import requests
import json

print("=" * 50)
print("    REST API DEMO")
print("=" * 50)

# ---------------------
# Basic GET request
# ---------------------
print("\n[1] Basic GET request")
response = requests.get("https://jsonplaceholder.typicode.com/users/1")
print(f"  Status code: {response.status_code}")
print(f"  URL: {response.url}")

if response.status_code == 200:
    user_data = response.json()
    print(f"  Name : {user_data['name']}")
    print(f"  Email: {user_data['email']}")
    print(f"  City : {user_data['address']['city']}")
else:
    print(f"  Request failed with status {response.status_code}")

# ---------------------
# Understanding status codes -- the table I built for myself
# ---------------------
print("\n[2] HTTP Status Codes I keep referring back to")
status_codes = [
    (200, "OK", "Request succeeded"),
    (201, "Created", "Resource created successfully (POST)"),
    (400, "Bad Request", "Server couldn't understand the request"),
    (401, "Unauthorized", "Authentication required/failed"),
    (403, "Forbidden", "Authenticated, but not allowed"),
    (404, "Not Found", "Resource doesn't exist"),
    (500, "Internal Server Error", "Something broke on the server side"),
]
for code, name, meaning in status_codes:
    print(f"  {code} {name:25} - {meaning}")

# ---------------------
# GET with query parameters
# ---------------------
print("\n[3] GET with query parameters")
params = {"userId": 1}
response = requests.get("https://jsonplaceholder.typicode.com/posts", params=params)
posts = response.json()
print(f"  Found {len(posts)} posts for userId=1")
print(f"  First post title: {posts[0]['title'][:50]}...")

# ---------------------
# POST request -- sending data
# ---------------------
print("\n[4] POST request -- creating a resource")
new_post = {
    "title": "My Python Learning Journey",
    "body": "Documenting everything I learn about Python here.",
    "userId": 1
}
response = requests.post(
    "https://jsonplaceholder.typicode.com/posts",
    json=new_post   # requests automatically sets Content-Type and serializes
)
print(f"  Status: {response.status_code}")
print(f"  Created resource: {response.json()}")

# ---------------------
# PUT vs PATCH -- I mixed these up initially
# ---------------------
print("\n[5] PUT (full replace) vs PATCH (partial update)")
print("  PUT requires sending the ENTIRE resource, even unchanged fields.")
print("  PATCH only requires the fields you actually want to change.")

# PUT example
put_response = requests.put(
    "https://jsonplaceholder.typicode.com/posts/1",
    json={"id": 1, "title": "Fully Updated Title", "body": "New body", "userId": 1}
)
print(f"  PUT status: {put_response.status_code}")

# PATCH example
patch_response = requests.patch(
    "https://jsonplaceholder.typicode.com/posts/1",
    json={"title": "Just the title changed"}
)
print(f"  PATCH status: {patch_response.status_code}")

# ---------------------
# DELETE request
# ---------------------
print("\n[6] DELETE request")
delete_response = requests.delete("https://jsonplaceholder.typicode.com/posts/1")
print(f"  DELETE status: {delete_response.status_code}")

# ---------------------
# Handling errors and timeouts
# ---------------------
print("\n[7] Error handling -- what I learned NOT to skip")
try:
    response = requests.get(
        "https://jsonplaceholder.typicode.com/users/9999",
        timeout=5   # ALWAYS set a timeout -- learned this after a script
                     # hung indefinitely once on a dead connection
    )
    response.raise_for_status()   # raises an exception for 4xx/5xx codes
except requests.exceptions.HTTPError as e:
    print(f"  HTTP error: {e}")
except requests.exceptions.Timeout:
    print("  Request timed out")
except requests.exceptions.ConnectionError:
    print("  Connection failed -- check internet or URL")
except requests.exceptions.RequestException as e:
    print(f"  Some other request error: {e}")

# ---------------------
# Headers -- sending custom headers (auth tokens, etc.)
# ---------------------
print("\n[8] Custom headers (used for auth tokens in real projects)")
headers = {
    "User-Agent": "PavanPythonLearning/1.0",
    "Accept": "application/json"
}
response = requests.get("https://jsonplaceholder.typicode.com/users/2", headers=headers)
print(f"  Status with custom headers: {response.status_code}")

print("""
  My note: in a REAL project needing authentication, this is where I'd
  add something like headers={"Authorization": "Bearer <token>"}.
  Never hardcode API keys directly in source code -- learned to use
  environment variables (os.environ.get('API_KEY')) instead, after
  reading about people accidentally leaking keys on public GitHub repos.
""")

print("=" * 50)

# =============================================================================
# Sample Output (live data, will vary slightly each run):
#
# [1] Basic GET request
#   Status code: 200
#   URL: https://jsonplaceholder.typicode.com/users/1
#   Name : Leanne Graham
#   Email: Sincere@april.biz
#   City : Gwenborough
# =============================================================================

# =============================================================================
# PROGRAM OUTPUT
# Run with: python3 REST_API.py
# =============================================================================
#
# NOTE: This sandboxed execution environment blocks outbound HTTP
# requests to hosts outside an allowlist -- an egress proxy returns an
# HTTP 403 with a plain-text 'Host not in allowlist' body instead of
# letting the request reach jsonplaceholder.typicode.com. Section [1]
# still completes because the code only checks status_code == 200, but
# section [3] calls response.json() on that plain-text 403 body, which
# is not valid JSON and raises an uncaught JSONDecodeError, ending the
# script there. This is an environment restriction, not a bug in the
# script -- with real internet access this runs the way the author's
# own 'Sample Output' comment at the bottom of this file describes.
#
# ==================================================
#     REST API DEMO
# ==================================================
#
# [1] Basic GET request
#   Status code: 403
#   URL: https://jsonplaceholder.typicode.com/users/1
#   Request failed with status 403
#
# [2] HTTP Status Codes I keep referring back to
#   200 OK                        - Request succeeded
#   201 Created                   - Resource created successfully (POST)
#   400 Bad Request               - Server couldn't understand the request
#   401 Unauthorized              - Authentication required/failed
#   403 Forbidden                 - Authenticated, but not allowed
#   404 Not Found                 - Resource doesn't exist
#   500 Internal Server Error     - Something broke on the server side
#
# [3] GET with query parameters
# Traceback (most recent call last):
#   File "/usr/local/lib/python3.12/dist-packages/requests/models.py", line 978, in json
#     return complexjson.loads(self.text, **kwargs)
#            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
#   File "/usr/lib/python3.12/json/__init__.py", line 346, in loads
#     return _default_decoder.decode(s)
#            ^^^^^^^^^^^^^^^^^^^^^^^^^^
#   File "/usr/lib/python3.12/json/decoder.py", line 337, in decode
#     obj, end = self.raw_decode(s, idx=_w(s, 0).end())
#                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
#   File "/usr/lib/python3.12/json/decoder.py", line 355, in raw_decode
#     raise JSONDecodeError("Expecting value", s, err.value) from None
# json.decoder.JSONDecodeError: Expecting value: line 1 column 1 (char 0)
#
# During handling of the above exception, another exception occurred:
#
# Traceback (most recent call last):
#   File "/tmp/tmp.8wUE8rivNP/REST_API.py", line 62, in <module>
#     posts = response.json()
#             ^^^^^^^^^^^^^^^
#   File "/usr/local/lib/python3.12/dist-packages/requests/models.py", line 982, in json
#     raise RequestsJSONDecodeError(e.msg, e.doc, e.pos)
# requests.exceptions.JSONDecodeError: Expecting value: line 1 column 1 (char 0)
#
# [Process exited with status 1]
#
# =============================================================================

