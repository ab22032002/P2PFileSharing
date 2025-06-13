import os
import hashlib

CHUNK_DIR = "chunks"
DOWNLOAD_DIR = "downloads"

def get_file_hash(file_path):
    """Generate a unique SHA-256 hash for a file (used as file_id)"""
    hasher = hashlib.sha256()
    with open(file_path, "rb") as f:
        while chunk := f.read(8192):
            hasher.update(chunk)
    return hasher.hexdigest()

def split_file(file_path, chunk_size=1024*1024):  # 1MB default
    """Splits a file into fixed-size chunks and saves them in chunks/"""
    if not os.path.exists(CHUNK_DIR):
        os.makedirs(CHUNK_DIR)

    file_id = get_file_hash(file_path)
    with open(file_path, "rb") as f:
        index = 0
        while chunk := f.read(chunk_size):
            chunk_filename = f"{file_id}_{index}"
            with open(os.path.join(CHUNK_DIR, chunk_filename), "wb") as chunk_file:
                chunk_file.write(chunk)
            index += 1
    
    save_file_metadata(file_id, os.path.basename(file_path), index)
    return file_id, index  # file_id and total number of chunks

def reconstruct_file(file_id, total_chunks, output_path, chunk_dir="chunks"):
    with open(output_path, "wb") as output_file:
        for i in range(total_chunks):
            chunk_path = os.path.join(chunk_dir, f"{file_id}_{i}")
            with open(chunk_path, "rb") as chunk_file:
                output_file.write(chunk_file.read())


import json

METADATA_FILE = "shared_files.json"

def save_file_metadata(file_id, filename, total_chunks):
    metadata = {}
    if os.path.exists("shared_files.json"):
        with open("shared_files.json", "r") as f:
            try:
                metadata = json.load(f)
            except json.JSONDecodeError:
                pass

    metadata[file_id] = {
        "filename": filename,
        "total_chunks": total_chunks
    }

    with open("shared_files.json", "w") as f:
        json.dump(metadata, f, indent=4)
