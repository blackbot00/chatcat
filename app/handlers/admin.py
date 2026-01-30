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
