import random

def get_stock_price(stock_name):
    # Mock prices (simulate real market)
    mock_prices = {
        "TCS": 3500,
        "INFY": 1500,
        "RELIANCE": 2800,
        "HDFCBANK": 1600,
    }

    return mock_prices.get(stock_name.upper(), random.randint(100, 1000))