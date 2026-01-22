import os
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
from flask import Flask
from threading import Thread

# ========== TOKEN ==========
BOT_TOKEN = "8087301459:AAHBvRA-erwAndeNIop8QvJEwSU235NLH2U"

# ========== FLASK SERVER ==========
app = Flask(__name__)

@app.route('/')
def home():
    return "✅ Bog'cha Boti ishlayapti"

@app.route('/health')
def health():
    return "OK", 200

def run_flask():
    port = int(os.environ.get('PORT', 10000))
    print(f"🌐 Flask server {port}-portda ishga tushdi")
    app.run(host='0.0.0.0', port=port, debug=False)

# ========== TELEGRAM BOT ==========
async def start(update: Update, context: CallbackContext):
    keyboard = [[KeyboardButton("👶 Bog'cha haqida")]]
    await update.message.reply_text(
        "Salom! Bog'cha boti ishlayapti!",
        reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    )

async def handle_message(update: Update, context: CallbackContext):
    if update.message.text == "👶 Bog'cha haqida":
        await update.message.reply_text("🏫 Bog'cha haqida ma'lumot")
    else:
        await update.message.reply_text("Tugmani bosing")

async def run_telegram_bot():
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    print("🤖 Telegram bot ishga tushdi!")
    await application.run_polling()

# ========== ASOSIY DASTUR ==========
def main():
    # Flask serverni ishga tushirish
    flask_thread = Thread(target=run_flask, daemon=True)
    flask_thread.start()
    
    # Telegram botni ishga tushirish
    import asyncio
    asyncio.run(run_telegram_bot())

if __name__ == '__main__':
    main()