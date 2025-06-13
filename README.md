# 🧩 P2P File Sharing System (Multithreaded)

A lightweight Peer-to-Peer (P2P) file sharing system built using Python. This system supports:

- File splitting and chunked sharing  
- Multithreaded downloading from a peer  
- Chunk-level communication using TCP sockets  
- Basic Base64-encoded chunk transmission  
- File reconstruction after download

---

## 🚀 Features Implemented So Far

### ✅ File Splitting
- Original files are split into fixed-size chunks.
- Each chunk is stored locally under `chunks/`.
- Metadata like `file_id`, total number of chunks, and filename is recorded in `shared_files.json`.

### ✅ Peer Server (`peer.py`)
- Listens for incoming TCP connections on port `9000`.
- Serves requested file chunks based on file ID and chunk index.
- Sends chunk data as Base64-encoded JSON packets.

### ✅ Client Downloader (`download_full_fileMT.py`)
- Loads `shared_files.json` to display available files.
- Downloads all chunks of a file **in parallel** using Python’s `ThreadPoolExecutor`.
- Reconstructs the file using received chunks.
- Saves the result in the `downloads/` folder with a `downloaded_` prefix.

```

## 📁 Project Structure
p2p_project/
|──src
  ├── peer.py              # Runs the server for this peer
  ├── client.py            # Downloads chunks from other peers
  ├── file_utils.py        # Utilities to split and join files
  ├── chunks/              # Stores local file chunks
  ├── downloads/           # Contains fully reconstructed/downloaded files
  ├── shared_files.json    # Metadata: file IDs, names, and their chunks
  ├── download_full_file.py        # Utilities to split and join files
  ├── download_full_fileMT.py        # Utilities to split and join files
  └── test_chunking.py     # Script to test chunking functionality
|README.md

```

## 🛠️ How to Run

### 1. 🧩 Split a File

```bash
# In Python
from file_utils import split_file
split_file("your_file.txt")

```
### 2.start the Peer server
```bash
# In Python
python src/peer.py

```
### ⬇️ Run the Multithreaded Client
```bash
# In Python
python src/download_full_fileMT.py

```
## Requirements 
Python 3.7+
No external libraries(only built-in:socket,json,base64,threading)

### 📦 Future Additions (Planned)
✅ Retry mechanism for failed chunk transfers

✅ SHA-256 hash-based file integrity verification

⏳ Peer discovery via broadcasting

⏳ GUI interface (Tkinter or CLI improvements)

⏳ Multiple peer file sourcing (swarm download)

### 🤝 Contributing
We’re still developing! Open to suggestions, pull requests, and improvements. You can:

Fix bugs

Add enhancements (progress bar, retry logic)

Help with cross-platform packaging

### Licence
This project is MIT Licensed. Free to use, modify, and share.