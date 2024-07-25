import json
import time
from datetime import datetime
import fcntl
import os

def create_block_entry():
    return {
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "hash": "",
        "stamp": "",
        "islatest": True
    }

def save_blocks_to_file(blocks, filename='ledger.json'):
    with open(filename, 'w') as file:
        fcntl.flock(file, fcntl.LOCK_EX)
        json.dump(blocks, file, indent=4)
        fcntl.flock(file, fcntl.LOCK_UN)

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

def main():
    while True:
        blocks = load_blocks_from_file()
        block_count = len(blocks) + 1

        for block in blocks.values():
            block[0]["islatest"] = False
        new_block_name = f"block{block_count}"
        blocks[new_block_name] = [create_block_entry()]
        save_blocks_to_file(blocks)
        print(f"Created {new_block_name} with entry: {blocks[new_block_name][0]}")
        time.sleep(30)

if __name__ == "__main__":
    main()