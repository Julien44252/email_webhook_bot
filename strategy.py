# strategy.py
import os
import pandas as pd
import ccxt
from dotenv import load_dotenv

# 1) Charge les clés KuCoin
load_dotenv()
API_KEY    = os.getenv("KUCOIN_API_KEY")
API_SECRET = os.getenv("KUCOIN_API_SECRET")
API_PWD    = os.getenv("KUCOIN_API_PWD")

exchange = ccxt.kucoin({
    "apiKey": API_KEY,
    "secret": API_SECRET,
    "password": API_PWD,
    "enableRateLimit": True,
})

def fetch_ohlcv(symbol: str, timeframe: str = "1h", limit: int = 200) -> pd.DataFrame:
    data = exchange.fetch_ohlcv(symbol, timeframe=timeframe, limit=limit)
    df = pd.DataFrame(data, columns=["timestamp","open","high","low","close","volume"])
    df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
    df.set_index("timestamp", inplace=True)
    return df

def compute_indicators(df: pd.DataFrame,
                       ema_fast: int = 8,
                       ema_slow: int = 21,
                       atr_period: int = 14) -> pd.DataFrame:
    # EMA
    df[f"EMA{ema_fast}"] = df["close"].ewm(span=ema_fast, adjust=False).mean()
    df[f"EMA{ema_slow}"] = df["close"].ewm(span=ema_slow, adjust=False).mean()
    # ATR
    high_low   = df["high"] - df["low"]
    high_close = (df["high"] - df["close"].shift()).abs()
    low_close  = (df["low"]  - df["close"].shift()).abs()
    df["TR"]   = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
    df["ATR"]  = df["TR"].rolling(atr_period).mean()
    return df.dropna()

def generate_signal(df: pd.DataFrame,
                    ema_fast: int = 8,
                    ema_slow: int = 21,
                    atr_trend_mult: float = 1.0) -> str:
    """
    ICT-style : on ne prend BUY que si EMA8 croise au-dessus de EMA21 
    ET la clôture est > ATR*multiplicateur (tendance haussière), 
    sinon SELL.
    """
    last = df.iloc[-1]
    prev = df.iloc[-2]

    # tendance haussière si close > ATR * multiplier
    up_trend   = last["close"] > atr_trend_mult * last["ATR"]
    down_trend = last["close"] < atr_trend_mult * last["ATR"]

    # BUY condition
    if prev[f"EMA{ema_fast}"] < prev[f"EMA{ema_slow}"] \
       and last[f"EMA{ema_fast}"] > last[f"EMA{ema_slow}"] \
       and up_trend:
        return "BUY"

    # SELL condition
    if prev[f"EMA{ema_fast}"] > prev[f"EMA{ema_slow}"] \
       and last[f"EMA{ema_fast}"] < last[f"EMA{ema_slow}"] \
       and down_trend:
        return "SELL"

    return ""

# Pour debug
if __name__ == "__main__":
    sym = "BTC/USDT"
    df = fetch_ohlcv(sym, "1h", 100)
    df = compute_indicators(df)
    print("Signal généré :", generate_signal(df))
