import json
import nacl.bindings
from nacl.public import PrivateKey, PublicKey, Box
from nacl.encoding import HexEncoder
import nacl.secret
import nacl.utils
from urllib import request, parse
import base64
import binascii

# Part 1
id_vk, id_sk = nacl.bindings.crypto_sign_keypair()
data = parse.urlencode({
        "api_token": "f0cd8f18e9d280fd23f9eae0d1df65bc0a93d1dbfc3e9f730d31c425249ce05e",
        "public_key": base64.b64encode(bytes(id_vk))
}).encode()
req = request.Request('https://whoomp.cs.uwaterloo.ca/458a3/api/prekey/set-identity-key', data)
r = request.urlopen(req)

secretkey = PrivateKey.generate()
prekey = secretkey.public_key

signed_prekey = nacl.bindings.crypto_sign(bytes(prekey), id_sk)
data = parse.urlencode({
        "api_token": "f0cd8f18e9d280fd23f9eae0d1df65bc0a93d1dbfc3e9f730d31c425249ce05e",
        "public_key": base64.b64encode(signed_prekey)
}).encode()
req = request.Request('https://whoomp.cs.uwaterloo.ca/458a3/api/prekey/set-signed-prekey', data)
r = request.urlopen(req)

# Part 2
data = parse.urlencode({
        "api_token": "f0cd8f18e9d280fd23f9eae0d1df65bc0a93d1dbfc3e9f730d31c425249ce05e",
        "user": "jessie"
}).encode()
req = request.Request('https://whoomp.cs.uwaterloo.ca/458a3/api/prekey/get-identity-key', data)
r = request.urlopen(req)
data = json.loads(r.read().decode(r.info().get_param('charset') or 'utf-8'))
print(data)
print(data["public_key"])
jessie_id_vk = base64.b64decode(data["public_key"])

data = parse.urlencode({
        "api_token": "f0cd8f18e9d280fd23f9eae0d1df65bc0a93d1dbfc3e9f730d31c425249ce05e",
        "user": "jessie"
}).encode()
req = request.Request('https://whoomp.cs.uwaterloo.ca/458a3/api/prekey/get-signed-prekey', data)
r = request.urlopen(req)
data = json.loads(r.read().decode(r.info().get_param('charset') or 'utf-8'))
print(data)
print(data["public_key"])
jessie_signed_prekey = base64.b64decode(data["public_key"])

jessie_pk = nacl.bindings.crypto_sign_open(jessie_signed_prekey, jessie_id_vk)

message = b"lmao"
nonce = nacl.utils.random(Box.NONCE_SIZE)
encrypted = nacl.bindings.crypto_box(message, nonce, jessie_pk, bytes(secretkey))
data = parse.urlencode({
        "api_token": "f0cd8f18e9d280fd23f9eae0d1df65bc0a93d1dbfc3e9f730d31c425249ce05e",
        "to": "jessie",
        "message": base64.b64encode(nonce + encrypted)
}).encode()
req = request.Request('https://whoomp.cs.uwaterloo.ca/458a3/api/prekey/send', data)
r = request.urlopen(req)

# Part 3
data = parse.urlencode({
        "api_token": "f0cd8f18e9d280fd23f9eae0d1df65bc0a93d1dbfc3e9f730d31c425249ce05e"
}).encode()
req = request.Request('https://whoomp.cs.uwaterloo.ca/458a3/api/prekey/inbox', data)
r = request.urlopen(req)
data = json.loads(r.read().decode(r.info().get_param('charset') or 'utf-8'))
encrypted = base64.b64decode(data[0]["message"])
box = Box(secretkey, PublicKey(jessie_pk))
plaintext = box.decrypt(encrypted)
print(plaintext.decode('utf-8'))
