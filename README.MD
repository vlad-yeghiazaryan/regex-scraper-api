## Purpose
API for scraping any set of static sites with regex queries.

## Execution order:
```bash
docker pull ibmfunctions/action-python-v3.7
```
```bash
docker run --rm -v "$PWD:/tmp" ibmfunctions/action-python-v3.7 bash -c "cd /tmp && virtualenv virtualenv && source virtualenv/bin/activate && pip install -r requirements.txt"
```
```bash
zip -r regexScraper.zip virtualenv __main__.py helper.py scraper.py
```
```bash
ibmcloud fn action create regexScraper regexScraper.zip --kind python:3.7 --web true
```
This is the equivalent python dictionary representation of the payload. Make sure to convert it into a valid json before sending the request.
```python
payload_sample = {"urls": ["https://medium.com"],
"query_list": { 
"first": "(?<=>01<.*?<h2.*?>)([\\\)\(\[\]…!&?’'\".,;@#%$\+\=\:\*\^\b\a\d\w\s]+)(?=<\/h2>)",
"second": "(?<=>02<.*?<h2.*?>)([\\\)\(\[\]…!&?’'\".,;@#%$\+\=\:\*\^\b\a\d\w\s]+)(?=<\/h2>)",
"third": "(?<=>03<.*?<h2.*?>)([\\\)\(\[\]…!&?’'\".,;@#%$\+\=\:\*\^\b\a\d\w\s]+)(?=<\/h2>)"
}}
```

Example use case in python:
```python
import requests
import json

api_url = 'https://9ec94559.us-south.apigw.appdomain.cloud/regex-scraper-api'
urls = ['https://medium.com']
query_list = {
    'first': f"(?<=>0{1}<.*?<h2.*?>)([\\\)\(\[\]…!&?’'\".,;@#%$\+\=\:\*\^\b\a\d\w\s]+)(?=<\/h2>)",
    'second': f"(?<=>0{2}<.*?<h2.*?>)([\\\)\(\[\]…!&?’'\".,;@#%$\+\=\:\*\^\b\a\d\w\s]+)(?=<\/h2>)",
    'third': f"(?<=>0{3}<.*?<h2.*?>)([\\\)\(\[\]…!&?’'\".,;@#%$\+\=\:\*\^\b\a\d\w\s]+)(?=<\/h2>)"
}
payload = {'urls': urls, 'query_list': query_list}
headers = {
    'content-type': "application/json",
    'accept': "application/json"
    }
data = requests.post(api_url, data = json.dumps(payload), headers=headers)
data.json()
```
```javascript
{'scraped_data': [{'date': '2022-01-04',
   'first': '10 Predictions for Web3 and the Cryptoeconomy for 2022',
   'second': 'Automate WhatsApp Messages with Python Instantly!',
   'third': 'Start a Sneaky Online Empire from Your Bedroom (In Silence) to Unlock Passive Income',
   'url': 'https://medium.com/'}]}
```