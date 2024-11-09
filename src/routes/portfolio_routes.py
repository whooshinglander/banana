from flask import Blueprint, jsonify
from src.models.portfolio import calculate_daily_portfolio_values

# Initialize the blueprint for portfolio-related routes
portfolio_bp = Blueprint('portfolio', __name__)

@portfolio_bp.route('/portfolio_values')
def portfolio_values():
    dates, values = calculate_daily_portfolio_values()
    return jsonify({'dates': [date.strftime('%Y-%m-%d') for date in dates], 'values': values})
