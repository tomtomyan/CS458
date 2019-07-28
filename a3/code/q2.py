import json
from urllib import request, parse
import nacl.secret
import nacl.utils
import base64
import binascii

key = "fc7fabaaa3d2b196c92351aa4afac1d16255444e54be64fc5febbb5bafbc68ae"

box = nacl.secret.SecretBox(binascii.unhexlify(key))

message = b"OMEGALUL"

encrypted = box.encrypt(message)

data = parse.urlencode({
        "api_token": "f0cd8f18e9d280fd23f9eae0d1df65bc0a93d1dbfc3e9f730d31c425249ce05e",
        "to": "jessie",
        "message": base64.b64encode(encrypted)
}).encode()

headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
}


# PART 2

data = parse.urlencode({
        "api_token": "f0cd8f18e9d280fd23f9eae0d1df65bc0a93d1dbfc3e9f730d31c425249ce05e"
}).encode()

req = request.Request('https://whoomp.cs.uwaterloo.ca/458a3/api/psk/inbox', data)
#req.add_header('Accept', 'application/json')
#req.add_header('Content-Type', 'application/json')

r = request.urlopen(req)

data = json.loads(r.read().decode(r.info().get_param('charset') or 'utf-8'))

print(data[0]["message"])

encrypted = base64.b64decode(data[0]["message"])

plaintext = box.decrypt(encrypted)

print(plaintext.decode('utf-8'))
