import json
import os
import csv
from datetime import datetime
import uuid
from typing import Dict, List, Optional, Union
import pathlib
import shutil

class StockTracker:
    def __init__(self, data_dir: str = "data"):
        """Initialize StockTracker with a data directory"""
        self.data_dir = data_dir
        self.transactions_file = os.path.join(data_dir, "transactions.json")
        self._ensure_data_files_exist()
    
    def _ensure_data_files_exist(self):
        """Ensure the data directory and files exist"""
        pathlib.Path(self.data_dir).mkdir(parents=True, exist_ok=True)
        if not os.path.exists(self.transactions_file):
            self._save_transactions([])
    
    def _load_transactions(self) -> List[Dict]:
        """Load transactions from JSON file"""
        try:
            with open(self.transactions_file, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError:
            return []
    
    def _save_transactions(self, transactions: List[Dict]):
        """Save transactions to JSON file"""
        with open(self.transactions_file, 'w') as f:
            json.dump(transactions, f, indent=2, default=str)
    
    def _validate_transaction(self, transaction: Dict) -> List[str]:
        """Validate transaction data"""
        errors = []
        
        # Required fields
        required_fields = ["symbol", "amount", "price", "commission", "currency", "portfolio_id"]
        for field in required_fields:
            if field not in transaction or transaction[field] is None:
                errors.append(f"Missing required field: {field}")
        
        # Value validations
        if "amount" in transaction and transaction["amount"] == 0:
            errors.append("Amount cannot be zero")
        
        if "price" in transaction and transaction["price"] <= 0:
            errors.append("Price must be positive")
            
        if "commission" in transaction and transaction["commission"] < 0:
            errors.append("Commission cannot be negative")
        
        return errors
    
    def add_transaction(self, transaction_data: Dict) -> Dict:
        """
        Add a new transaction
        
        Args:
            transaction_data: Dictionary containing transaction details
            Required fields: symbol, amount, price, commission, currency, portfolio_id
            Optional fields: notes, date
        """
        # Validate transaction data
        errors = self._validate_transaction(transaction_data)
        if errors:
            raise ValueError(f"Invalid transaction data: {', '.join(errors)}")
        
        # Create new transaction
        transaction = {
            "transaction_id": str(uuid.uuid4()),
            "date": transaction_data.get("date") or datetime.now().isoformat(),
            "symbol": transaction_data["symbol"].upper(),
            "amount": float(transaction_data["amount"]),
            "price": float(transaction_data["price"]),
            "commission": float(transaction_data["commission"]),
            "currency": transaction_data["currency"].upper(),
            "portfolio_id": transaction_data["portfolio_id"],
            "notes": transaction_data.get("notes")
        }
        
        transactions = self._load_transactions()
        transactions.append(transaction)
        self._save_transactions(transactions)
        
        return transaction
    
    def update_transaction(self, transaction_id: str, updates: Dict) -> Optional[Dict]:
        """Update an existing transaction"""
        transactions = self._load_transactions()
        
        for i, transaction in enumerate(transactions):
            if transaction["transaction_id"] == transaction_id:
                # Create updated transaction
                updated_transaction = transaction.copy()
                updated_transaction.update(updates)
                
                # Validate updated transaction
                errors = self._validate_transaction(updated_transaction)
                if errors:
                    raise ValueError(f"Invalid update data: {', '.join(errors)}")
                
                # Apply updates
                if "symbol" in updates:
                    updated_transaction["symbol"] = updates["symbol"].upper()
                if "currency" in updates:
                    updated_transaction["currency"] = updates["currency"].upper()
                
                transactions[i] = updated_transaction
                self._save_transactions(transactions)
                return updated_transaction
        
        return None
    
    def delete_transaction(self, transaction_id: str) -> bool:
        """Delete a transaction"""
        transactions = self._load_transactions()
        initial_count = len(transactions)
        
        transactions = [t for t in transactions if t["transaction_id"] != transaction_id]
        
        if len(transactions) < initial_count:
            self._save_transactions(transactions)
            return True
        return False
    
    def get_transaction(self, transaction_id: str) -> Optional[Dict]:
        """Get a specific transaction by ID"""
        transactions = self._load_transactions()
        for transaction in transactions:
            if transaction["transaction_id"] == transaction_id:
                return transaction
        return None
    
    def get_all_transactions(self) -> List[Dict]:
        """Get all transactions"""
        return self._load_transactions()
    
    def export_to_csv(self, filename: str):
        """Export all transactions to CSV file"""
        transactions = self._load_transactions()
        if not transactions:
            raise ValueError("No transactions to export")
        
        fieldnames = ["transaction_id", "date", "symbol", "amount", "price", 
                     "commission", "currency", "portfolio_id", "notes"]
        
        with open(filename, 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(transactions)
    
    def export_to_json(self, filename: str):
        """Export all transactions to JSON file"""
        transactions = self._load_transactions()
        if not transactions:
            raise ValueError("No transactions to export")
        
        with open(filename, 'w') as f:
            json.dump(transactions, f, indent=2, default=str)
    
    def import_from_csv(self, filename: str) -> List[Dict]:
        """Import transactions from CSV file"""
        imported_transactions = []
        
        with open(filename, 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                # Convert string values to appropriate types
                transaction_data = {
                    "symbol": row["symbol"],
                    "amount": float(row["amount"]),
                    "price": float(row["price"]),
                    "commission": float(row["commission"]),
                    "currency": row["currency"],
                    "portfolio_id": row["portfolio_id"],
                    "notes": row["notes"] if row["notes"] != "" else None,
                    "date": row["date"]
                }
                
                imported_transaction = self.add_transaction(transaction_data)
                imported_transactions.append(imported_transaction)
        
        return imported_transactions
    
    def import_from_json(self, filename: str) -> List[Dict]:
        """Import transactions from JSON file"""
        with open(filename, 'r') as f:
            transactions = json.load(f)
        
        imported_transactions = []
        for transaction_data in transactions:
            # Remove transaction_id if present to generate new one
            transaction_data.pop("transaction_id", None)
            imported_transaction = self.add_transaction(transaction_data)
            imported_transactions.append(imported_transaction)
        
        return imported_transactions
    
    def backup_data(self, backup_dir: str = "backups"):
        """Create a backup of the transactions file"""
        pathlib.Path(backup_dir).mkdir(parents=True, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = os.path.join(backup_dir, f"transactions_backup_{timestamp}.json")
        
        shutil.copy2(self.transactions_file, backup_file)
        return backup_file

# Example usage
def main():
    # Create StockTracker instance
    tracker = StockTracker()
    
    # Add sample transactions
    transaction1 = tracker.add_transaction({
        "symbol": "AAPL",
        "amount": 10,
        "price": 150.50,
        "commission": 4.95,
        "currency": "USD",
        "portfolio_id": "portfolio1",
        "notes": "Initial purchase"
    })
    
    transaction2 = tracker.add_transaction({
        "symbol": "GOOGL",
        "amount": 5,
        "price": 2800.00,
        "commission": 4.95,
        "currency": "USD",
        "portfolio_id": "portfolio1",
        "notes": "Adding Google"
    })
    
    # Export to CSV and JSON
    tracker.export_to_csv("transactions_export.csv")
    tracker.export_to_json("transactions_export.json")
    
    # Update a transaction
    tracker.update_transaction(transaction1["transaction_id"], {
        "amount": 15,
        "notes": "Updated purchase"
    })
    
    # Delete a transaction
    tracker.delete_transaction(transaction2["transaction_id"])
    
    # Create backup
    backup_file = tracker.backup_data()
    print(f"Backup created: {backup_file}")
    
    # Import from CSV (after clearing data for demonstration)
    tracker._save_transactions([])  # Clear existing data
    imported_transactions = tracker.import_from_csv("transactions_export.csv")
    print(f"Imported {len(imported_transactions)} transactions from CSV")

if __name__ == "__main__":
    main()