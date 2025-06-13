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

        # ✅ Read the full JSON response safely
        response_chunks = []
        while True:
            part = s.recv(4096)
            if not part:
                break
            response_chunks.append(part)

        full_response = b''.join(response_chunks).decode('utf-8')
        response_data = json.loads(full_response)

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

# Replace with your actual file_id and chunk index
request_chunk(file_id="295254942f1f4043904d419acc4d7617f351e8b3f461b46ad622811741defef7", chunk_index=1)
