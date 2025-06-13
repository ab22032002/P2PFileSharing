from file_utils import split_file, reconstruct_file

# Create a big test file (~2.5MB)
with open("big_sample2.txt", "w") as f:
    f.write("Hello P2P!\n" * 300_0000)

# Split the file into chunks
file_id, total_chunks = split_file("big_sample2.txt")

print(f"File ID: {file_id}")
print(f"Total Chunks Created: {total_chunks}")

# Reconstruct the file
reconstruct_file(file_id, total_chunks, "rejoined_big_sample2.txt")

print("Reconstructed file saved in 'downloads/rejoined_big_sample2.txt'")
