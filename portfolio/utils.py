import yfinance as yf

def get_stock_price(stock_name):
    try:
        stock = yf.Ticker(stock_name + ".NS")  # NSE stocks
        data = stock.history(period="1d")

        if not data.empty:
            return float(data['Close'].iloc[-1])

    except Exception as e:
        print("Error fetching price:", e)

    return 0