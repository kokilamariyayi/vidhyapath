import requests
url = "https://vidhyapath.onrender.com/chat"
payload = {"message": "What can I study after 12th?", "target_lang": "ta"}
response = requests.post(url, json=payload)
print(response.json())
