from client import Client
from server import Server
from auth import authenticate
import sys

resp = input(
    "Enter 'c' to run in client mode, 's' to run in server mode: ").lower()
while resp not in ('c', 's'):
    print("Invalid choice")
    resp = input(
        "Enter 'c' to run in client mode, 's' to run in server mode: ").lower()
if resp == 'c':
    token = input("Enter authentication token: ")
    if not authenticate(token):
        print("Invalid token")
        sys.exit()
    client = Client(('127.0.0.1', 9000))
    client.run()
else:
    server = Server('127.0.0.1', 9000, 3)
    server.run()
