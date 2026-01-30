from telegram import Update
from telegram.ext import ContextTypes
from datetime import datetime, timedelta

from app.keyboards.premium import premium_keyboard
from app.constants.plans import PREMIUM_PLANS
from app.services.payment_service import create_cashfree_order
from app.db.mongo import users_col, payments_col

async def premium_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = users_col.find_one({"_id": update.effective_user.id})

    if user.get("premium"):
        expiry = user.get("premium_expiry")
        await update.message.reply_text(
            f"💎 *Premium Active*\nExpires on: {expiry}",
            parse_mode="Markdown"
        )
        return

    await update.message.reply_text(
        "💎 *Upgrade to Premium*\n━━━━━━━━━━━━━━━\nChoose your plan 👇",
        reply_markup=premium_keyboard(),
        parse_mode="Markdown"
    )

async def premium_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    data = query.data
    user_id = query.from_user.id

    if not data.startswith("buy:"):
        return

    plan_key = data.split(":")[1]
    plan = PREMIUM_PLANS[plan_key]

    order = await create_cashfree_order(user_id, plan["price"])

    payments_col.insert_one({
        "user_id": user_id,
        "order_id": order["order_id"],
        "plan": plan_key,
        "amount": plan["price"],
        "status": "PENDING",
        "created_at": datetime.utcnow()
    })

    await query.edit_message_text(
        "💳 *Complete Payment*\n\nClick below 👇",
        reply_markup={
            "inline_keyboard": [[
                {
                    "text": "💰 Pay Now",
                    "url": order["payment_link"]
                }
            ]]
        },
        parse_mode="Markdown"
  )
