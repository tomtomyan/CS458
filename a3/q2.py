import json
import urllib2
import nacl.secret
import nacl.utils
import base64

key = "fc7fabaaa3d2b196c92351aa4afac1d16255444e54be64fc5febbb5bafbc68ae"

box = nacl.secret.SecretBox(key)

message = b"OMEGALUL"

encrypted = box.encrypt(message)

data = {
        "api_token": "f0cd8f18e9d280fd23f9eae0d1df65bc0a93d1dbfc3e9f730d31c425249ce05e",
        "to": "jessie",
        "message": base64.b64.encode(encrypted)
}

req = urllib2.Request('https://whoomp.cs.uwaterloo.ca/458a3/api/psk/send')
req.add_header('Accept', 'application/json')
req.add_header('Content-Type', 'application/json')

response = urllib2.urlopen(req, json.dumps(data))
print(response.read())
