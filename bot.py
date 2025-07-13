import os
import telebot
import requests
from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.getenv("7753208710:AAGrk0xaPrXtLtJyoNWBhuQJZRZRWgJCiZA")
WEBHOOK_URL = os.getenv("https://script.google.com/macros/s/AKfycbwl2ttEmeOn-sxR5dk_u1erUDX0Kpyuk0PeGFX2zPceyyq-rhtzlgvgeMIyHynxx8EG/exec")

bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(m):
    bot.reply_to(m, "WELCOME! Use:\n/expense <amount> <desc>\n/income <amount> <desc>")

def send_to_sheet(t, amt, desc, m):
    payload = {"type": t, "amount": amt, "description": desc}
    r = requests.post(WEBHOOK_URL, json=payload)
    if r.status_code == 200:
        bot.reply_to(m, f"✅ {t} saved!")
    else:
        bot.reply_to(m, "❌ Error saving.")

@bot.message_handler(commands=['expense'])
def exp(m):
    try:
        amt, desc = m.text.split(' ',2)[1:]
        send_to_sheet("Expense", float(amt), desc, m)
    except:
        bot.reply_to(m, "⚠️ Use: /expense 150 lunch")

@bot.message_handler(commands=['income'])
def inc(m):
    try:
        amt, desc = m.text.split(' ',2)[1:]
        send_to_sheet("Income", float(amt), desc, m)
    except:
        bot.reply_to(m, "⚠️ Use: /income 2000 salary")

bot.polling()
