import time
import threading
import requests
from flask import Flask

# ==========================
# 🔹 Telegram Bot Settings
# ==========================
BOT_TOKEN = 8376149890  # your token
CHAT_ID = 1609197089  # your chat id

# ==========================
# 🔹 Flask Web Setup
# ==========================
app = Flask(__name__)

@app.route('/')
def home():
    return "🚀 Crypto Wealth Builder Bot is running successfully!"

# ==========================
# 🔹 Get Top Coins from CoinGecko
# ==========================
def get_top_coins():
    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {
        "vs_currency": "usd",
        "order": "market_cap_desc",
        "per_page": 50,
        "page": 1,
        "sparkline": "false"
    }
    r = requests.get(url, params=params)
    return r.json()

# ==========================
# 🔹 Analyze Coins for Long-Term Investing
# ==========================
def analyze_coins():
    data = get_top_coins()
    buy_signals = []
    sell_signals = []

    for coin in data:
        name = coin["name"]
        symbol = coin["symbol"].upper()
        price_change_7d = coin.get("price_change_percentage_7d_in_currency", 0)
        price_change_30d = coin.get("price_change_percentage_30d_in_currency", 0)
        mcap_rank = coin["market_cap_rank"]

        # 🔸 Long-Term BUY Logic
        if price_change_30d < -10 and price_change_7d > 0:
            buy_signals.append(f"🟢 BUY: {name} ({symbol}) — Rank {mcap_rank} | Rebounding after dip")

        # 🔸 SELL Logic
        elif price_change_7d > 20:
            sell_signals.append(f"🔴 SELL: {name} ({symbol}) — Up {round(price_change_7d,1)}% in 7d (Overheated)")

    # Compose message
    if not buy_signals and not sell_signals:
        message = "🕵️ No strong long-term opportunities now. Market neutral."
    else:
        message = "💰 Weekly Crypto Long-Term Signals:\n\n"
        if buy_signals:
            message += "\n".join(buy_signals)
        if sell_signals:
            message += "\n\n" + "\n".join(sell_signals)

    send_telegram_message(message)

# ==========================
# 🔹 Telegram Message Sender
# ==========================
def send_telegram_message(message):
    url = f"https://api.telegram.org/8376149890:AAFiw5rok3-NbT5SdxHGWcmn3Q7aEOzKKYs/sendMessage"
    payload = {"chat_id":1609197089 , "text": message}
    try:
        requests.post(url, data=payload)
    except Exception as e:
        print(f"Telegram send error: {e}")

# ==========================
# 🔹 Background Loop
# ==========================
def run_bot():
    while True:
        print("🔍 Scanning crypto market for long-term signals...")
        analyze_coins()
        print("✅ Scan complete. Next scan in 7 days.\n")
        time.sleep(604800)  # 7 days = 604800 seconds

# ==========================
# 🔹 Run Flask + Bot Together
# ==========================
if __name__ == '__main__':
    threading.Thread(target=run_bot, daemon=True).start()
    app.run(host='0.0.0.0', port=10000)
