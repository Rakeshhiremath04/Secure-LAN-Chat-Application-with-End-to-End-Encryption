Secure LAN Chat Application (Encrypted) - Instructions

1. Install Python 3.8+ and cryptography library:
   python -m pip install -r requirements.txt

2. Server Execution:
   python chat_server.py
   - It will start listening on port 12345.

3. Client Execution:
   python chat_client.py
   - Enter server IP, username, and password.
   - Default users: alice/password1, bob/password2

4. Chat Commands:
   /quit or /exit : exit client

5. Notes:
   - Must run server first.
   - Both server and clients already share a fixed encryption key.
