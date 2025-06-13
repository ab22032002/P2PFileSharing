import socket
import json
import base64

def request_chunk(file_id, chunk_index, peer_ip="127.0.0.1", peer_port=9000):
    request = {
        "type": "REQUEST_CHUNK",
        "file_id": file_id,
        "chunk_index": chunk_index
    }

    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((peer_ip, peer_port))
        s.send(json.dumps(request).encode())

        # Read full response (with buffer loop)
        chunks = []
        while True:
            chunk = s.recv(4096)
            if not chunk:
                break
            chunks.append(chunk)
        
        full_data = b''.join(chunks).decode()
        response_data = json.loads(full_data)

        if response_data["type"] == "CHUNK_DATA":
            decoded_data = base64.b64decode(response_data["data"])
            print(f"[✓] Received chunk {chunk_index} of file {file_id}")
            print("Data Preview (first 100 bytes):")
            print(decoded_data[:100])
        else:
            print("[!] Error:", response_data["message"])
    except Exception as e:
        print("[!] Failed to request chunk:", e)
    finally:
        s.close()
