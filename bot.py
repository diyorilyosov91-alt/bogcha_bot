import os
import logging
import json
from datetime import datetime
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext, CallbackQueryHandler

# ========== TOKENNI SHU YERGA QO'YING ==========
BOT_TOKEN = "8087301459:AAHBvRA-erwAndeNIop8QvJEwSU235NLH2U"
# ==============================================

# Logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Ma'lumotlar bazasi (oddiy fayl)
DB_FILE = "data.json"

def load_db():
    try:
        with open(DB_FILE, 'r') as f:
            return json.load(f)
    except:
        return {"kelmaganlar": [], "savollar": []}

def save_db(data):
    with open(DB_FILE, 'w') as f:
        json.dump(data, f, indent=2)

# Asosiy tugmalar
def get_main_keyboard():
    return ReplyKeyboardMarkup([
        ["👶 Bog'cha haqida", "🍎 Taomnoma"],
        ["📅 E'lonlar", "❓ Farzandim kelmaydi"],
        ["💬 AI Yordamchi", "📞 Aloqa"],
        ["📍 Manzil", "⭐ Baholash"]
    ], resize_keyboard=True)

# /start komandasi
async def start(update: Update, context: CallbackContext):
    user = update.message.from_user
    welcome_text = f"""
👋 *Assalomu alaykum {user.first_name}!*

*Quvnoq Bolajon* bog'chasining rasmiy botiga xush kelibsiz!

Kerakli bo'limni tanlang 👇
    """
    await update.message.reply_text(welcome_text, 
                                   reply_markup=get_main_keyboard(),
                                   parse_mode='Markdown')

# Bog'cha haqida
async def bogcha_info(update: Update, context: CallbackContext):
    info_text = """
🏫 *QUVNOQ BOLAJON BOG'CHASI*

*📊 Umumiy ma'lumot:*
• Yosh: 3-7 yosh
• Guruhlar: 5 ta
• Tarbiyachilar: 15 ta
• Ish vaqti: 7:00 - 19:00

*🎓 Qo'shimcha darslar:*
• Rassomchilik
• Raqs
• Ingliz tili
• Shaxmat
    """
    await update.message.reply_text(info_text, parse_mode='Markdown')

# Taomnoma
async def taomnoma(update: Update, context: CallbackContext):
    menu_text = """
🍽 *HAFTA TAOMNOMASI*

*DUSHANBA:*
🍳 Nonushta: Sariyog'li choy, tuxum, non
🍲 Tushlik: Mastava, salat, non
🥗 Kechki: Meva, kefir

*SESHANBA:*
🍳 Nonushta: Sut, pirog, meva
🍲 Tushlik: Sho'rva, kartoshka, salat
🥗 Kechki: Yogurt, pechenye
    """
    await update.message.reply_text(menu_text, parse_mode='Markdown')

# E'lonlar
async def elonlar(update: Update, context: CallbackContext):
    elon_text = """
📢 *YANGI E'LONLAR*

*1. YANGI YIL BAYRAMI* 🎄
📅 Sana: 25-dekabr
🕐 Vaqt: 10:00

*2. OTA-ONA MAJLISI*
📅 Sana: 28-dekabr
🕐 Vaqt: 16:00
    """
    await update.message.reply_text(elon_text, parse_mode='Markdown')

# Farzand kelmaydi
async def farzand_kelmaydi(update: Update, context: CallbackContext):
    keyboard = [
        [InlineKeyboardButton("Kasallik", callback_data='reason_sick')],
        [InlineKeyboardButton("Tashrif", callback_data='reason_trip')],
        [InlineKeyboardButton("Boshqa sabab", callback_data='reason_other')]
    ]
    await update.message.reply_text(
        "❓ *Farzandingiz kelmaslik sababi?*",
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode='Markdown'
    )

# AI yordamchi
async def ai_helper(update: Update, context: CallbackContext):
    await update.message.reply_text(
        "💬 *Savolingizni yozing, men javob beraman!*\n\n"
        "Masalan:\n• Bog'cha qachon ochilgan?\n• Qanday hujjatlar kerak?\n• Farzandim moslashmayapti"
    )
    context.user_data['waiting_for_ai'] = True

