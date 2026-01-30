from telegram import Update
from telegram.ext import ContextTypes
from app.config import ADMIN_IDS
from app.db.mongo import users_col

async def ban_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id not in ADMIN_IDS:
        await update.message.reply_text("Admin only")
        return

    user_id = int(context.args[0])
    users_col.update_one({"_id": user_id}, {"$set": {"banned": True}})
    await update.message.reply_text("🚫 User banned")

async def unban_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id not in ADMIN_IDS:
        await update.message.reply_text("Admin only")
        return

    user_id = int(context.args[0])
    users_col.update_one({"_id": user_id}, {"$set": {"banned": False}})
    await update.message.reply_text("✅ User unbanned")

async def warn_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id not in ADMIN_IDS:
        await update.message.reply_text("Admin only")
        return

    user_id = int(context.args[0])
    reason = " ".join(context.args[1:])

    await context.bot.send_message(
        user_id,
        f"⚠️ *Warning*\nReason: {reason}",
        parse_mode="Markdown"
    )

    await update.message.reply_text("⚠️ Warning sent")
