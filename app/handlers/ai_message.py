import re
from telegram import Update
from telegram.ext import ContextTypes

from app.db.mongo import users_col
from app.services.ai_service import ai_reply
from app.constants.plans import FREE_AI_LIMIT
from app.utils.logger import log_group2

PHONE_REGEX = r"\b\d{10}\b"

async def ai_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if "ai_mode" not in context.user_data:
        return

    user_id = update.effective_user.id
    user = users_col.find_one({"_id": user_id})
    is_premium = user.get("premium", False)

    # LIMIT
    today = str(update.message.date.date())
    usage = user.get("ai_usage", {}).get(today, 0)

    if not is_premium and usage >= FREE_AI_LIMIT:
        await update.message.reply_text("🚫 Daily AI limit reached (40). Upgrade to Premium 💎")
        return

    msg = update.message.text

    # SAFETY
    if re.search(PHONE_REGEX, msg):
        reply = "🙏 Safety ku phone number share panna mudiyadhu."
    elif "http" in msg or "www" in msg:
        reply = "🚫 Links share panna allowed illa."
    else:
        gender = user.get("gender", "neutral")
        ai_gender = "girl" if gender == "male" else "boy" if gender == "female" else "neutral"

        system_prompt = (
            f"You are a {ai_gender} AI partner.\n"
            f"Mode: {context.user_data['ai_mode']}\n"
            f"Language: {context.user_data['ai_lang']}\n"
            "Be romantic, safe, and respectful.\n"
            "Never ask phone numbers or external contacts."
        )

        reply = await ai_reply(system_prompt, msg)

    await update.message.reply_text(reply)

    # UPDATE USAGE
    users_col.update_one(
        {"_id": user_id},
        {"$inc": {f"ai_usage.{today}": 1}}
    )

    # LOG
    await log_group2(
        f"👤 {update.effective_user.first_name} ({user_id}) ↔ 🤖 AI\n"
        f"User: {msg}\nAI: {reply}"
      )
