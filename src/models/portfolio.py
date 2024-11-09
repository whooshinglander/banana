import yfinance as yf
from src.utils.data_utils import load_transactions
from collections import defaultdict
from datetime import datetime, timedelta

def get_current_prices(tickers):
    """Fetch the latest prices for a list of tickers."""
    prices = {}
    for ticker in tickers:
        stock = yf.Ticker(ticker)
        history = stock.history(period="1d")
        prices[ticker] = history['Close'][-1] if not history.empty else 0
    return prices

def calculate_average_cost(ticker, transactions):
    """Calculate the average cost per share for a given ticker."""
    total_cost = total_amount = 0
    for trans in transactions:
        if trans['stockTicker'] == ticker:
            total_cost += trans['pricePerShare'] * trans['amount']
            total_amount += trans['amount']
    return (total_cost / total_amount) if total_amount else 0

def calculate_daily_portfolio_values():
    """Calculate daily portfolio values based on historical data."""
    transactions = load_transactions()
    holdings = defaultdict(int)

    # Calculate holdings based on transactions
    for trans in transactions:
        ticker = trans['stockTicker']
        holdings[ticker] += trans['amount']

    portfolio_values = defaultdict(float)
    end_date = datetime.now()
    start_date = end_date - timedelta(days=365)  # Last 1 year of data

    for ticker, amount in holdings.items():
        stock = yf.Ticker(ticker)
        history = stock.history(start=start_date, end=end_date)

        for date, row in history.iterrows():
            close_price = row['Close']
            portfolio_values[date] += close_price * amount

    sorted_dates = sorted(portfolio_values.keys())
    sorted_values = [portfolio_values[date] for date in sorted_dates]
    return sorted_dates, sorted_values
