from telegram import InlineKeyboardButton, InlineKeyboardMarkup

def back_exit():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("⬅️ Back", callback_data="back"),
            InlineKeyboardButton("🚪 Exit", callback_data="exit")
        ]
    ])
