import os, requests, json, logging
from flask import Flask, request

logging.basicConfig(level=logging.INFO)
app = Flask(__name__)

TRAINER_BOT_TOKEN = os.environ.get("TRAINER_BOT_TOKEN", "")
ADMIN_ID = os.environ.get("ADMIN_ID", "")

HALL_MAP = {
    "весна": "Зал 1 - ЖК Весна",
    "апрелевка": "Зал 1 - ЖК Весна",
    "селятино": "Зал 2 - Селятино",
    "бунино": "Зал 3 - Эко Бунино",
    "эко": "Зал 3 - Эко Бунино",
}

def normalize_hall(raw):
    if not raw:
        return raw
    low = raw.lower()
    for key, val in HALL_MAP.items():
        if key in low:
            return val
    return raw

@app.route("/tilda", methods=["GET", "POST"])
def tilda():
    form_data = request.form.to_dict()
    args_data = request.args.to_dict()
    json_data = {}
    try:
        json_data = request.get_json(force=True) or {}
    except Exception:
        pass

    all_data = {**form_data, **args_data, **json_data}
    logging.info("Tilda data: %s", all_data)

    # Тестовый запрос от Tilda — игнорируем
    if all_data == {"test": "test"} or not all_data.get("Phone"):
        return "ok", 200

    phone = all_data.get("Phone", "Не указан")
    name = all_data.get("name", "Не указано")
    hall_raw = all_data.get("Где_хотите_заниматься", "Не указан")
    hall = normalize_hall(hall_raw)

    # Формат который парсит @Juma2018_bot
    msg = (
        "Request details:\n"
        "Phone: " + phone + "\n"
        "name: " + name + "\n"
        "Где_хотите_заниматься: " + hall
    )

    try:
        url = "https://api.telegram.org/bot" + TRAINER_BOT_TOKEN + "/sendMessage"
        resp = requests.post(url, json={"chat_id": ADMIN_ID, "text": msg}, timeout=10)
        logging.info("Telegram response: %s", resp.status_code)
    except Exception as e:
        logging.error("Telegram error: %s", e)

    return "ok", 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
