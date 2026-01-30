from telegram import Update
from telegram.ext import ContextTypes
from app.config import ADMIN_IDS
from app.db.mongo import users_col

async def broadcast_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id not in ADMIN_IDS:
        await update.message.reply_text("🚫 This command is only for Admin")
        return

    if not context.args:
        await update.message.reply_text("Usage: /broadcast <message>")
        return

    message = " ".join(context.args)
    users = users_col.find({})

    sent = 0
    for user in users:
        try:
            await context.bot.send_message(user["_id"], message)
            sent += 1
        except:
            pass

    await update.message.reply_text(f"📣 Broadcast sent to {sent} users")
