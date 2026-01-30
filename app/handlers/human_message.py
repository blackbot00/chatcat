import re
from telegram import Update
from telegram.ext import ContextTypes
from datetime import datetime

from app.utils.logger import log_group2

LINK_REGEX = r"http|www"

async def human_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if "partner" not in context.user_data:
        return

    text = update.message.text
    partner_id = context.user_data["partner"]
    user = update.effective_user

    # RESTRICTIONS
    if re.search(LINK_REGEX, text):
        await update.message.reply_text("🚫 Links are not allowed.")
        return

    # FORWARD MESSAGE
    await context.bot.send_message(
        partner_id,
        f"💬 {text}"
    )

    # LOG
    await log_group2(
        f"[{datetime.now().strftime('%I:%M %p')}] "
        f"{user.first_name}({user.id}) ➜ {partner_id}\n"
        f"💬 {text}"
  )
