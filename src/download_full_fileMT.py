import json
import os
import socket
import base64
from concurrent.futures import ThreadPoolExecutor, as_completed

CHUNK_DIR = "chunks"
DOWNLOAD_DIR = "downloads"
METADATA_FILE = "shared_files.json"
PEER_IP = "127.0.0.1"
PEER_PORT = 9000
MAX_THREADS = 5

os.makedirs(DOWNLOAD_DIR, exist_ok=True)


def load_metadata():
    with open(METADATA_FILE, "r") as f:
        return json.load(f)


def request_chunk(file_id, chunk_index):
    request = {
        "type": "REQUEST_CHUNK",
        "file_id": file_id,
        "chunk_index": chunk_index
    }

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((PEER_IP, PEER_PORT))
            s.send(json.dumps(request).encode())

            # Receive the response (handle fragmented or large responses)
            buffer = b""
            while True:
                data = s.recv(4096)
                if not data:
                    break
                buffer += data

            response = buffer.decode(errors="ignore")
            response_data = json.loads(response)

            if response_data["type"] == "CHUNK_DATA":
                decoded_data = base64.b64decode(response_data["data"])
                return chunk_index, decoded_data
            else:
                raise Exception(response_data.get("message", "Unknown error"))
    except Exception as e:
        print(f"[!] Exception on chunk {chunk_index}: {e}")
        return chunk_index, None


def reconstruct_file(file_id, chunks_data, output_path):
    chunks_data.sort()  # Sort by chunk index
    with open(output_path, "wb") as f:
        for _, data in chunks_data:
            if data:
                f.write(data)


def main():
    metadata = load_metadata()
    file_keys = list(metadata.keys())

    print("Available Files:")
    for idx, file_id in enumerate(file_keys):
        info = metadata[file_id]
        print(f"[{idx}] {info['filename']} ({info['total_chunks']} chunks)")

    choice = int(input("Enter the number of the file you want to download: "))
    selected_file_id = file_keys[choice]
    filename = metadata[selected_file_id]['filename']
    total_chunks = metadata[selected_file_id]['total_chunks']

    print(f"\n⏬ Downloading '{filename}' from peer...\n")

    chunks = []

    with ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
        futures = [executor.submit(request_chunk, selected_file_id, i) for i in range(total_chunks)]
        for future in as_completed(futures):
            chunk_result = future.result()
            if chunk_result[1] is None:
                print(f"[!] Failed to get chunk {chunk_result[0]}, stopping...")
                return
            chunks.append(chunk_result)

    output_path = os.path.join(DOWNLOAD_DIR, f"downloaded_{filename}")
    reconstruct_file(selected_file_id, chunks, output_path)
    print(f"\n✅ File reconstructed: {output_path}")


if __name__ == "__main__":
    main()
