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
├── file_utils.py        # 🧩 Split/join files
├── chunks/              # 📂 Stores local chunks
├── downloads/           # 📥 Final reconstructed files
├── shared_files.json    # 📃 List of local shared files (file_id, name, chunks)
└── test_chunking.py     # 🧪 Optional testing script
