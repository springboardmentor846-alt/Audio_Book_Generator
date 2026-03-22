import requests

url = "http://127.0.0.1:5000/upload"
filepath = "test.txt"

# Create dummy test file
with open(filepath, "w") as f:
    f.write("Hello world! This is a test file for the AI audiobook generator.")

with open(filepath, "rb") as f:
    files = {"file": f}
    data = {"language": "Spanish", "speed": "Normal"}
    print("Sending request...")
    response = requests.post(url, files=files, data=data)

print(f"Status Code: {response.status_code}")
try:
    print(f"Response: {response.json()}")
except Exception as e:
    print(f"Text Response: {response.text}")
