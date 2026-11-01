import socket
import threading
import json
import hashlib
from cryptography.fernet import Fernet

KEY = b'xxxxxxxxxxxxxx'
fernet = Fernet(KEY)

USERS = {
    "Rakesh": {"salt": "somesalt123", "password": "xxxx"},
    "Balaji": {"salt": "othersalt456", "password": "xxxxx"}
}

clients = []
clients_lock = threading.Lock()

def verify_user(username, password):
    if username not in USERS:
        return False
    salt = USERS[username]["salt"].encode()
    hashed = hashlib.sha256(salt + password.encode()).hexdigest()
    return hashed == hashlib.sha256(salt + USERS[username]["password"].encode()).hexdigest()

def broadcast(sender, message):
    encrypted_msg = fernet.encrypt(message.encode()).decode()
    with clients_lock:
        for c in clients:
            try:
                c.sendall((json.dumps({"from": sender, "message": encrypted_msg}) + "\n").encode())
            except:
                pass

def handle_client(conn, addr):
    fileobj = conn.makefile("r")
    auth_line = fileobj.readline()
    if not auth_line:
        conn.close()
        return
    auth = json.loads(auth_line.strip())
    username = auth.get("username")
    password = auth.get("password")
    if not verify_user(username, password):
        conn.sendall((json.dumps({"status": "fail", "msg": "invalid credentials"}) + "\n").encode())
        conn.close()
        return
    conn.sendall((json.dumps({"status": "ok", "msg": "welcome"}) + "\n").encode())
    with clients_lock:
        clients.append(conn)
    broadcast("SERVER", f"{username} joined the chat")
    for line in fileobj:
        if not line:
            break
        msg = json.loads(line.strip())
        text = msg.get("message", "")
        broadcast(username, text)
    with clients_lock:
        clients.remove(conn)
    broadcast("SERVER", f"{username} left the chat")
    conn.close()

def main():
    host = "0.0.0.0"
    port = 12345
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((host, port))
    sock.listen(5)
    print(f"Server listening on {host}:{port}")
    try:
        while True:
            conn, addr = sock.accept()
            threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()
    except KeyboardInterrupt:
        print("Server stopped")
    finally:
        sock.close()

if __name__ == "__main__":
    main()
