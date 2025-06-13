import socket
import threading
import json
import os
import base64

CHUNK_DIR = "chunks"

def handle_peer(conn, addr):
    print(f"[+] Connected by {addr}")
    try:
        # Receive full request (up to 4096 bytes)
        buffer = b""
        while True:
            part = conn.recv(1024)
            if not part:
                break
            buffer += part
            if len(part) < 1024:
                break

        try:
            message = json.loads(buffer.decode(errors="ignore"))
        except json.JSONDecodeError as e:
            print(f"[!] JSON decode error from {addr}: {e}")
            return

        if message.get("type") == "REQUEST_CHUNK":
            file_id = message["file_id"]
            chunk_index = message["chunk_index"]

            chunk_path = os.path.join(CHUNK_DIR, f"{file_id}_{chunk_index}")
            if os.path.exists(chunk_path):
                with open(chunk_path, "rb") as f:
                    chunk_data = f.read()
                encoded_data = base64.b64encode(chunk_data).decode()

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
        else:
            response = {
                "type": "ERROR",
                "message": "Unsupported request type"
            }

        response_json = json.dumps(response).encode()
        conn.sendall(response_json)

    except Exception as e:
        print(f"[!] Error while handling {addr}: {e}")
    finally:
        conn.close()
        print(f"[-] Connection with {addr} closed.")


def start_server(port=9000):
    if not os.path.exists(CHUNK_DIR):
        os.makedirs(CHUNK_DIR)

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(("0.0.0.0", port))
    server.listen(10)
    print(f"[🌐] Peer server listening on port {port}...")

    def shutdown_trigger():
        input("⏹ Press Enter to stop the server...\n")
        os._exit(0)

    threading.Thread(target=shutdown_trigger, daemon=True).start()

    try:
        while True:
            conn, addr = server.accept()
            threading.Thread(target=handle_peer, args=(conn, addr), daemon=True).start()
    except KeyboardInterrupt:
        print("\n[!] Server interrupted. Shutting down.")
    finally:
        server.close()


if __name__ == "__main__":
    start_server()
