from telegram import Update
from telegram.ext import ContextTypes
from app.db.mongo import users_col
from app.constants import texts
from app.keyboards.registration import state_keyboard
from app.keyboards.chat import human_ai_keyboard
from app.utils.logger import log_group1

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    user_db = users_col.find_one({"_id": user.id})

    # First time
    if not user_db:
        users_col.insert_one({
            "_id": user.id,
            "name": user.first_name,
            "username": user.username,
            "registered": False
        })
        await log_group1(f"🆕 First Start\n👤 {user.first_name} ({user.id})")

        await update.message.reply_text(
            texts.STATE_TEXT,
            reply_markup=state_keyboard(),
            parse_mode="Markdown"
        )
        return

    # Not registered yet
    if not user_db.get("registered"):
        await update.message.reply_text(
            texts.STATE_TEXT,
            reply_markup=state_keyboard(),
            parse_mode="Markdown"
        )
        return

    # Already registered
    await update.message.reply_text(
        texts.CHOOSE_CHAT,
        reply_markup=human_ai_keyboard(),
        parse_mode="Markdown"
    )
