import os
import logging
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext, CallbackQueryHandler

# ========== TOKEN ==========
BOT_TOKEN = "8087301459:AAHBvRA-erwAndeNIop8QvJEwSU235NLH2U"

# ========== LOGGING ==========
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

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
    await update.message.reply_text("🏫 Bog'cha haqida ma'lumot")

# ========== TAOMNOMA ==========
async def taomnoma(update: Update, context: CallbackContext):
    await update.message.reply_text("🍽 Taomnoma")

# ========== E'LONLAR ==========
async def elonlar(update: Update, context: CallbackContext):
    await update.message.reply_text("📢 E'lonlar")

# ========== FARZAND KELMAYDI ==========
async def farzand_kelmaydi(update: Update, context: CallbackContext):
    keyboard = [[InlineKeyboardButton("Kasallik", callback_data='sick')]]
    await update.message.reply_text(
        "Farzandingiz kelmaslik sababi?",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# ========== ALOQA ==========
async def aloqa(update: Update, context: CallbackContext):
    await update.message.reply_text("📞 Aloqa")

# ========== MANZIL ==========
async def manzil(update: Update, context: CallbackContext):
    await update.message.reply_text("📍 Manzil")

# ========== TUGMA BOSILGANDA ==========
async def button_callback(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.answer()
    await query.edit_message_text("✅ Xabaringiz qabul qilindi!")

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
    # Application yaratish
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Handlerlar
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_callback))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    # Render uchun port
    port = int(os.environ.get("PORT", 8080))
    
    # Server ishga tushirish
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
    print(f"✅ Server {port}-portda ishga tushdi")
    
    # Botni ishga tushirish
    print("🤖 Bot ishga tushdi...")
    application.run_polling()

if __name__ == '__main__':
    main()