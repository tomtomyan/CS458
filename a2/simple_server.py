import socket
import sys

# modified by Brian Winkelmann and then later by Stan Gurtler
# code modified from sample code at
# https://docs.python.org/2/library/socket.html

# defaults to port 31337, but can be used with any port
# supplied by command line argument like so:
# python simple_server.py 32674
# this would open a server on port 32674 instead of 31337
port = 31337
if len(sys.argv) > 1:
    port = int(sys.argv[1])

hostname = ""

try:
    with open("/etc/hostname", "r") as f:
        hostname = f.readline().rstrip()
except:
    pass

if hostname.find("ugster") != -1:
    hostname = hostname + ".student.cs.uwaterloo.ca"
else:
    hostname = "localhost"

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((hostname, port))
s.listen(1)

print("Simple server running on http://%s:%d/" % (hostname, port))
print("Use (ctrl + c) to end server")
i = 0
while True:
    try:
        conn, addr = s.accept()
        data = conn.recv(1024)
        conn.close()
        print "\n {0}".format(i)
        print(data.splitlines()[0])
        i += 1
    except KeyboardInterrupt:
        s.close()
        print("\nGoodbye")
        break
