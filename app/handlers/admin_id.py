from telegram import Update
from telegram.ext import ContextTypes
from app.config import ADMIN_IDS
from app.db.mongo import users_col

async def id_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id not in ADMIN_IDS:
        await update.message.reply_text("🚫 This command is only for Admin")
        return

    if not context.args:
        await update.message.reply_text("Usage: /id <user_id>")
        return

    user_id = int(context.args[0])
    user = users_col.find_one({"_id": user_id})

    if not user:
        await update.message.reply_text("User not found")
        return

    text = (
        "👤 *USER PROFILE*\n"
        "━━━━━━━━━━━━━━\n"
        f"🆔 User ID: {user_id}\n"
        f"👤 Name: {user.get('name')}\n"
        f"⚧ Gender: {user.get('gender')}\n"
        f"🎂 Age: {user.get('age')}\n\n"
        "💎 *PREMIUM*\n"
        f"Status: {'Active' if user.get('premium') else 'Free'}\n"
        f"Expiry: {user.get('premium_expiry', '-')}\n\n"
        "🛡 *SAFETY*\n"
        f"Banned: {'Yes' if user.get('banned') else 'No'}"
    )

    await update.message.reply_text(text, parse_mode="Markdown")
