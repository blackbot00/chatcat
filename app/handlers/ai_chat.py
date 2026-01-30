from telegram import Update
from telegram.ext import ContextTypes
from datetime import date

from app.db.mongo import users_col
from app.keyboards.ai import ai_language_keyboard, ai_mode_keyboard, ai_exit_keyboard
from app.constants.plans import FREE_AI_LIMIT
from app.services.ai_service import ai_reply
from app.utils.logger import log_group2
from app.constants.texts import AI_DISABLED

async def ai_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id
    data = query.data

    # AI OFF
    if not context.bot_data.get("AI_ENABLED", True):
        await query.answer(AI_DISABLED, show_alert=True)
        return

    user = users_col.find_one({"_id": user_id})
    is_premium = user.get("premium", False)

    # ENTER AI
    if data == "chat_ai":
        await query.edit_message_text(
            "🌐 *Choose AI Language*",
            reply_markup=ai_language_keyboard(),
            parse_mode="Markdown"
        )

    # LANGUAGE
    elif data.startswith("ai_lang:"):
        lang = data.split(":")[1]
        context.user_data["ai_lang"] = lang

        await query.edit_message_text(
            "💖 *Choose AI Personality*",
            reply_markup=ai_mode_keyboard(is_premium),
            parse_mode="Markdown"
        )

    # MODE
    elif data.startswith("ai_mode:"):
        mode = data.split(":")[1]

        if mode == "18plus" and not is_premium:
            await query.answer("💎 Premium users only", show_alert=True)
            return

        context.user_data["ai_mode"] = mode
        context.user_data["ai_count"] = 0

        await query.edit_message_text(
            "🤖 *AI Chat Started*\n\nSay hi 😊",
            reply_markup=ai_exit_keyboard(),
            parse_mode="Markdown"
        )

    # EXIT
    elif data == "ai_exit":
        context.user_data.clear()
        await query.edit_message_text(
            "💬 *Who do you want to chat with?*",
            reply_markup=None,
            parse_mode="Markdown"
        )
