import os
import logging
import json
from datetime import datetime
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext, CallbackQueryHandler

# ========== TOKEN ==========
BOT_TOKEN = "8087301459:AAHBvRA-erwAndeNIop8QvJEwSU235NLH2U"

# ========== LOGGING ==========
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# ========== ASOSIY TUGMALAR ==========
def get_main_keyboard():
    return ReplyKeyboardMarkup([
        ["👶 Bog'cha haqida", "🍎 Taomnoma"],
        ["📅 E'lonlar", "❓ Farzandim kelmaydi"],
        ["📞 Aloqa", "📍 Manzil"]
    ], resize_keyboard=True)

# ========== /start KOMANDASI ==========
async def start(update: Update, context: CallbackContext):
    user = update.message.from_user
    await update.message.reply_text(
        f"Salom {user.first_name}! Bog'cha botiga xush kelibsiz!\n\nKerakli bo'limni tanlang:",
        reply_markup=get_main_keyboard()
    )

# ========== BOG'CHA HAQIDA ==========
async def bogcha_info(update: Update, context: CallbackContext):
    info_text = """🏫 QUVNOQ BOLAJON BOG'CHASI

📊 Umumiy ma'lumot:
• Yosh: 3-7 yosh
• Guruhlar: 5 ta
• Tarbiyachilar: 15 ta
• Ish vaqti: 7:00 - 19:00

🎓 Qo'shimcha darslar:
• Rassomchilik
• Raqs
• Ingliz tili
• Shaxmat"""
    await update.message.reply_text(info_text)

# ========== TAOMNOMA ==========
async def taomnoma(update: Update, context: CallbackContext):
    menu_text = """🍽 HAFTA TAOMNOMASI

DUSHANBA:
🍳 Nonushta: Sariyog'li choy, tuxum, non
🍲 Tushlik: Mastava, salat, non
🥗 Kechki: Meva, kefir

SESHANBA:
🍳 Nonushta: Sut, pirog, meva
🍲 Tushlik: Sho'rva, kartoshka, salat
🥗 Kechki: Yogurt, pechenye"""
    await update.message.reply_text(menu_text)

# ========== E'LONLAR ==========
async def elonlar(update: Update, context: CallbackContext):
    elon_text = """📢 YANGI E'LONLAR

1. YANGI YIL BAYRAMI 🎄
📅 Sana: 25-dekabr
🕐 Vaqt: 10:00

2. OTA-ONA MAJLISI
📅 Sana: 28-dekabr
🕐 Vaqt: 16:00"""
    await update.message.reply_text(elon_text)

# ========== FARZAND KELMAYDI ==========
async def farzand_kelmaydi(update: Update, context: CallbackContext):
    keyboard = [
        [InlineKeyboardButton("Kasallik", callback_data='sick')],
        [InlineKeyboardButton("Tashrif", callback_data='trip')],
        [InlineKeyboardButton("Boshqa", callback_data='other')]
    ]
    await update.message.reply_text(
        "Farzandingiz kelmaslik sababi?",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# ========== ALOQA ==========
async def aloqa(update: Update, context: CallbackContext):
    await update.message.reply_text("📞 ALOQA:\n\nDirektor: +99890 123-45-67\nTarbiyachi: +99891 234-56-78")

# ========== MANZIL ==========
async def manzil(update: Update, context: CallbackContext):
    await update.message.reply_text("📍 Manzil:\nToshkent shahri, Yunusobod tumani")

# ========== TUGMA BOSILGANDA ==========
async def button_callback(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.answer()
    
    sabablar = {
        'sick': "Kasallik",
        'trip': "Tashrif", 
        'other': "Boshqa sabab"
    }
    
    sabab = sabablar.get(query.data, "Noma'lum")
    user = query.from_user
    
    # Foydalanuvchiga xabar
    await query.edit_message_text(f"✅ Xabaringiz qabul qilindi!\nSabab: {sabab}\nAdministratorlar siz bilan bog'lanadi.")
    
    # Logga yozish
    print(f"📝 Yangi kelmaslik: {user.first_name}, Sabab: {sabab}, Vaqt: {datetime.now()}")
    
    # Bu yerda sizga xabar yuborish kodi qo'shiladi (keyinroq)

# ========== XABARLARNI QAYTA ISHLASH ==========
async def handle_message(update: Update, context: CallbackContext):
    text = update.message.text
    
    if text == "👶 Bog'cha haqida":
        await bogcha_info(update, context)
    elif text == "🍎 Taomnoma":
        await taomnoma(update, context)
    elif text == "📅 E'lonlar":
        await elonlar(update, context)
    elif text == "❓ Farzandim kelmaydi":
        await farzand_kelmaydi(update, context)
    elif text == "📞 Aloqa":
        await aloqa(update, context)
    elif text == "📍 Manzil":
        await manzil(update, context)
    else:
        await update.message.reply_text("Iltimos, tugmalardan foydalaning.", reply_markup=get_main_keyboard())

# ========== ASOSIY FUNKSIYA ==========
def main():
    # Botni yaratish
    app = Application.builder().token(BOT_TOKEN).build()
    
    # Handlerlar
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_callback))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    # Render uchun port (MUHIM!)
    port = int(os.environ.get("PORT", 8080))
    
    # Oddiy server ishga tushirish (portni bog'lash uchun)
    from http.server import HTTPServer, BaseHTTPRequestHandler
    class Handler(BaseHTTPRequestHandler):
        def do_GET(self):
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b'Bot is running!')
        def log_message(self, format, *args):
            pass
    
    import threading
    server = HTTPServer(('0.0.0.0', port), Handler)
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.daemon = True
    server_thread.start()
    print(f"🌐 Server {port}-portda ishga tushdi")
    
    # Botni ishga tushirish
    print("🤖 Bot ishga tushdi...")
    app.run_polling()

if __name__ == '__main__':
    main()