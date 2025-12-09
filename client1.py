import requests

print("\n--- Testing Root ---")
url = "http://127.0.0.1:5000/"
r = requests.get(url)
print(r.text)


print("\n--- Testing /ByKeyword ---")
url = "http://127.0.0.1:5000/ByKeyword?key=123&keyword=security"
r = requests.get(url)
print(r.text)


print("\n--- Testing /ByAuthor ---")
url = "http://127.0.0.1:5000/ByAuthor?key=123&name=Bonny%20Chu"
r = requests.get(url)
print(r.text)


print("\n--- Testing /ByDate ---")
url = "http://127.0.0.1:5000/ByDate?key=123&date=2024-12-01"
r = requests.get(url)
print(r.text)


print("\n--- Testing /ByCategory ---")
url = "http://127.0.0.1:5000/ByCategory?key=123&cat=Politics"
r = requests.get(url)
print(r.text)


print("\n--- Testing /ByRandom ---")
url = "http://127.0.0.1:5000/ByRandom?key=123"
r = requests.get(url)
print(r.text)
