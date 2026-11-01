import socket
import json
from cryptography.fernet import Fernet
import threading

KEY = b'xxxxxxxxxxxxxxxxxxxxxx'
fernet = Fernet(KEY)

host = input("Enter server IP (e.g., 127.0.0.1): ")
port = 12345

username = input("Username: ")
password = input("Password: ")

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((host, port))
sock.sendall((json.dumps({"username": username, "password": password}) + "\n").encode())
reply = json.loads(sock.makefile("r").readline().strip())
if reply.get("status") != "ok":
    print("Auth failed:", reply.get("msg"))
    sock.close()
    exit()

print("Connected to chat server!")

def recv_messages():
    fileobj = sock.makefile("r")
    for line in fileobj:
        msg = json.loads(line.strip())
        decrypted = fernet.decrypt(msg["message"].encode()).decode()
        print(f"[{msg['from']}] {decrypted}")

threading.Thread(target=recv_messages, daemon=True).start()

while True:
    try:
        text = input()
        if text.lower() in ("/quit", "/exit"):
            break
        sock.sendall((json.dumps({"message": text}) + "\n").encode())
    except KeyboardInterrupt:
        break

sock.close()
print("Disconnected.")
