from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import os
import sqlite3
from datetime import time

TOKEN = os.getenv("TOKEN")

# ---------- DATABASE ----------
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

# ---------- BOT ----------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    save_user(user_id)

    await update.message.reply_text(
        "🦇 Welcome to Gotham\n"
        "You'll receive monthly reminders."
    )

async def monthly_message(context: ContextTypes.DEFAULT_TYPE):
    users = get_users()

    text = (
        "Gotham reminder:\n"
        "Take your Vitamin D ☀️"
    )

    for user_id in users:
        try:
            await context.bot.send_message(chat_id=user_id, text=text)
        except:
            pass

# ---------- APP ----------
app = Application.builder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))

app.job_queue.run_monthly(
    monthly_message,
    when=time(10, 0),  # 10:00 صبح
    day=11
)

print("Bot is running...")
app.run_polling()
