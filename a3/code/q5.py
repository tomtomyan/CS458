import json
import nacl.bindings.crypto_generichash
import nacl.bindings
from nacl.hash import blake2b
from nacl.public import PrivateKey, PublicKey, Box
from nacl.encoding import HexEncoder
from urllib import request, parse
import base64
import binascii

# Uncomment for part 1
#data = parse.urlencode({
#        "api_token": "f0cd8f18e9d280fd23f9eae0d1df65bc0a93d1dbfc3e9f730d31c425249ce05e",
#        "user": "jessie"
#}).encode()
#req = request.Request('https://whoomp.cs.uwaterloo.ca/458a3/api/pke/get-key', data)
#r = request.urlopen(req)
#data = json.loads(r.read().decode(r.info().get_param('charset') or 'utf-8'))
#print(data)
#print(data["public_key"])
#pk = base64.b64decode(data["public_key"])
#pk_hash = nacl.hash.blake2b(pk)
#print(pk_hash)

# Part 2
jessie_pk = b'JLAb7Kj93aUdb6RBkyhk8Z9A9vKa3WJIzloSvsFGDTA='
sk = PrivateKey.generate()
pk = sk.public_key
data = parse.urlencode({
        "api_token": "f0cd8f18e9d280fd23f9eae0d1df65bc0a93d1dbfc3e9f730d31c425249ce05e",
        "public_key": base64.b64encode(bytes(pk))
}).encode()
req = request.Request('https://whoomp.cs.uwaterloo.ca/458a3/api/pke/set-key', data)
r = request.urlopen(req)
message = b"OMEGALUL"
nonce = nacl.utils.random(Box.NONCE_SIZE)
encrypted = nacl.bindings.crypto_box(message, nonce, base64.b64decode(jessie_pk), bytes(sk))
data = parse.urlencode({
        "api_token": "f0cd8f18e9d280fd23f9eae0d1df65bc0a93d1dbfc3e9f730d31c425249ce05e",
        "to": "jessie",
        "message": base64.b64encode(nonce + encrypted)
}).encode()
req = request.Request('https://whoomp.cs.uwaterloo.ca/458a3/api/pke/send', data)
r = request.urlopen(req)

# PART 3
data = parse.urlencode({
        "api_token": "f0cd8f18e9d280fd23f9eae0d1df65bc0a93d1dbfc3e9f730d31c425249ce05e"
}).encode()
req = request.Request('https://whoomp.cs.uwaterloo.ca/458a3/api/pke/inbox', data)
r = request.urlopen(req)
data = json.loads(r.read().decode(r.info().get_param('charset') or 'utf-8'))
encrypted = base64.b64decode(data[0]["message"])
box = Box(sk, PublicKey(base64.b64decode(jessie_pk)))
plaintext = box.decrypt(encrypted)
print(plaintext.decode('utf-8'))
