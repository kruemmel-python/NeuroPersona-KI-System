import yfinance as yf

# Historische Daten für eine Aktie (z.B. Apple)
data = yf.download("AAPL", start="2022-01-01", end="2023-01-01")
print(data)
