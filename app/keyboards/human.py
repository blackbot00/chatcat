from telegram import InlineKeyboardButton, InlineKeyboardMarkup

def human_exit_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🚪 Exit Chat", callback_data="human_exit")]
    ])

def report_keyboard():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("🚩 Scam", callback_data="report:scam"),
            InlineKeyboardButton("🤬 Abuse", callback_data="report:abuse")
        ],
        [
            InlineKeyboardButton("🔞 Adult", callback_data="report:adult"),
            InlineKeyboardButton("❌ No Report", callback_data="report:none")
        ]
    ])
