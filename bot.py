import os
import time
from flask import Flask
from threading import Thread

# ========== FLASK SERVER (Render uchun) ==========
app = Flask(__name__)

@app.route('/')
def home():
    return "✅ Bog'cha boti ishlayapti!"

def run_flask():
    port = int(os.environ.get('PORT', 8080))
    print(f"🌐 Flask server {port}-portda ishga tushmoqda...")
    app.run(host='0.0.0.0', port=port)

# ========== TELEGRAM BOT ==========
def run_bot():
    print("🤖 Telegram bot ishga tushmoqda...")
    
    try:
        # Kutubxonalarni import qilish
        from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
        from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
        
        # ========== TO'G'RI TOKEN ==========
        BOT_TOKEN = "8087301459:AAHBvRA-erwAndeNIop8QvJEwSU235NLH2U"
        
        # ========== ASOSIY TUGMALAR ==========
        def get_main_keyboard():
            keyboard = [
                [KeyboardButton("👶 Bog'cha haqida"), KeyboardButton("🍎 Taomnoma")],
                [KeyboardButton("📅 E'lonlar"), KeyboardButton("❓ Farzandim kelmaydi")],
                [KeyboardButton("📞 Aloqa"), KeyboardButton("📍 Manzil")]
            ]
            return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        
        # ========== /start KOMANDASI ==========
        async def start(update: Update, context: CallbackContext):
            user = update.message.from_user
            await update.message.reply_text(
                f"Salom {user.first_name}! Quvnoq Bolajon bog'chasi botiga xush kelibsiz!\n\nKerakli bo'limni tanlang:",
                reply_markup=get_main_keyboard()
            )
        
        # ========== XABARLARNI QAYTA ISHLASH ==========
        async def handle_message(update: Update, context: CallbackContext):
            text = update.message.text
            
            if text == "👶 Bog'cha haqida":
                info = """🏫 QUVNOQ BOLAJON BOG'CHASI

📊 Umumiy ma'lumot:
• Yosh: 3-7 yosh
• Guruhlar: 5 ta
• Ish vaqti: 7:00-19:00
• Tarbiyachilar: 15 ta

🎓 Qo'shimcha darslar:
• Rassomchilik
• Raqs
• Ingliz tili
• Shaxmat"""
                await update.message.reply_text(info)
                
            elif text == "🍎 Taomnoma":
                menu = """🍽 HAFTA TAOMNOMASI

DUSHANBA:
• Nonushta: Sariyog'li choy, tuxum, non
• Tushlik: Mastava, salat
• Kechki: Meva, kefir"""
                await update.message.reply_text(menu)
                
            elif text == "📅 E'lonlar":
                elon = """📢 YANGI E'LONLAR

1. YANGI YIL BAYRAMI
📅 25-dekabr, 10:00

2. OTA-ONA MAJLISI
📅 28-dekabr, 16:00"""
                await update.message.reply_text(elon)
                
            elif text == "❓ Farzandim kelmaydi":
                await update.message.reply_text("✅ Xabaringiz qabul qilindi! Administratorlar siz bilan bog'lanadi.")
                print(f"📝 Farzand kelmaydi: {update.message.from_user.first_name}")
                
            elif text == "📞 Aloqa":
                aloqa = """📞 ALOQA MA'LUMOTLARI

Direktor: +99890 123-45-67
Tarbiyachi: +99891 234-56-78
Administrator: +99893 345-67-89"""
                await update.message.reply_text(aloqa)
                
            elif text == "📍 Manzil":
                await update.message.reply_text("📍 Manzil: Toshkent shahri, Yunusobod tumani")
                
            else:
                await update.message.reply_text("Iltimos, tugmalardan foydalaning.", reply_markup=get_main_keyboard())
        
        # ========== ASOSIY BOT FUNKSIYASI ==========
        async def main():
            application = Application.builder().token(BOT_TOKEN).build()
            application.add_handler(CommandHandler("start", start))
            application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
            
            print("✅ Telegram bot ishga tushdi!")
            await application.run_polling()
        
        # Botni ishga tushirish
        import asyncio
        asyncio.run(main())
        
    except Exception as e:
        print(f"❌ Bot xatosi: {e}")
        time.sleep(10)
        run_bot()  # Qayta urinish

# ========== ASOSIY DASTUR ==========
if __name__ == '__main__':
    # Flask serverni ishga tushirish
    flask_thread = Thread(target=run_flask, daemon=True)
    flask_thread.start()
    
    # Telegram botni ishga tushirish
    bot_thread = Thread(target=run_bot, daemon=True)
    bot_thread.start()
    
    print("🚀 Bog'cha boti ishga tushdi!")
    
    # Dasturni to'xtamasligi uchun
    while True:
        time.sleep(3600)