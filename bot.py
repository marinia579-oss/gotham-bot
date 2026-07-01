from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from zoneinfo import ZoneInfo
import json
import os
from datetime import time

TOKEN = "YOUR_BOT_TOKEN"
USERS_FILE = "users.json"

def save_user(user_id):
    if not os.path.exists(USERS_FILE):
        with open(USERS_FILE, "w") as f:
            json.dump([], f)

    with open(USERS_FILE, "r") as f:
        users = json.load(f)

    if user_id not in users:
        users.append(user_id)

    with open(USERS_FILE, "w") as f:
        json.dump(users, f)

def get_users():
    if not os.path.exists(USERS_FILE):
        return []

    with open(USERS_FILE, "r") as f:
        return json.load(f)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    save_user(user_id)

    await update.message.reply_text(
        "Welcome to Gotham🦇\n\n"
        "You'll receive a Vitamin D reminder\n"
        "on the 11th of every month."
    )

async def send_gotham_message(context: ContextTypes.DEFAULT_TYPE):
    users = get_users()

    text = (
        "Gotham needs Batman\n"
        "Batman needs Vitamin D\n"
        "The fate of Gotham is in your hands..\n"
        "Take your Vitamin D.\n\n"
        "-The people of Gotham"
    )

    for user_id in users:
        try:
            await context.bot.send_message(chat_id=user_id, text=text)
        except Exception:
            pass

app = Application.builder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))

app.job_queue.run_monthly(
    send_gotham_message,
    when=time(1, 43, tzinfo=ZoneInfo("Asia/Tehran")),
    day=11
)

print("Bot is running...")

app.run_polling()
