import os
import sys
from flask import Flask
from threading import Thread
import logging

# Flask server (Render uchun)
app = Flask('')

@app.route('/')
def home():
    return "Bot is running!"

def run():
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))

def keep_alive():
    server = Thread(target=run)
    server.daemon = True
    server.start()
    print("✅ Web server ishga tushdi")

# ========== TELEGRAM BOT ==========
try:
    from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
    from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
    
    BOT_TOKEN = "8087301459:AAHBvRA-erwAndeNIop8QvJEwSU235NLH2U"
    
    async def start(update: Update, context: CallbackContext):
        keyboard = [[KeyboardButton("👶 Bog'cha haqida")]]
        await update.message.reply_text(
            "Salom! Bog'cha botiga xush kelibsiz!",
            reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        )
    
    async def handle_message(update: Update, context: CallbackContext):
        text = update.message.text
        if text == "👶 Bog'cha haqida":
            await update.message.reply_text("🏫 Bog'cha haqida ma'lumot")
        else:
            await update.message.reply_text("Iltimos, tugmalardan foydalaning.")
    
    async def main_bot():
        application = Application.builder().token(BOT_TOKEN).build()
        application.add_handler(CommandHandler("start", start))
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
        
        print("🤖 Bot ishga tushdi...")
        await application.run_polling()
    
    # Botni ishga tushirish
    import asyncio
    bot_thread = Thread(target=lambda: asyncio.run(main_bot()))
    bot_thread.daemon = True
    bot_thread.start()
    
except ImportError as e:
    print(f"Kutubxona muammosi: {e}")
    print("requirements.txt faylini tekshiring")

# ========== ASOSIY ==========
if __name__ == '__main__':
    keep_alive()
    print("🚀 Bot va server ishga tushdi!")
    
    # Doimiy ishlash uchun
    while True:
        import time
        time.sleep(3600)  # 1 soat