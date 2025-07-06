import yfinance as yf
import pandas as pd

def get_stock_data(ticker, period='3mo', interval='1d'):
    stock = yf.Ticker(ticker)
    df = stock.history(period=period, interval=interval)
    return df

def calculate_macd(df):
    df['EMA12'] = df['Close'].ewm(span=12, adjust=False).mean()
    df['EMA26'] = df['Close'].ewm(span=26, adjust=False).mean()
    df['MACD'] = df['EMA12'] - df['EMA26']
    df['Signal_Line'] = df['MACD'].ewm(span=9, adjust=False).mean()
    return df

def calculate_ema9(df):
    df['EMA9'] = df['Close'].ewm(span=9, adjust=False).mean()
    return df

def get_last_row(df):
    return df.iloc[-1] if not df.empty else None

def main():
    ticker = input("Enter stock ticker (e.g., AAPL, MSFT, TSLA): ").upper()

    try:
        df = get_stock_data(ticker)
        if df.empty:
            print("No data found for ticker:", ticker)
            return

        df = calculate_macd(df)
        df = calculate_ema9(df)

        # Show the last 5 rows
        #print("\n--- Latest MACD and EMA9 values ---")
        #print(df[['Close', 'EMA9', 'MACD', 'Signal_Line']].tail())

        last_row = get_last_row(df)
        if last_row is not None and 'Close' in last_row:
            # Assuming you want to display the Close price formatted
            display(f"{ticker} Latest MACD: {last_row['MACD']:.2f}")
            display(f"{ticker} Latest EMA9: {last_row['EMA9']:.2f}")
        elif last_row is not None:
             display(last_row) # Display the entire last row if 'Close' is not available

    except Exception as e:
        print("Error:", str(e))
if __name__ == "__main__":
    main()