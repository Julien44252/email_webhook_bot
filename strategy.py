# strategy.py

import ccxt
import pandas as pd
import ta

# 1) Récupère les données OHLCV depuis l’exchange
def fetch_ohlcv(symbol: str, timeframe: str = "1h", limit: int = 100) -> pd.DataFrame:
    exchange = ccxt.binance()  # ou l’exchange de ton choix
    bars = exchange.fetch_ohlcv(symbol, timeframe=timeframe, limit=limit)
    df = pd.DataFrame(bars, columns=["timestamp", "open", "high", "low", "close", "volume"])
    df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
    df.set_index("timestamp", inplace=True)
    return df

# 2) Calcule tes indicateurs ICT
def compute_indicators(df: pd.DataFrame) -> pd.DataFrame:
    # Ex : un simple RSI
    df["rsi"] = ta.momentum.rsi(df["close"], window=14)
    # Ajoute ici tes pivot points, order blocks, etc.
    return df

# 3) Génère le signal BUY/SELL/NEUTRAL
def generate_signal(df: pd.DataFrame) -> str:
    latest = df.iloc[-1]
    if latest["rsi"] < 30:
        return "BUY"
    elif latest["rsi"] > 70:
        return "SELL"
    else:
        return ""  # pas de signal

# 4) Envoie l’ordre via l’API ccxt
def place_order(symbol: str, side: str, amount: float):
    exchange = ccxt.binance({
        "apiKey":    "TA_CLE_API",
        "secret":    "TON_SECRET",
    })
    order = exchange.create_order(symbol, "market", side, amount)
    return order
