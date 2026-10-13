from flask import Flask, request
import requests, os, json
from datetime import datetime

app = Flask(__name__)
DISCORD_URL = os.getenv("DISCORD_WEBHOOK_URL")

@app.route("/", methods=["GET"])
def home():
    return "SSO Discord Bot is Live! - Ready for TradingView"

@app.route("/webhook", methods=["POST"])
def webhook():
    try:
        # 兼容 JSON 和 純文字
        data = request.get_json(force=True, silent=True)
        if not data:
            data = {"raw": request.get_data(as_text=True) or "empty"}

        embed = {
            "title": "🔔 SSO 信號觸發",
            "color": 3066993,
            "fields": [
                {"name": "Ticker", "value": str(data.get("ticker","SSO")), "inline": True},
                {"name": "Action", "value": str(data.get("action","BUY")), "inline": True},
                {"name": "Price", "value": str(data.get("price","-")), "inline": True},
                {"name": "Time", "value": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "inline": False},
                {"name": "Detail", "value": f"```json\n{json.dumps(data, ensure_ascii=False)[:900]}\n```", "inline": False}
            ]
        }
        if DISCORD_URL:
            requests.post(DISCORD_URL, json={"username":"SSO助手","embeds":[embed]}, timeout=10)
        return "ok", 200
    except Exception as e:
        # 出錯也發去Discord讓你知道
        try:
            requests.post(DISCORD_URL, json={"content": f"❌ SSO Bot出錯: {e}\n原始數據: {request.get_data(as_text=True)[:500]}"}, timeout=10)
        except:
            pass
        return str(e), 500
