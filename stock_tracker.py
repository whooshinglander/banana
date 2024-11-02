from flask import Flask, render_template, request, jsonify
import json
import os
import pathlib
import time

app = Flask(__name__)

class StockTracker:
    def __init__(self, data_dir="data"):
        self.data_dir = data_dir
        self._ensure_data_files_exist()

    def _ensure_data_files_exist(self):
        pathlib.Path(self.data_dir).mkdir(parents=True, exist_ok=True)

    def _load_transactions(self, file_path):
        try:
            with open(file_path, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return []

    def _save_transactions(self, file_path, transaction):
        with open(file_path, 'w') as f:
            json.dump(transaction, f, indent=4)

    def add_transaction(self, transaction):
        # Generate a unique filename based on the current timestamp
        timestamp = int(time.time())
        file_name = f"transaction_{timestamp}.json"
        file_path = os.path.join(self.data_dir, file_name)

        # Save the transaction to a new JSON file
        self._save_transactions(file_path, transaction)

    def get_transactions(self):
        # List all transaction files in the data directory
        transactions = []
        for file_name in os.listdir(self.data_dir):
            if file_name.startswith("transaction_") and file_name.endswith(".json"):
                file_path = os.path.join(self.data_dir, file_name)
                transactions.append(self._load_transactions(file_path))
        return transactions

# Initialize StockTracker instance
tracker = StockTracker()

# Route to serve the HTML form
@app.route('/')
def index():
    return render_template('transaction_form.html')

# Route to handle form submission
@app.route('/submit', methods=['POST'])
def submit():
    # Get form data
    transaction_type = request.form['transactionType']
    quantity = int(request.form['quantity'])

    # If the transaction type is 'sell', make the quantity negative
    if transaction_type == 'sell':
        quantity = -abs(quantity)

    transaction = {
        "date": request.form['date'],
        "ticker": request.form['ticker'],
        "quantity": quantity,
        "price": float(request.form['price']),
        "transactionType": transaction_type,
        "currency": request.form['currency'],
        "commission": float(request.form['commission']),
        "notes": request.form.get('notes', '')  # Capture notes field, default to empty if not provided
    }
    
    # Add transaction to a new JSON file
    tracker.add_transaction(transaction)
    return jsonify({"message": "Transaction added successfully!"}), 201

# Route to display stored transactions
@app.route('/transactions', methods=['GET'])
def get_transactions():
    transactions = tracker.get_transactions()
    return jsonify(transactions), 200

# Route to serve the calendar view
@app.route('/calendar', methods=['GET'])
def calendar():
    return render_template('calendar.html')

if __name__ == '__main__':
    app.run(debug=True)
