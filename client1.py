import requests
import configclient

API_KEY = configclient.client["key"]

print("\n--- Testing /ByKeyword ---")
url = f"http://127.0.0.1:5000/ByKeyword?key={API_KEY}&keyword=security"
r = requests.get(url)
print(r.text)

print("\n--- Testing /ByAuthor ---")
url = f"http://127.0.0.1:5000/ByAuthor?key={API_KEY}&name=Bonny%20Chu"
r = requests.get(url)
print(r.text)

print("\n--- Testing /ByDate ---")
url = f"http://127.0.0.1:5000/ByDate?key={API_KEY}&date=2025-12-03"
r = requests.get(url)
print(r.text)
