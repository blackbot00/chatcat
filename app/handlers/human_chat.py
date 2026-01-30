from telegram import Update
from telegram.ext import ContextTypes
from datetime import datetime, date

from app.db.mongo import users_col
from app.services.match_service import add_to_queue, pop_match, remove_from_queue
from app.keyboards.human import human_exit_keyboard, report_keyboard
from app.constants.plans import FREE_HUMAN_LIMIT
from app.utils.logger import log_group2, log_group1

async def human_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id
    data = query.data

    user = users_col.find_one({"_id": user_id})
    is_premium = user.get("premium", False)

    # ENTER HUMAN CHAT
    if data == "chat_human":
        today = str(date.today())
        count = user.get("human_usage", {}).get(today, 0)

        if not is_premium and count >= FREE_HUMAN_LIMIT:
            await query.answer("🚫 Daily human chat limit reached. Upgrade to Premium 💎", show_alert=True)
            return

        add_to_queue(user_id)
        partner_id = pop_match(user_id)

        if not partner_id:
            await query.edit_message_text("🔎 Searching for partner...")
            return

        # CONNECT
        partner = users_col.find_one({"_id": partner_id})

        context.user_data["partner"] = partner_id
        context.bot_data[partner_id] = user_id

        users_col.update_one(
            {"_id": user_id},
            {"$inc": {f"human_usage.{today}": 1}}
        )

        info = (
            "💞 *Partner Connected!*\n"
            "━━━━━━━━━━━━━━━\n"
            f"⚧ Gender: {'Premium only' if not is_premium else partner.get('gender')}\n"
            f"🎂 Age: {partner.get('age')}"
        )

        await query.edit_message_text(info, reply_markup=human_exit_keyboard(), parse_mode="Markdown")

        await context.bot.send_message(
            chat_id=partner_id,
            text=info,
            reply_markup=human_exit_keyboard(),
            parse_mode="Markdown"
        )

    # EXIT
    elif data == "human_exit":
        partner_id = context.user_data.get("partner")

        if partner_id:
            await context.bot.send_message(
                partner_id,
                "❌ Partner left the chat.",
            )

            await log_group2(
                f"❌ Chat Ended\n{user_id} ↔ {partner_id}"
            )

        context.user_data.clear()
        remove_from_queue(user_id)

        await query.edit_message_text(
            "🚩 *Do you want to report this chat?*",
            reply_markup=report_keyboard(),
            parse_mode="Markdown"
        )

    # REPORT
    elif data.startswith("report:"):
        reason = data.split(":")[1]
        if reason != "none":
            await log_group1(
                f"🚨 Report Received\n"
                f"👤 User: {user_id}\n"
                f"📌 Reason: {reason}"
            )

        await query.edit_message_text(
            "💬 *Who do you want to chat with?*",
            parse_mode="Markdown"
      )
