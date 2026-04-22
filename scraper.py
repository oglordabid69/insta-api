import requests

url = "http://127.0.0.1:8000/leads"

data = {
    "company": "OpenAI",
    "website": "https://openai.com",
    "score": 98
}

response = requests.post(url, json=data)

print(response.json())