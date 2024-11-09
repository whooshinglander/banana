from flask import Flask
from src.routes.ticker_routes import ticker_bp
from src.routes.portfolio_routes import portfolio_bp
from src.routes.transaction_routes import transaction_bp

app = Flask(__name__, template_folder='src/templates')

# Register blueprints for modular routes
app.register_blueprint(ticker_bp)
app.register_blueprint(portfolio_bp)
app.register_blueprint(transaction_bp)

if __name__ == '__main__':
    app.run(debug=True)