# Aloqa
async def aloqa(update: Update, context: CallbackContext):
    await update.message.reply_text(
        "📞 *ALOQA:*\n\n"
        "Direktor: +99890 123-45-67\n"
        "Tarbiyachi: +99891 234-56-78\n"
        "Administrator: +99893 345-67-89"
    )

# Manzil
async def manzil(update: Update, context: CallbackContext):
    await update.message.reply_text(
        "📍 *Manzil:*\n"
        "Toshkent shahri, Yunusobod tumani,\n"
        "Farobiy ko'chasi, 45-uy"
    )

# Baholash
async def baholash(update: Update, context: CallbackContext):
    keyboard = [
        [InlineKeyboardButton("⭐", callback_data='rate_1')],
        [InlineKeyboardButton("⭐⭐", callback_data='rate_2')],
        [InlineKeyboardButton("⭐⭐⭐", callback_data='rate_3')],
        [InlineKeyboardButton("⭐⭐⭐⭐", callback_data='rate_4')],
        [InlineKeyboardButton("⭐⭐⭐⭐⭐", callback_data='rate_5')]
    ]
    await update.message.reply_text(
        "⭐ *Bog'chani baholang:*",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# Xabarlarni qayta ishlash
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
    elif text == "💬 AI Yordamchi":
        await ai_helper(update, context)
    elif text == "📞 Aloqa":
        await aloqa(update, context)
    elif text == "📍 Manzil":
        await manzil(update, context)
    elif text == "⭐ Baholash":
        await baholash(update, context)
    elif context.user_data.get('waiting_for_ai'):
        # AI ga savol
        await update.message.reply_text("🤔 *Fikrlayapman...*", parse_mode='Markdown')
        
        # Oddiy AI javobi
        ai_responses = [
            "Bu haqida bog'cha administratsiyasiga murojaat qilishingizni tavsiya qilaman.",
            "Bog'chamizda bunday holatda quyidagi tartib qo'llaniladi...",
            "Farzandingiz uchun eng yaxshi yechim - tarbiyachi bilan shaxsan suhbatlashish.",
            "Iltimos, 71-123-45-67 raqamiga qo'ng'iroq qiling.",
            "Bog'cha qoidalariga ko'ra, bunday holatda...",
        ]
        
        import random
        ai_response = random.choice(ai_responses)
        await update.message.reply_text(f"💡 *Javob:* {ai_response}", parse_mode='Markdown')
        context.user_data['waiting_for_ai'] = False
    else:
        await update.message.reply_text(
            "Tushunmadim. Iltimos, tugmalardan foydalaning.",
            reply_markup=get_main_keyboard()
        )

# Tugma bosilganda
async def button_callback(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.answer()
    
    if query.data.startswith('reason_'):
        reason = query.data.replace('reason_', '')
        reasons = {
            'sick': "Kasallik",
            'trip': "Tashrif",
            'other': "Boshqa sabab"
        }
        
        db = load_db()
        db["kelmaganlar"].append({
            "user_id": query.from_user.id,
            "ism": query.from_user.first_name,
            "sabab": reasons[reason],
            "vaqt": datetime.now().isoformat()
        })
        save_db(db)
        
        await query.edit_message_text(
            f"✅ *Xabaringiz qabul qilindi!*\n\n"
            f"Sabab: {reasons[reason]}\n"
            f"Administratorlar siz bilan bog'lanadi.",
            parse_mode='Markdown'
        )
    
    elif query.data.startswith('rate_'):
        rating = int(query.data.replace('rate_', ''))
        await query.edit_message_text(
            f"⭐ *Rahmat! Siz {rating} ball berdiz!*",
            parse_mode='Markdown'
        )

# Xatoliklar
async def error(update: Update, context: CallbackContext):
    logger.warning('Xatolik: %s', context.error)

# Asosiy funksiya
def main():
    # Application yaratish
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Handlerlar
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_callback))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    # Xatolik handler
    application.add_error_handler(error)
    
    # Botni ishga tushirish
    print("🤖 Bot ishga tushdi...")
    application.run_polling()

if __name__ == '__main__':
    main()
