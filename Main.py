import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import ta

# Define the ticker symbol and timeframe
ticker_symbol = "TSLA"  # Example: Apple Inc.
start_date = "2024-01-01"
end_date = "2025-01-01"

# Fetch historical market data
data = yf.download(ticker_symbol, start=start_date, end=end_date)

# Calculate Bollinger Bands
bb_period = 20
bb_std = 2
data['BB_Middle'] = ta.volatility.bollinger_mavg(data['Close'], window=bb_period)
data['BB_Std'] = ta.volatility.bollinger_mavg(data['Close'], window=bb_period, fillna=True).rolling(bb_period).std()
data['BB_Upper'] = data['BB_Middle'] + bb_std * data['BB_Std']
data['BB_Lower'] = data['BB_Middle'] - bb_std * data['BB_Std']

# Generate buy/sell signals
data['Signal'] = 0
data['Signal'][data['Close'] < data['BB_Lower']] = 1  # Buy signal when price is below lower band
data['Signal'][data['Close'] > data['BB_Upper']] = -1  # Sell signal when price is above upper band
data['Position'] = data['Signal'].diff()

# Plot
plt.figure(figsize=(10, 5))
plt.plot(data['Close'], label='Price')
plt.plot(data['BB_Middle'], label='Middle Band')
plt.plot(data['BB_Upper'], label='Upper Band', linestyle='--', color='g')
plt.plot(data['BB_Lower'], label='Lower Band', linestyle='--', color='r')

plt.title('Bollinger Bands Strategy for ' + ticker_symbol)
plt.legend()
plt.show()
