import requests
import pandas as pd
import numpy as np
import time
from datetime import datetime

# ===== Telegram Bot Setup =====
BOT_TOKEN = "8376149890:AAFiw5rok3-NbT5SdxHGWcmn3Q7aEOzKKYs"
CHAT_ID = 1609197089

def send_telegram_alert(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message}
    requests.post(url, data=payload)

# ===== Fetch Crypto Data =====
def get_crypto_data():
    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {"vs_currency": "usd", "order": "market_cap_desc", "per_page": 10, "page": 1}
    data = requests.get(url, params=params).json()
    df = pd.DataFrame(data)[["id", "symbol", "current_price", "total_volume", "price_change_percentage_24h"]]
    return df

# ===== RSI Calculation =====
def calculate_rsi(prices, period=14):
    delta = prices.diff()
    gain = delta.clip(lower=0)
    loss = -1 * delta.clip(upper=0)
    avg_gain = gain.rolling(window=period).mean()
    avg_loss = loss.rolling(window=period).mean()
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

# ===== Analyzer =====
def analyze_crypto():
    df = get_crypto_data()

    # Simulate price history for RSI
    df["price_history"] = df["current_price"].apply(lambda x: np.linspace(x*0.98, x*1.02, 30))
    df["RSI"] = df["price_history"].apply(lambda x: calculate_rsi(pd.Series(x)).iloc[-1])

    # EMA & Volume Strength
    df["EMA_short"] = df["current_price"] * 0.99
    df["EMA_long"] = df["current_price"] * 1.01
    df["Trend"] = np.where(df["EMA_short"] > df["EMA_long"], "Bullish", "Bearish")
    avg_vol = df["total_volume"].mean()
    df["Volume_Strength"] = np.where(df["total_volume"] > avg_vol, "High", "Low")

    # Final Signal
    signals = []
    for _, row in df.iterrows():
        if row["RSI"] < 30 and row["Trend"] == "Bullish" and row["Volume_Strength"] == "High":
            signals.append("STRONG BUY ✅")
        elif 30 <= row["RSI"] <= 70:
            signals.append("NEUTRAL ⚠️")
        else:
            signals.append("SELL 🔻")
    df["Signal"] = signals

    return df[["id", "symbol", "current_price", "RSI", "Trend", "Volume_Strength", "Signal"]]

# ===== Alert System =====
def run_and_alert():
    df = analyze_crypto()
    strong_buys = df[df["Signal"].str.contains("STRONG BUY")]
    if not strong_buys.empty:
        msg = "🚀 STRONG BUY ALERT 🚀\n\n"
        for _, row in strong_buys.iterrows():
            msg += f"{row['id'].upper()} ({row['symbol'].upper()})\nPrice: ${row['current_price']}\nRSI: {row['RSI']:.2f}\nTrend: {row['Trend']}\n\n"
        send_telegram_alert(msg)
    else:
        print("No strong buy signals now.")

# ===== Keep Running Forever =====
if __name__ == "__main__":
    print("🤖 Crypto Analyzer Bot Started — Running Every 30 Minutes")
    while True:
        try:
            run_and_alert()
            print(f"✅ Checked at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        except Exception as e:
            print(f"❌ Error: {e}")
        time.sleep(1800)  # 30 minutes

