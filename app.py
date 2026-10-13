from flask import Flask, request
import requests, os, json
from datetime import datetime

app = Flask(__name__)
DISCORD_URL = os.getenv("DISCORD_WEBHOOK_URL")

@app.route("/", methods=["GET"])
def home():
    return "SSO 【entity-Discord¦canonical_name=Discord】 Bot is Live!"

@app.route("/webhook", methods=["POST"])
def webhook():
    try:
        data = request.get_json(force=True, silent=True) or {}
        embed = {
            "title": "🔔 SSO 信號觸發",
            "color": 3066993,
            "fields": [
                {"name": "Ticker", "value": str(data.get("ticker","SSO")), "inline": True},
                {"name": "Action", "value": str(data.get("action","BUY")), "inline": True},
                {"name": "Price", "value": str(data.get("price","-")), "inline": True},
                {"name": "Time", "value": datetime.now().strftime("%m-%d %H:%M"), "inline": False},
                {"name": "Detail", "value": f"```json\n{json.dumps(data, ensure_ascii=False)[:800]}\n```", "inline": False}
            ]
        }
        requests.post(DISCORD_URL, json={"username":"SSO助手","embeds":[embed]}, timeout=10)
        return "ok", 200
    except Exception as e:
        return str(e), 500
