from flask import Blueprint, request, jsonify
import yfinance as yf

ticker_bp = Blueprint('ticker', __name__)

@ticker_bp.route('/search_ticker')
def search_ticker():
    query = request.args.get('q')
    if not query:
        return jsonify([])

    try:
        ticker = yf.Ticker(query)
        ticker_data = ticker.info
        suggestions = []
        if 'symbol' in ticker_data:
            suggestions.append({
                'label': f"{ticker_data['symbol']} - {ticker_data.get('shortName', 'Unknown')}",
                'value': ticker_data['symbol']
            })
        return jsonify(suggestions)
    except Exception as e:
        print(f"Error searching for ticker '{query}': {e}")
        return jsonify([])
