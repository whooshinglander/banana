
# Elephant Stock Portfolio Tracker

A web-based application to manage, track, and visualize a stock portfolio. This app allows users to add transactions, view portfolio holdings, track daily prices, and analyze monthly and yearly portfolio performance with interactive charts.

## Features

- **Transaction Management**: Add stock buy/sell transactions with date, ticker, amount, and price per share.
- **Daily Price Tracking**: Automatically fetches daily closing prices for stocks in the portfolio.
- **Portfolio Holdings Overview**: Displays current stock holdings, including quantity, last known price, and total value.
- **Performance Visualization**: Line charts show portfolio value over time, with monthly and yearly views.

## Project Structure

```
Elephant/
├── data/
│   ├── daily_prices.json          # Daily prices for each stock, updated once daily
│   ├── last_price.json            # Latest price fetched for each stock (if applicable)
│   └── transaction files (.json)  # Individual JSON files storing each transaction
├── src/
│   └── transaction.html           # HTML template with transaction form, portfolio table, and chart
├── dashboard.py                   # Main Flask application with endpoints and logic
└── README.md                      # Project documentation
```

## Setup

### Prerequisites

- Python 3.7 or higher
- Virtual environment (`venv`) setup (optional but recommended)

### Installation

1. **Clone the repository**:

   ```bash
   git clone <repository-url>
   cd Elephant
   ```

2. **Set up a virtual environment** (optional):

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows, use: venv\Scripts\activate
   ```

3. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

### Configuration

1. **API Key**:
   - The application uses Alpha Vantage’s free API to fetch daily prices. No API key setup is needed, as the free demo key is embedded in the code. For production, it is recommended to sign up for your own key [here](https://www.alphavantage.co/support/#api-key).

2. **Data Storage**:
   - All transaction data is stored in `data/` as individual JSON files.
   - Daily prices are saved in `data/daily_prices.json` and update once daily.

## Usage

### Run the Application

```bash
python dashboard.py
```

Open your browser and go to `http://127.0.0.1:5000` to access the application.

### Main Functionalities

1. **Add a New Transaction**:
   - Use the form to enter stock ticker, amount, price per share, and date.
   - Click "Add Transaction" to save.

2. **View Portfolio Holdings**:
   - The main dashboard displays each stock’s ticker, quantity, last price, and total value.
   - A total portfolio value is displayed at the bottom.

3. **View Portfolio Performance**:
   - A line chart displays monthly and yearly portfolio values over time.
   - Values are based on daily prices from `daily_prices.json`.

4. **Update Daily Prices**:
   - Prices are updated once per day using the `/update_prices` endpoint.
   - To trigger a price update manually, navigate to `http://127.0.0.1:5000/update_prices`.

## API Endpoints

- `/` : Main dashboard with transaction form, portfolio holdings table, and performance chart.
- `/add_transaction` : Processes new transactions and adds them to the portfolio.
- `/update_prices` : Updates daily prices for all stocks in the portfolio.
- `/portfolio_values` : Serves monthly and yearly portfolio values for chart rendering.

## Notes

- **Data Limitations**: The free Alpha Vantage API is limited to 5 requests per minute and 500 requests per day. Adjust usage accordingly.
- **Portfolio Analysis**: Data in `daily_prices.json` is used for monthly and yearly analysis, enabling flexibility in performance calculations.

## Future Improvements

- **Enhanced Ticker Validation**: Improve ticker input by adding auto-complete suggestions or validation.
- **Advanced Analytics**: Integrate additional financial metrics, such as dividend tracking and sector allocation.
- **UI Enhancements**: Implement additional visualizations for detailed analysis.

---

This project provides a solid foundation for tracking and analyzing a stock portfolio over time. Let us know if there’s anything else you’d like to add!
