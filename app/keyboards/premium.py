from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from app.constants.plans import PREMIUM_PLANS

def premium_keyboard():
    buttons = []
    for key, plan in PREMIUM_PLANS.items():
        buttons.append([
            InlineKeyboardButton(
                plan["label"],
                callback_data=f"buy:{key}"
            )
        ])

    buttons.append([InlineKeyboardButton("⬅️ Back", callback_data="back:chat")])
    return InlineKeyboardMarkup(buttons)
