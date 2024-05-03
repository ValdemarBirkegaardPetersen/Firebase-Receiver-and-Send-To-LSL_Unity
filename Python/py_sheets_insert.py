import requests
import json

# Set up the URL and the API endpoint
url = 'https://sheetdb.io/api/v1/0nzn27jxip8c9  '

# Prepare headers and data payload
headers = {
    'Accept': 'application/json',
    'Content-Type': 'application/json'
}
data = {
    'data': [
        {
            'Baseline': 0,
            '': 1,
            'Task 1': 2,
            'Task 2': 3,
            'Task 3': 4,
            'Task 4': 5,
            'Task 5': 6,
            
        }
    ]
}

# Make the POST request
response = requests.post(url, headers=headers, data=json.dumps(data))

# Convert the response to JSON
response_json = response.json()

# Print the result
print(response_json)