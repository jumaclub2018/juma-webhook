import os, requests, json, logging
from flask import Flask, request

logging.basicConfig(level=logging.INFO)
app = Flask(__name__)

TRAINER_BOT_TOKEN = os.environ.get("TRAINER_BOT_TOKEN", "")
ADMIN_ID = os.environ.get("ADMIN_ID", "")

@app.route("/tilda", methods=["POST"])
def tilda():
    form_data = request.form.to_dict()
    json_data = {}
    try:
        json_data = request.get_json(force=True) or {}
    except Exception:
        pass

    all_data = {**form_data, **json_data}
    logging.info("Tilda data: %s", all_data)

    debug_msg = "🔍 Данные от Tilda:\n" + json.dumps(all_data, ensure_ascii=False, indent=2)
    
    url = "https://api.telegram.org/bot" + TRAINER_BOT_TOKEN + "/sendMessage"
    logging.info("Sending to: %s", url[:50])
    logging.info("chat_id: %s", ADMIN_ID)
    
    try:
        resp = requests.post(url, json={"chat_id": ADMIN_ID, "text": debug_msg}, timeout=10)
        logging.info("Telegram response: %s %s", resp.status_code, resp.text[:200])
    except Exception as e:
        logging.error("Telegram error: %s", e)

    return "ok", 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
