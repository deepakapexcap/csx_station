
from cryptography.hazmat.primitives.asymmetric import ed25519
from urllib.parse import urlparse, urlencode
import urllib
import json
import time 
from keys import secret_key
 # example method  ['GET', 'POST', 'DELETE']

 # params represent the query params we need to pass during GET call


# secret_key= SECRET_KEY

def get_signature(method, endpoint, params, epoch_time,secret_key):
  unquote_endpoint = endpoint
  if method == "GET" and len(params) != 0:
      endpoint += ('&', '?')[urlparse(endpoint).query == ''] + urlencode(params)
      unquote_endpoint = urllib.parse.unquote_plus(endpoint)

  signature_msg = method + unquote_endpoint + epoch_time

  request_string = bytes(signature_msg, 'utf-8')
  secret_key_bytes = bytes.fromhex(secret_key)
  secret_key = ed25519.Ed25519PrivateKey.from_private_bytes(secret_key_bytes)
  signature_bytes = secret_key.sign(request_string)
  signature = signature_bytes.hex()
  return signature