import requests
from flask import Flask, request
import random
import re

# توکن ربات
TOKEN = "FGEBC0JWNTCHIUWSQVVCBDEIJPBNUGFXBZRPLNQDPRMVKAPWAKMWBKRHVCYOROCH"
BASE_URL = f"https://botapi.rubika.ir/v3/{TOKEN}/"

app = Flask(__name__)

# پیام‌های آماده
link_messages = [
    "پیام حاوی لینک حذف شد ✅",
    "لینک‌ها مجاز نیستند 😉",
    "لینک دیدم، پاک شد 🤖"
]

badcode_messages = [
    "پیام خطرناک حذف شد ⚠️",
    "کد هنگی شناسایی شد 😅",
    "این کد ممنوع است 🚫"
]

fun_messages = [
    "همه چی آرومه 😌",
    "🤖 BOT آنلاین است!",
    "کی میخواد بازی کنه؟ 🎲"
]

# تابع ارسال پیام
def send_message(chat_id, text):
    requests.post(BASE_URL + "sendMessage", json={"chat_id": chat_id, "text": text})

# مسیر اصلی Webhook
@app.route("/", methods=["POST"])
def index():
    data = request.get_json()

    # بررسی ساختار داده‌ها
    if "update" in data:
        update = data["update"]
        chat_id = update.get("chat_id")
        new_message = update.get("new_message", {})
        text = new_message.get("text", "")

        if not chat_id or not text:
            return "ok"

        # حذف لینک‌ها
        if re.search(r"(http://|https://|www\.|\.ir|\.com|\.net)", text):
            send_message(chat_id, random.choice(link_messages))
            return "ok"

        # حذف کد خطرناک / هنگی
        if re.search(r"(while\s*true|for\s*;;|rm\s+-rf|system\()", text, re.I):
            send_message(chat_id, random.choice(badcode_messages))
            return "ok"

        # بازی تاس
        if text == "تاس":
            number = random.randint(1, 6)
            send_message(chat_id, f"🎲 تاس: {number}")
            return "ok"

        # سوال ساده
        if text.lower() == "سوال":
            question = "چی بزرگ‌تره؟ ۱۰ یا ۵؟"
            send_message(chat_id, question)
            return "ok"

        # جواب مودبانه
        send_message(chat_id, f"سلام! شما گفتید: {text} 🤖")
    return "ok"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)