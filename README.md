# Simple Blockchain Project

## Overview

This project demonstrates a very simple blockchain implementation. The blockchain is represented using JSON files, and it includes basic functionalities such as adding transactions, checking balances, and mining blocks. I made this project to help me better understand how blockchains work.

## Specifications

### Components

1. **Ledger Creation Script (`ledgers.py`)**
   - Continuously creates new ledgers every minute.
   - Marks the latest ledger with `"islatest": true`.
   - Saves the ledgers to a JSON file (`ledgers.json`).

2. **Transaction Script (`transactions.py`)**
   - Allows users to add transactions to the latest ledger.
   - Provides functionality to check the balance of a user by summing the amounts received and sent.
   - Updates the JSON file (`ledgers.json`) with new transactions.

3. **Mining Script (`mining.py`)**
   - Continuously checks for ledgers that are not hashed and not marked as the latest.
   - Mines these ledgers by finding a `stamp` that generates a valid hash with a certain difficulty (e.g., leading zeros).
   - Updates the JSON file (`ledgers.json`) with the `stamp` and `hash` values.

4. **Blockchain Explorer (`data_grabber.py`, `templates/index.html`)**
   - Provides a web interface to view the blockchain data.
   - Displays blocks, transactions, and user balances.
   - Uses Flask and Socket.IO to serve the web interface and update data in real-time.

### JSON Structure

The ledgers are stored in a JSON file (`ledgers.json`) with the following structure:

```json
{
    "ledger1": [
        {
            "date": "2024-07-24 12:00:00",
            "hash": "",
            "stamp": "",
            "islatest": true
        },
        ...
    ],
    ...
}
```

### Mining Algorithm

The mining algorithm works as follows:
1. Combine the content of the ledger, the hash of the previous ledger, and a `stamp`.
2. Hash the combined string using MD5.
3. Check if the hash meets the difficulty requirement (e.g., starts with 5 zeros).
4. If the hash is valid, store the `stamp` and `hash` in the JSON file.

### Usage

#### Ledger Creation Script

To run the ledger creation script:

```bash
python ledgers.py
```

This script will continuously create new ledgers every minute and save them to `ledgers.json`.

#### Transaction Script

To run the transaction script:

```bash
python transactions.py
```

This script allows users to check their balance or make transactions.

#### Mining Script

To run the mining script:

```bash
python mining.py
```

This script continuously mines new ledgers that are ready to be mined and updates the `ledgers.json` file with the results.

#### Blockchain Explorer

To run the blockchain explorer:

```bash
python data_grabber.py
```

This script starts a Flask web server and serves the blockchain explorer interface at `http://localhost:5000`.

## Conclusion

This simple blockchain project provides a basic implementation of a blockchain using Python and JSON files. It covers the fundamental aspects of blockchain technology, including ledger creation, transaction handling, and mining. This project is a great starting point for anyone looking to learn about blockchains and their underlying principles.

## Changelog

### v1.1
- Added a blockchain explorer with a web interface using Flask and Socket.IO.
- Displays blocks, transactions, and user balances in real-time.
- Added `data_grabber.py` and `templates/index.html` for the web interface.
