import pandas as pd
import yfinance as yf
import pandas_ta as ta
import warnings

# Ignore FutureWarnings
warnings.filterwarnings("ignore", category=FutureWarning)

period = "1y"
interval = "1d"
# Define the ticker symbols
ndxt_symbols = ['AAPL', 'MSFT', 'AMZN', 'GOOGL', 'GOOG', 'TSLA', 'NVDA']

df_all = pd.DataFrame(columns = ['Stock', 'Open', 'High', 'Low', 'Close', 'Volume', 'SMA150', 'SMA100', 'SMA20', 'RSI'])
for ticker in ndxt_symbols:
    # Download the data from Yahoo Finance for the ticker and specified period
    data = yf.download(ticker, period=period, interval=interval)

    # Remove this month's data
    data = data[data.index.month != pd.Timestamp.now().month]

    # Calculate the 150-day, 100-day and 20-day SMA for the stock using pandas
    sma150 = data["Close"].rolling(150).mean()
    sma100 = data["Close"].rolling(100).mean()
    sma20 = data["Close"].rolling(20).mean()

    # Calculate the RSI for the stock using pandas_ta
    rsi = ta.rsi(data["Close"], length=14)


    # Create a pandas DataFrame with the data
    df = pd.DataFrame({'Stock': ticker,'Open': data['Open'],'High': data['High'],'Low': data['Low'],'Close': data['Close'],
                       'Volume': data['Volume'],'SMA150': sma150, 'SMA100': sma100, 'SMA20': sma20, 'RSI': rsi})
    df_all = df_all._append(df)

# Rename the index column to "Date"
df_all = df_all.rename_axis("Date")

# Save the DataFrame to a csv file
df_all.to_csv('output.csv', index=True)