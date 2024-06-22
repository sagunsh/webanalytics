import requests

r = requests.get('http://127.0.0.1:3000/')

print(r.text)