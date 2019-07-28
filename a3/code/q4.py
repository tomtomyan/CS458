import json
import nacl.bindings
from urllib import request, parse
import base64
import binascii

# Uncomment for part 1
#verify_key, signing_key = nacl.bindings.crypto_sign_keypair()
#print(binascii.hexlify(signing_key))
#data = parse.urlencode({
#        "api_token": "f0cd8f18e9d280fd23f9eae0d1df65bc0a93d1dbfc3e9f730d31c425249ce05e",
#        "public_key": base64.b64encode(verify_key)
#}).encode()
#req = request.Request('https://whoomp.cs.uwaterloo.ca/458a3/api/signed/set-key', data)
#r = request.urlopen(req)

# PART 2
signing_key = binascii.unhexlify(b'd478e8e7256ff9f5fdee4199d85f01fba409ef0e2b2443ded670ae82f90a54d6a79c0e6e687b3f454e38d978d41c253c35a57b76311bcc4db59672f0e1d7daaa')
message = b"OMEGALUL"
signed = nacl.bindings.crypto_sign(message, signing_key)

data = parse.urlencode({
        "api_token": "f0cd8f18e9d280fd23f9eae0d1df65bc0a93d1dbfc3e9f730d31c425249ce05e",
        "to": "jessie",
        "message": base64.b64encode(signed)
}).encode()

req = request.Request('https://whoomp.cs.uwaterloo.ca/458a3/api/signed/send', data)
r = request.urlopen(req)
