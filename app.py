import os, requests
from flask import Flask, request

app = Flask(__name__)

TRAINER_BOT_TOKEN = os.environ.get("TRAINER_BOT_TOKEN", "")
ADMIN_ID = os.environ.get("ADMIN_ID", "")

@app.route("/tilda", methods=["POST"])
def tilda():
    data = request.form.to_dict()
    name = data.get("Name") or data.get("name") or "Не указано"
    phone = data.get("Phone") or data.get("phone") or "Не указано"
    hall = data.get("Где_хотите_заниматься") or data.get("where") or "Не указан"
    msg = (
        "Request details:"
        "Phone: " + phone + "\n"
        "name: " + name + "\n"
        "Где_хотите_заниматься: " + hall
    )
    requests.post(
        "https://api.telegram.org/bot" + TRAINER_BOT_TOKEN + "/sendMessage",
        json={"chat_id": ADMIN_ID, "text": msg}
    )
    return "ok", 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
