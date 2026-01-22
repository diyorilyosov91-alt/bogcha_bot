import os
import time
from flask import Flask
from threading import Thread

# 1. Flask server (Render uchun)
app = Flask(__name__)

@app.route('/')
def home():
    return "✅ Bot is running!"

def run_flask():
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)

# 2. Telegram bot (alohida threadda)
def run_bot():
    try:
        print("🚀 Telegram bot ishga tushmoqda...")
        
        # Kutubxonani import qilish
        from telegram import Update
        from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
        
        BOT_TOKEN = "8087301459:AAHBvRA-erwAndeNIop8QvJEwSU235NLH2U"
        
        async def start(update: Update, context: CallbackContext):
            await update.message.reply_text("Salom! Bot ishlayapti!")
        
        async def main():
            application = Application.builder().token(BOT_TOKEN).build()
            application.add_handler(CommandHandler("start", start))
            
            print("🤖 Telegram bot ishga tushdi!")
            await application.run_polling()
        
        # Asyncio ishga tushirish
        import asyncio
        asyncio.run(main())
        
    except Exception as e:
        print(f"❌ Bot xatosi: {e}")
        print("Bot qayta urinib ko'rmoqda...")
        time.sleep(10)
        run_bot()

if __name__ == '__main__':
    # Flask serverni ishga tushirish
    flask_thread = Thread(target=run_flask, daemon=True)
    flask_thread.start()
    print("🌐 Flask server ishga tushdi")
    
    # Telegram botni ishga tushirish
    bot_thread = Thread(target=run_bot, daemon=True)
    bot_thread.start()
    
    # Asosiy threadni ushlab turish
    while True:
        time.sleep(3600)