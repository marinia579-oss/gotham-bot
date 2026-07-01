from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from datetime import time
from zoneinfo import ZoneInfo
import os
import sqlite3

TOKEN = os.getenv("TOKEN")

# ---------------- DB ----------------
conn = sqlite3.connect("users.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY
)
""")
conn.commit()

def save_user(user_id):
    cursor.execute("INSERT OR IGNORE INTO users (user_id) VALUES (?)", (user_id,))
    conn.commit()

def get_users():
    cursor.execute("SELECT user_id FROM users")
    return [row[0] for row in cursor.fetchall()]

# ---------------- BOT ----------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    save_user(user_id)

    await update.message.reply_text(
        "🦇 Welcome to Gotham\n\n"
        "You'll receive a Vitamin D reminder\n"
        "on the 11th of every month."
    )

async def send_gotham_message(context: ContextTypes.DEFAULT_TYPE):
    users = get_users()

    text = (
        "Gotham needs Batman\n"
        "Batman needs Vitamin D\n"
        "Take your Vitamin D.\n\n"
        "- Gotham"
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
