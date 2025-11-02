import time
import threading
import requests
from flask import Flask

# ==========================
# 🔹 Telegram Bot Settings
# ==========================
BOT_TOKEN = 8376149890  # ← replace with your bot token
CHAT_ID = 1609197089                # ← replace with your chat ID

# ==========================
# 🔹 Flask Web Setup (for Render)
# ==========================
app = Flask(__name__)

@app.route('/')
def home():
    return "🚀 Crypto AI Bot is running successfully on Render!"

# ==========================
# 🔹 Your Crypto Logic (example)
# ==========================
def check_crypto_signals():
    try:
        print("🔍 Checking crypto signals...")
        # Example logic (replace with your own signal check)
        signals = ["No strong buy signals now."]
        message = "\n".join(signals)
        send_telegram_message(message)
    except Exception as e:
        send_telegram_message(f"⚠️ Error: {e}")

# ==========================
# 🔹 Telegram Message Sender
# ==========================
def send_telegram_message(message):
    url = f"https://api.telegram.org/bot8376149890:AAFiw5rok3-NbT5SdxHGWcmn3Q7aEOzKKYs/sendMessage"
    payload = {"chat_id": 1609197089, "text": message}
    try:
        requests.post(url, data=payload)
    except Exception as e:
        print(f"Telegram send error: {e}")

# ==========================
# 🔹 Background Loop
# ==========================
def run_bot():
    while True:
        check_crypto_signals()
        print("⏱ Waiting 30 minutes before next scan...\n")
        time.sleep(1800)  # 30 minutes

# ==========================
# 🔹 Run Flask + Bot Together
# ==========================
if __name__ == '__main__':
    # Run your crypto bot in background
    threading.Thread(target=run_bot, daemon=True).start()

    # Start Flask web server for Render
    app.run(host='0.0.0.0', port=10000)
