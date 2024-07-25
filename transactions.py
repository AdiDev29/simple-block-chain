import json
import time
from datetime import datetime
import os
import fcntl

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

def get_latest_block(blocks):
    for block_name, entries in blocks.items():
        if entries[0].get("islatest"):
            return block_name
    return None

def calculate_balance(username, blocks):
    balance = 0.0
    user_found = False
    for block in blocks.values():
        for entry in block:
            if 'user' in entry and 'recipient' in entry and 'amount' in entry:
                if entry['user'] == username:
                    balance -= float(entry['amount'])
                    user_found = True
                elif entry['recipient'] == username:
                    balance += float(entry['amount'])
                    user_found = True
    return balance, user_found

def main():
    while True:
        action = input("Welcome! Check balance (1) or make transaction (2): ")
        if action == "1":
            username = input("Enter your user name: ")
            blocks = load_blocks_from_file()
            balance, user_found = calculate_balance(username, blocks)
            if user_found:
                print(f"The balance for {username} is ${balance:.2f}")
            else:
                print("User not found")
        elif action == "2":
            user = input("Enter or create your user name: ")
            recipient = input("Enter or create your recipient: ")
            amount = input("Enter the amount: ")
            confirm = input(f"You, {user}, are sending ${amount} to {recipient}, confirm? y/n: ")
            if confirm == "y":
                blocks = load_blocks_from_file()
                latest_block = get_latest_block(blocks)
                if latest_block:
                    transaction = {
                        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "user": user,
                        "recipient": recipient,
                        "amount": amount
                    }
                    blocks[latest_block].append(transaction)
                    save_blocks_to_file(blocks)
                    print(f"Transaction added to {latest_block}: {transaction}")
                else:
                    print("No blocks available to add the transaction.")
            else:
                print("You canceled!")
                time.sleep(1)

if __name__ == "__main__":
    main()