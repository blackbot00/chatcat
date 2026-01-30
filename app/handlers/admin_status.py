from telegram import Update
from telegram.ext import ContextTypes
from datetime import datetime

from app.config import ADMIN_IDS
from app.db.mongo import users_col, payments_col, reports_col

BOT_START_TIME = datetime.utcnow()

async def status_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id not in ADMIN_IDS:
        await update.message.reply_text("🚫 This command is only for Admin")
        return

    total_users = users_col.count_documents({})
    premium_users = users_col.count_documents({"premium": True})
    banned_users = users_col.count_documents({"banned": True})

    uptime = datetime.utcnow() - BOT_START_TIME

    text = (
        "🤖 *BOT STATUS — ADMIN*\n"
        "━━━━━━━━━━━━━━━━━━\n"
        "🟢 Bot: Online\n"
        f"⏱ Uptime: {uptime.days} days\n\n"
        "👥 *USERS*\n"
        f"• Total Users: {total_users}\n"
        f"• Premium Users: {premium_users}\n"
        f"• Banned Users: {banned_users}\n\n"
        "🛡 Safety: Enabled ✅\n"
        "🤖 AI: Enabled ✅"
    )

    await update.message.reply_text(text, parse_mode="Markdown")
