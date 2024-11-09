from flask import Blueprint, render_template, request, redirect, url_for, flash
from src.models.transaction import load_transactions, save_transaction
from src.models.portfolio import get_current_prices, calculate_average_cost
from collections import defaultdict
import yfinance as yf

transaction_bp = Blueprint('transaction', __name__)

@transaction_bp.route('/')
def index():
    transactions = load_transactions()
    holdings = defaultdict(lambda: {'amount': 0, 'total_value': 0, 'average_cost': 0})

    for trans in transactions:
        ticker = trans['stockTicker']
        holdings[ticker]['amount'] += trans['amount']
        holdings[ticker]['total_value'] += trans['amount'] * trans['pricePerShare']

    current_prices = get_current_prices(list(holdings.keys()))
    for ticker, data in holdings.items():
        data['current_price'] = current_prices.get(ticker, 0)
        data['average_cost'] = calculate_average_cost(ticker, transactions)

    return render_template('transaction.html', holdings=holdings)

@transaction_bp.route('/add_transaction', methods=['POST'])
def add_transaction():
    stock_ticker = request.form['stockTicker']
    amount = int(request.form['amount'])
    price_per_share = float(request.form['pricePerShare'])

    # Validate ticker using yfinance
    stock = yf.Ticker(stock_ticker)
    if not stock.info or 'symbol' not in stock.info:
        flash("Invalid stock ticker. Please select a valid ticker from the dropdown.")
        return redirect(url_for('transaction.index'))

    # If valid, save the transaction
    data = {
        'date': request.form['date'],
        'stockTicker': stock_ticker,
        'amount': amount,
        'pricePerShare': price_per_share
    }
    save_transaction(data)
    return redirect(url_for('transaction.index'))
