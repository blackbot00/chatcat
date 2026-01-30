from telegram import InlineKeyboardButton, InlineKeyboardMarkup

def state_keyboard():
    states = ["Tamil Nadu", "Kerala", "Karnataka", "Andhra", "Telangana", "Other"]
    buttons = [
        InlineKeyboardButton(s, callback_data=f"state:{s}")
        for s in states
    ]
    rows = [buttons[i:i+3] for i in range(0, len(buttons), 3)]
    return InlineKeyboardMarkup(rows)


def gender_keyboard():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("👦 Male", callback_data="gender:male"),
            InlineKeyboardButton("👧 Female", callback_data="gender:female"),
            InlineKeyboardButton("⚧ Transgender", callback_data="gender:trans")
        ],
        [InlineKeyboardButton("⬅️ Back", callback_data="back:state")]
    ])


def age_keyboard():
    ages = list(range(18, 51))
    buttons = [
        InlineKeyboardButton(str(a), callback_data=f"age:{a}")
        for a in ages
    ]
    rows = [buttons[i:i+7] for i in range(0, len(buttons), 7)]
    rows.append([InlineKeyboardButton("⬅️ Back", callback_data="back:gender")])
    return InlineKeyboardMarkup(rows)
