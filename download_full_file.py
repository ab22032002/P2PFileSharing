import json
import socket
import base64
import os
from file_utils import reconstruct_file

SHARED_FILE = "shared_files.json"
DOWNLOADS_DIR = "downloads"

def load_shared_files():
    if os.path.exists(SHARED_FILE):
        with open(SHARED_FILE, "r") as f:
            return json.load(f)
    return {}

def recv_full_data(sock):
    buffer = b""
    while True:
        try:
            part = sock.recv(4096)
            if not part:
                break
            buffer += part
        except:
            break
    return buffer

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

        full_response = recv_full_data(s).decode()
        response_data = json.loads(full_response)

        if response_data["type"] == "CHUNK_DATA":
            decoded_data = base64.b64decode(response_data["data"])
            return decoded_data
        else:
            print("[!] Error:", response_data["message"])
            return None
    except Exception as e:
        print(f"[!] Exception on chunk {chunk_index}:", e)
        return None
    finally:
        s.close()


def main():
    shared_files = load_shared_files()
    if not shared_files:
        print("[!] No shared files available.")
        return

    print("Available Files:")
    keys = list(shared_files.keys())
    for idx, file_id in enumerate(keys):
        info = shared_files[file_id]
        print(f"[{idx}] {info['filename']} ({info['total_chunks']} chunks)")

    choice = int(input("Enter the number of the file you want to download: "))
    chosen_id = keys[choice]
    filename = shared_files[chosen_id]["filename"]
    total_chunks = shared_files[chosen_id]["total_chunks"]

    # Create temp chunk folder
    temp_chunk_dir = f"temp_chunks_{chosen_id}"
    os.makedirs(temp_chunk_dir, exist_ok=True)

    print(f"\n⏬ Downloading '{filename}' from peer...")
    for i in range(total_chunks):
        chunk_data = request_chunk(chosen_id, i)
        if chunk_data:
            chunk_path = os.path.join(temp_chunk_dir, f"{chosen_id}_{i}")
            with open(chunk_path, "wb") as f:
                f.write(chunk_data)
        else:
            print(f"[!] Failed to get chunk {i}, stopping...")
            return

    # Reconstruct file
    output_path = os.path.join(DOWNLOADS_DIR, f"downloaded_{filename}")
    reconstruct_file(chosen_id, total_chunks, output_path, chunk_dir=temp_chunk_dir)
    print(f"\n✅ File reconstructed: {output_path}")

    # Clean up temp chunks
    for f in os.listdir(temp_chunk_dir):
        os.remove(os.path.join(temp_chunk_dir, f))
    os.rmdir(temp_chunk_dir)

if __name__ == "__main__":
    main()
