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
sk = PrivateKey.generate()
pk = sk.public_key
data = parse.urlencode({
        "api_token": "f0cd8f18e9d280fd23f9eae0d1df65bc0a93d1dbfc3e9f730d31c425249ce05e",
        "public_key": base64.b64encode(bytes(pk))
}).encode()
req = request.Request('https://whoomp.cs.uwaterloo.ca/458a3/api/surveil/set-key', data)
r = request.urlopen(req)

data = parse.urlencode({
        "api_token": "f0cd8f18e9d280fd23f9eae0d1df65bc0a93d1dbfc3e9f730d31c425249ce05e",
        "user": "jessie"
}).encode()
req = request.Request('https://whoomp.cs.uwaterloo.ca/458a3/api/surveil/get-key', data)
r = request.urlopen(req)
data = json.loads(r.read().decode(r.info().get_param('charset') or 'utf-8'))
jessie_pk = base64.b64decode(data["public_key"])

gov_pk = base64.b64decode(b"JlE8TXsFgSjl8QHRTw2LMCLpmkHcJjkPSEpfHyI8VAY=")

message = b"LOLLLLL"
message_key = nacl.utils.random(nacl.secret.SecretBox.KEY_SIZE)
box = nacl.secret.SecretBox(message_key)
message_ciphertext = box.encrypt(message)

recipient_nonce = nacl.utils.random(Box.NONCE_SIZE)
recipient_ciphertext = nacl.bindings.crypto_box(message_key, recipient_nonce, jessie_pk, bytes(sk))

gov_nonce = nacl.utils.random(Box.NONCE_SIZE)
gov_ciphertext = nacl.bindings.crypto_box(message_key, gov_nonce, gov_pk, bytes(sk))
print(len(recipient_nonce))
print(len(recipient_ciphertext))

#data = parse.urlencode({
#        "api_token": "f0cd8f18e9d280fd23f9eae0d1df65bc0a93d1dbfc3e9f730d31c425249ce05e",
#        "to": "jessie",
#        "message": base64.b64encode(recipient_nonce + recipient_ciphertext + gov_nonce + gov_ciphertext + message_ciphertext)
#}).encode()
#req = request.Request('https://whoomp.cs.uwaterloo.ca/458a3/api/surveil/send', data)
#r = request.urlopen(req)

# PART 2
data = parse.urlencode({
        "api_token": "f0cd8f18e9d280fd23f9eae0d1df65bc0a93d1dbfc3e9f730d31c425249ce05e"
}).encode()
req = request.Request('https://whoomp.cs.uwaterloo.ca/458a3/api/surveil/inbox', data)
r = request.urlopen(req)
data = json.loads(r.read().decode(r.info().get_param('charset') or 'utf-8'))
print(data)
message = base64.b64decode(data[0]["message"])
print(message)
print()
nb = nacl.bindings.crypto_box_NONCEBYTES
kb = nacl.bindings.crypto_secretbox_KEYBYTES
mb = 16
recipient_nonce = message[:nb]
print(recipient_nonce)
recipient_ciphertext = message[nb:nb+kb+mb]
print(len(recipient_ciphertext))
print(recipient_ciphertext)
box = Box(sk, PublicKey(jessie_pk))
message_key = box.decrypt(recipient_nonce+recipient_ciphertext)
print("MESSAGE KEY " + str(len(message_key)))
print(message_key)
message_ciphertext = message[2*nb+2*kb+2*mb:]
print(len(message_ciphertext))
print(message_ciphertext)
box = nacl.secret.SecretBox(message_key)
plaintext = box.decrypt(message_ciphertext)
print(plaintext.decode('utf-8'))
