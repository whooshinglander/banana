from flask import Flask, render_template, request, jsonify
import json
import os
import pathlib

app = Flask(__name__)

class StockTracker:
    def __init__(self, data_dir="data"):
        self.data_dir = data_dir
        self.transactions_file = os.path.join(data_dir, "transactions.json")
        self._ensure_data_files_exist()

    def _ensure_data_files_exist(self):
        pathlib.Path(self.data_dir).mkdir(parents=True, exist_ok=True)
        if not os.path.exists(self.transactions_file):
            self._save_transactions([])

    def _load_transactions(self):
        try:
            with open(self.transactions_file, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError:
            return []

    def _save_transactions(self, transactions):
        with open(self.transactions_file, 'w') as f:
            json.dump(transactions, f, indent=4)

    def add_transaction(self, transaction):
        transactions = self._load_transactions()
        transactions.append(transaction)
        self._save_transactions(transactions)

    def get_transactions(self):
        return self._load_transactions()

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
    transaction = {
        "date": request.form['date'],
        "ticker": request.form['ticker'],
        "quantity": int(request.form['quantity']),
        "price": float(request.form['price']),
        "transactionType": request.form['transactionType'],
        "notes": request.form.get('notes', '')  # Capture notes field, default to empty if not provided
    }
    # Add transaction to JSON file
    tracker.add_transaction(transaction)
    return "Transaction added successfully!"

# Route to display stored transactions
@app.route('/transactions', methods=['GET'])
def get_transactions():
    transactions = tracker.get_transactions()
    return jsonify(transactions)

if __name__ == '__main__':
    app.run(debug=True)
