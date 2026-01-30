from telegram import InlineKeyboardButton, InlineKeyboardMarkup

def ai_language_keyboard():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("🇮🇳 Tamil", callback_data="ai_lang:tamil"),
            InlineKeyboardButton("🇬🇧 English", callback_data="ai_lang:english")
        ],
        [
            InlineKeyboardButton("🇮🇳 Hindi", callback_data="ai_lang:hindi"),
            InlineKeyboardButton("🇮🇳 Telugu", callback_data="ai_lang:telugu")
        ],
        [
            InlineKeyboardButton("✨ Tanglish", callback_data="ai_lang:tanglish")
        ],
        [
            InlineKeyboardButton("⬅️ Back", callback_data="back:chat")
        ]
    ])


def ai_mode_keyboard(is_premium: bool):
    buttons = [
        [
            InlineKeyboardButton("💖 Sweet", callback_data="ai_mode:sweet"),
            InlineKeyboardButton("💘 Romantic", callback_data="ai_mode:romantic")
        ],
        [
            InlineKeyboardButton("🤗 Caring", callback_data="ai_mode:caring"),
            InlineKeyboardButton("😈 Possessive", callback_data="ai_mode:possessive")
        ]
    ]

    if is_premium:
        buttons.append(
            [InlineKeyboardButton("🔥 18+ (Premium)", callback_data="ai_mode:18plus")]
        )

    buttons.append([InlineKeyboardButton("⬅️ Back", callback_data="back:lang")])
    return InlineKeyboardMarkup(buttons)


def ai_exit_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🚪 Exit AI Chat", callback_data="ai_exit")]
    ])
