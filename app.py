from flask import Flask, request
import requests, os

app = Flask(__name__)

PHONE_NUMBER_ID = os.environ.get("PHONE_ID")
ACCESS_TOKEN = os.environ.get("TOKEN")
TO_NUMBER = os.environ.get("TO_NUMBER")

def send_whatsapp(text):
    url = f"https://graph.facebook.com/v19.0/{PHONE_NUMBER_ID}/messages"
    headers = {"Authorization": f"Bearer {ACCESS_TOKEN}", "Content-Type": "application/json"}
    data = {"messaging_product": "whatsapp", "to": TO_NUMBER, "type": "text", "text": {"body": text}}
    requests.post(url, headers=headers, json=data)

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_data(as_text=True)
    print(f"收到TradingView: {data}")
    if "正T" in data or "買" in data:
        send_whatsapp(f"🟢 買入信號\nSSO {data}\n止損-0.4% 止盈+0.5% 15分鐘")
    elif "賣出" in data or "平" in data:
        send_whatsapp(f"🟡 賣出信號\nSSO {data}\n立刻平T倉")
    return "ok", 200

@app.route('/')
def home():
    return "Bot is running"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
