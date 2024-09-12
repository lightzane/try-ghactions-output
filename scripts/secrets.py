import requests
import json
import sys
from base64 import b64encode
from nacl import encoding, public

GH_TOKEN = sys.argv[1]
REPO = sys.argv[2]
OWNER = 'lightzane'

# Reference: https://docs.github.com/en/rest/actions/secrets?apiVersion=2022-11-28#create-or-update-a-repository-secret
HEADERS = {
  'Accept': 'application/vnd.github+json',
  'Authorization': f'Bearer {GH_TOKEN}',
  'X-GitHub-Api-Version': '2022-11-28'
}

def github_api(SECRET_NAME):
  return f'https://api.github.com/repos/{OWNER}/{REPO}/actions/secrets/{SECRET_NAME}'

def get_secret(key):
  return requests.get(
    github_api(key),
    headers=HEADERS
  )

def put_secret(key, enc_value):
  if enc_value is None:
    return None

  jsonData = {
    'encrypted_value': enc_value,
    'key_id': data['key_id'] # data variable will be defined later at Line 52
  }

  return requests.put(
    github_api(key),
    headers=HEADERS,
    json=jsonData
  )

def encrypt(public_key: str, secret_value: str) -> str:
  """Encrypt a Unicode string using the public key"""
  public_key = public.PublicKey(public_key.encode('utf-8'), encoding.Base64Encoder())
  sealed_box = public.SealedBox(public_key)
  encrypted = sealed_box.encrypt(secret_value.encode('utf-8'))
  return b64encode(encrypted).decode('utf-8')


# Reference: https://docs.github.com/en/rest/actions/secrets?apiVersion=2022-11-28#get-a-repository-public-key
response = get_secret('public-key')
data = json.loads(response.content)

encrypted_gh_token = encrypt(data['key'], GH_TOKEN)

secrets_mapping = {
  'GH_TOKEN': encrypted_gh_token
}

for key, value in secrets_mapping.items():
  put_secret(key, value)
