from telegram import Update
from telegram.ext import ContextTypes
from app.db.mongo import users_col
from app.constants.texts import START_TEXT
from app.keyboards.chat import human_ai_keyboard
from app.utils.logger import log_group1

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user

    exists = users_col.find_one({"_id": user.id})

    if not exists:
        users_col.insert_one({
            "_id": user.id,
            "name": user.first_name,
            "username": user.username,
            "registered": False
        })
        await log_group1(f"🆕 First Start\n👤 {user.first_name} ({user.id})")

    await update.message.reply_text(
        START_TEXT,
        reply_markup=human_ai_keyboard(),
        parse_mode="Markdown"
    )
