import requests
import time
import re
import json
import random
import os

# ---------- تنظیمات ----------
TOKEN = "FGEBC0JWNTCHIUWSQVVCBDEIJPBNUGFXBZRPLNQDPRMVKAPWAKMWBKRHVCYOROCH"
BASE_URL = f"https://botapi.rubika.ir/v3/{TOKEN}/"
MEMORY_FILE = "memory.json"
BOT_NAME = "BOT"

# ---------- سشن ----------
session = requests.Session()
session.headers.update({"Connection": "keep-alive"})

last_update_id = 0

# ---------- حافظه ----------
if os.path.exists(MEMORY_FILE):
    with open(MEMORY_FILE, "r", encoding="utf-8") as f:
        memory = json.load(f)
else:
    memory = {}

def save_memory():
    with open(MEMORY_FILE, "w", encoding="utf-8") as f:
        json.dump(memory, f, ensure_ascii=False, indent=2)

# ---------- توابع API ----------
def get_updates():
    global last_update_id
    try:
        r = session.post(BASE_URL + "getUpdates", json={"offset": last_update_id + 1, "timeout": 20}, timeout=35)
        return r.json()
    except:
        return {}

def send_message(chat_id, text):
    session.post(BASE_URL + "sendMessage", json={"chat_id": chat_id, "text": text})

def delete_message(chat_id, message_id):
    session.post(BASE_URL + "deleteMessage", json={"chat_id": chat_id, "message_id": message_id})

# ---------- پیام‌های آماده ----------
link_jokes = [
    "لینک ممنوعه 😄 پاک شد",
    "این گروه لینک‌خور نیست 😉",
    "لینک دیدم، پاکش کردم 🤖"
]

badcode_jokes = [
    "کد خطرناک شناسایی شد 🚫 حذف شد",
    "این کد گوشی ملت می‌ترکه 😅",
    "این کد بوی هنگ می‌داد 😐"
]

noise_texts = [
    f"{BOT_NAME} بیداره!",
    "کی آنلاینِ؟ 😌",
    "حوصله‌تون سر نره 😉",
    "همه چی آرومه 😄"
]

games = {
    "تاس": lambda: f"🎲 نتیجه تاس: {random.randint(1,6)}",
    "سوال": lambda: f"❓ سوال: انتخاب درست رو بده!"
}

print(f"🤖 {BOT_NAME} started successfully...")

# ---------- حلقه اصلی ----------
while True:
    try:
        updates = get_updates()
        if "data" in updates:
            for update in updates["data"]:
                last_update_id = update["update_id"]
                msg = update.get("message")
                if not msg:
                    continue

                chat_id = msg["chat"]["id"]
                message_id = msg["message_id"]
                text = msg.get("text", "").strip()

                # --- حذف لینک ---
                if re.search(r"(http://|https://|www\.|\.ir|\.com|\.net)", text):
                    delete_message(chat_id, message_id)
                    send_message(chat_id, random.choice(link_jokes))
                    continue

                # --- حذف کد مخرب / هنگی ---
                if re.search(r"(while\s*true|for\s*;;|system\(|fork\(|rm\s+-rf)", text, re.I):
                    delete_message(chat_id, message_id)
                    send_message(chat_id, random.choice(badcode_jokes))
                    continue

                # --- یاد دادن ---
                if text.startswith("یاد بگیر"):
                    try:
                        key, value = text.replace("یاد بگیر", "", 1).split("=>")
                        memory[key.strip()] = value.strip()
                        save_memory()
                        send_message(chat_id, "باشه 😊 یاد گرفتم")
                    except:
                        send_message(chat_id, "فرمت درست:\nیاد بگیر سلام => سلام خوشگلا 🙂")
                    continue

                # --- جواب از حافظه ---
                if text in memory:
                    send_message(chat_id, memory[text])
                    continue

                # --- شلوغ‌کاری کنترل‌شده ---
                if text == "شلوغ کن":
                    send_message(chat_id, random.choice(noise_texts))
                    continue

                # --- بازی ---
                if text in games:
                    send_message(chat_id, games[text]())
                    continue

        time.sleep(1)
    except Exception as e:
        print("ERROR:", e)
        time.sleep(5)