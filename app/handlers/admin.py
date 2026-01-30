from telegram import Update
from telegram.ext import ContextTypes
from app.config import ADMIN_IDS
from app.constants.texts import ADMIN_ONLY

async def ai_on(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id not in ADMIN_IDS:
        await update.message.reply_text(ADMIN_ONLY)
        return
    context.bot_data["AI_ENABLED"] = True
    await update.message.reply_text("✅ AI Chat Enabled")

async def ai_off(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id not in ADMIN_IDS:
        await update.message.reply_text(ADMIN_ONLY)
        return
    context.bot_data["AI_ENABLED"] = False
    await update.message.reply_text("🚫 AI Chat Disabled")

from datetime import datetime, timedelta
from app.db.mongo import users_col
from app.config import ADMIN_IDS

async def giveaway(update, context):
    if update.effective_user.id not in ADMIN_IDS:
        await update.message.reply_text("Admin only")
        return

    user_id = int(context.args[0])
    days = int(context.args[1])

    expiry = datetime.utcnow() + timedelta(days=days)

    users_col.update_one(
        {"_id": user_id},
        {"$set": {
            "premium": True,
            "premium_expiry": expiry.strftime("%d-%m-%Y")
        }}
    )

    await update.message.reply_text("🎁 Giveaway Premium Activated")
    await context.bot.send_message(user_id, "🎉 Surprise! Premium activated for you 💎")
