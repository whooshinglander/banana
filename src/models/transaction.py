import json
import os
import uuid

DATA_DIR = 'data'

def load_transactions():
    transactions = []
    for filename in os.listdir(DATA_DIR):
        filepath = os.path.join(DATA_DIR, filename)
        if os.path.isfile(filepath) and filename.endswith('.json'):
            with open(filepath, 'r') as f:
                try:
                    transaction = json.load(f)
                    if all(key in transaction for key in ['stockTicker', 'amount', 'pricePerShare']):
                        transactions.append(transaction)
                except json.JSONDecodeError:
                    print(f"Error decoding JSON from file {filename}")
    return transactions

def save_transaction(data):
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
    unique_id = uuid.uuid4()
    filename = os.path.join(DATA_DIR, f'{unique_id}.json')
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)
