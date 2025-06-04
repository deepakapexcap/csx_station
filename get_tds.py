import json
import requests
from keys import api_key,secret_key
from gen_sign import get_signature
import time

payload={}

url = "https://coinswitch.co/trade/api/v2/tds"

epoch_time = str(int(time.time() * 1000))
signature= get_signature("GET","/trade/api/v2/tds",payload,epoch_time,secret_key)

headers = {
  'Content-Type': 'application/json',
  'X-AUTH-SIGNATURE': signature,
  'X-AUTH-APIKEY': api_key,
  'X-AUTH-EPOCH': epoch_time  

}


response = requests.request("GET", url, headers=headers, json=payload)
response = response.json()
print(response)