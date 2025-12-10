import requests
import configclient

API_KEY = configclient.client["key"]

print("\n--- Testing Query 1 ---")
url = f"http://127.0.0.1:5000/runQuery?key={API_KEY}&q=chicago"
r = requests.get(url)
print(r.text)

print("\n--- Testing Query 2 ---")
url = f"http://127.0.0.1:5000/runQuery?key={API_KEY}&q=military"
r = requests.get(url)
print(r.text)

print("\n--- Testing Query 3 ---")
url = f"http://127.0.0.1:5000/runQuery?key={API_KEY}&q=climate"
r = requests.get(url)
print(r.text)
