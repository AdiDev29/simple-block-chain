import json
from flask import Flask, jsonify, render_template
from flask_socketio import SocketIO, emit
import time
import os
import fcntl

app = Flask(__name__)
app.config['SECRET_KEY'] = '18889999'  # Replace with a strong secret key
socketio = SocketIO(app)

# Global variables to store ledger data
blocks = {}
transactions = []
users = {}

# Load blockchain data from ledger.json
def load_ledger_data():
    with open('ledger.json', 'r') as f:
        fcntl.flock(f, fcntl.LOCK_SH)
        try:
            ledger_data = json.load(f)
        except json.JSONDecodeError:
            ledger_data = {}
        fcntl.flock(f, fcntl.LOCK_UN)
    return ledger_data

# Extract blocks, transactions, and users from ledger_data
def process_ledger_data(ledger_data):
    blocks = ledger_data
    transactions = []
    users = {}

    # Extract transactions from blocks
    for block_name in blocks:
        block = blocks[block_name]
        for entry in block:
            if 'user' in entry:
                transactions.append(entry)

    # Calculate user balances
    for transaction in transactions:
        user = transaction['user']
        recipient = transaction['recipient']
        amount = int(transaction['amount'])

        if user not in users:
            users[user] = 0
        if recipient not in users:
            users[recipient] = 0

        users[user] -= amount
        users[recipient] += amount

    return blocks, transactions, users

# API endpoints
@app.route('/blocks')
def get_blocks():
    global blocks
    return jsonify(blocks)

@app.route('/transactions')
def get_transactions():
    global transactions
    return jsonify(transactions)

@app.route('/users')
def get_users():
    global users
    return jsonify(users)

# Render the HTML template
@app.route('/')
def index():
    return render_template('index.html')

# SocketIO event to update data
@socketio.event
def connect():
    print('Client connected')
    ledger_data = load_ledger_data()
    global blocks, transactions, users
    blocks, transactions, users = process_ledger_data(ledger_data)
    emit('update_data', {'blocks': blocks, 'transactions': transactions, 'users': users})

@socketio.event
def disconnect():
    print('Client disconnected')

# Background task to periodically update data
def update_data():
    global blocks, transactions, users
    while True:
        time.sleep(5)  # Update every 5 seconds
        ledger_data = load_ledger_data()
        blocks, transactions, users = process_ledger_data(ledger_data)
        socketio.emit('update_data', {'blocks': blocks, 'transactions': transactions, 'users': users}, broadcast=True)

# Start the background task
socketio.start_background_task(update_data)

# Run the app
if __name__ == '__main__':
    ledger_data = load_ledger_data()
    blocks, transactions, users = process_ledger_data(ledger_data)
    socketio.run(app, debug=True)
