from telegram import InlineKeyboardButton, InlineKeyboardMarkup

def human_ai_keyboard():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("👤 Human", callback_data="chat_human"),
            InlineKeyboardButton("🤖 AI", callback_data="chat_ai")
        ]
    ])
