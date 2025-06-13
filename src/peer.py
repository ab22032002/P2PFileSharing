import socket
import threading
import json
import os
import base64

CHUNK_DIR = "chunks"

def handle_peer(conn, addr):
    print(f"[+] Connected by {addr}")
    try:
        data = conn.recv(4096).decode()
        message = json.loads(data)

        if message["type"] == "REQUEST_CHUNK":
            file_id = message["file_id"]
            chunk_index = message["chunk_index"]

            chunk_path = os.path.join(CHUNK_DIR, f"{file_id}_{chunk_index}")
            if os.path.exists(chunk_path):
                with open(chunk_path, "rb") as f:
                    chunk_data = f.read()
                encoded_data = base64.b64encode(chunk_data).decode('utf-8')  # ✅ Fix here
                response = {
                    "type": "CHUNK_DATA",
                    "file_id": file_id,
                    "chunk_index": chunk_index,
                    "data": encoded_data
                }
            else:
                response = {
                    "type": "ERROR",
                    "message": f"Chunk {chunk_index} not found for file {file_id}"
                }

            conn.sendall(json.dumps(response).encode())

    except Exception as e:
        print(f"[!] Error: {e}")
    finally:
        conn.close()

def start_server(port=9000):
    if not os.path.exists(CHUNK_DIR):
        os.makedirs(CHUNK_DIR)

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("0.0.0.0", port))
    server.listen(5)
    print(f"[+] Peer server listening on port {port}...")
    
    # ✅ Manual stop
    threading.Thread(target=lambda: input("⏹ Press Enter to stop the server...\n") or os._exit(0)).start()

    try:
        while True:
            conn, addr = server.accept()
            threading.Thread(target=handle_peer, args=(conn, addr)).start()
    except KeyboardInterrupt:
        print("\n[!] Shutting down server.")
        server.close()


if __name__ == "__main__":
    start_server()

