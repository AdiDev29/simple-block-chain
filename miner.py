import hashlib
import json
import re
import os
import fcntl
import time

def load_blocks_from_file(filename='ledger.json'):
    if os.path.exists(filename):
        with open(filename, 'r') as file:
            fcntl.flock(file, fcntl.LOCK_SH)
            try:
                blocks = json.load(file)
            except json.JSONDecodeError:
                blocks = {}
            fcntl.flock(file, fcntl.LOCK_UN)
        return blocks
    return {}

def save_blocks_to_file(blocks, filename='ledger.json'):
    with open(filename, 'w') as file:
        fcntl.flock(file, fcntl.LOCK_EX)
        json.dump(blocks, file, indent=4)
        fcntl.flock(file, fcntl.LOCK_UN)

def get_unhashed_blocks(blocks):
    unhashed_blocks = []
    for blocks_name, entries in blocks.items():
        if not entries[0].get("hash") and not entries[0].get("islatest"):
            unhashed_blocks.append((blocks_name, entries))
    unhashed_blocks.sort(key=lambda x: x[1][0]["date"])  # Sort by date
    return unhashed_blocks

def get_previous_hash(blocks, current_index):
    if current_index == 0:
        return "0" * 64  # Initial hash value for the first blocks (SHA-256 produces 64 characters)
    previous_blocks_name = f"blocks{current_index}"
    return blocks[previous_blocks_name][0].get("hash", "0" * 64)

def mine_blocks(blocks, previous_hash):
    stamp = 0
    blocks_content = json.dumps(blocks, sort_keys=True)
    while True:
        combined = blocks_content + previous_hash + str(stamp)
        cipher = hashlib.sha256(combined.encode())
        if re.match("^0{5}", cipher.hexdigest()):  # Assuming a difficulty of 5 leading zeros
            return cipher.hexdigest(), stamp
        stamp += 1

def main():
    while True:
        blocks = load_blocks_from_file()
        unhashed_blocks = get_unhashed_blocks(blocks)
        
        for index, (blocks_name, blocks_entries) in enumerate(unhashed_blocks):
            previous_hash = get_previous_hash(blocks, index)
            blocks_hash, blocks_stamp = mine_blocks(blocks_entries, previous_hash)
            blocks_entries[0]["hash"] = blocks_hash
            blocks_entries[0]["stamp"] = blocks_stamp
            save_blocks_to_file(blocks)
            print(f"blocks {blocks_name} updated with hash: {blocks_hash} and stamp: {blocks_stamp}")
        
        time.sleep(10)  # Wait for 10 seconds before checking again

if __name__ == "__main__":
    main()