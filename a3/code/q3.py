import json
from nacl import pwhash, secret, utils
from urllib import request, parse
import base64
import binascii

password = b"southern purpose"
message = b"OMEGALUL"

salt = "0abda7d80cbdaa3b1cb797dd83857cca6565fee329b0d166fa359eb4440aba6d"
ops = 524288
mem = 16777216

key = pwhash.kdf_scryptsalsa208sha256(32, password, binascii.unhexlify(salt), ops, mem)

box = secret.SecretBox(key)

encrypted = box.encrypt(message)

data = parse.urlencode({
        "api_token": "f0cd8f18e9d280fd23f9eae0d1df65bc0a93d1dbfc3e9f730d31c425249ce05e",
        "to": "jessie",
        "message": base64.b64encode(encrypted)
}).encode()

# Uncomment for part 1
#req = request.Request('https://whoomp.cs.uwaterloo.ca/458a3/api/psp/send', data)
#r = request.urlopen(req)

# PART 2

data = parse.urlencode({
        "api_token": "f0cd8f18e9d280fd23f9eae0d1df65bc0a93d1dbfc3e9f730d31c425249ce05e"
}).encode()

req = request.Request('https://whoomp.cs.uwaterloo.ca/458a3/api/psp/inbox', data)
r = request.urlopen(req)

data = json.loads(r.read().decode(r.info().get_param('charset') or 'utf-8'))

print(data[0]["message"])

encrypted = base64.b64decode(data[0]["message"])

plaintext = box.decrypt(encrypted)

print(plaintext.decode('utf-8'))
