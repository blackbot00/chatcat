from telegram import Update
from telegram.ext import ContextTypes
from app.constants.texts import CHOOSE_CHAT
from app.keyboards.chat import human_ai_keyboard

async def chat_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        CHOOSE_CHAT,
        reply_markup=human_ai_keyboard(),
        parse_mode="Markdown"
    )
