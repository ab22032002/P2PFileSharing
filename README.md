# P2PFileSharing
P2P file sharing Using TCP/IP and concepts of Multithreading
Project Initialization : 
Connecting to Github 
git clone https://github.com/ab22032002/P2PFileSharing.git
cd P2PFileSharing
<hr>
Directory Structure
p2p_project/
├── peer.py              # 👥 Runs the server for this peer
├── client.py            # 📥 Downloads chunks from other peers
├── file_utils.py        # 🧩 Utilities to split and join files
├── chunks/              # 📂 Stores local file chunks
├── downloads/           # 📥 Contains fully reconstructed/downloaded files
├── shared_files.json    # 📃 Metadata: file IDs, names, and their chunks
└── test_chunking.py     # 🧪 Script to test chunking functionality


