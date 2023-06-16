import requests
import pprint

"""
BASE_URL = 'http://127.0.0.1:8000'
#response = requests.get(f"{BASE_URL}/list-productlines")
"""
#response1 = requests.get("http://127.0.0.1:8000/list-productlines")
#pprint.pprint(response1.json())

response2 = requests.get("http://127.0.0.1:8000/get-productlines/Motorcycles")
pprint.pprint(response2.json())