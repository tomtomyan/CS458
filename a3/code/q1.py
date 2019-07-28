import json
import urllib2

data = {
        "api_token": "f0cd8f18e9d280fd23f9eae0d1df65bc0a93d1dbfc3e9f730d31c425249ce05e",
        "to": "jessie",
        "message": "d2VsbCBoZWxsbyB0aGVyZQ=="
}

req = urllib2.Request('https://whoomp.cs.uwaterloo.ca/458a3/api/plain/send')
req.add_header('Accept', 'application/json')
req.add_header('Content-Type', 'application/json')

response = urllib2.urlopen(req, json.dumps(data))

# Part 2
data = {
        "api_token": "f0cd8f18e9d280fd23f9eae0d1df65bc0a93d1dbfc3e9f730d31c425249ce05e"
}

req = urllib2.Request('https://whoomp.cs.uwaterloo.ca/458a3/api/plain/inbox')
req.add_header('Accept', 'application/json')
req.add_header('Content-Type', 'application/json')

response = urllib2.urlopen(req, json.dumps(data))
print(response.read())
