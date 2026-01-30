from telegram import Update
from telegram.ext import ContextTypes
from app.db.mongo import users_col
from app.keyboards.registration import gender_keyboard, age_keyboard
from app.keyboards.chat import human_ai_keyboard
from app.constants import texts
from app.utils.logger import log_group1

async def registration_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    data = query.data
    user_id = query.from_user.id

    # STATE
    if data.startswith("state:"):
        state = data.split(":")[1]
        users_col.update_one(
            {"_id": user_id},
            {"$set": {"state": state}}
        )
        await query.edit_message_text(
            texts.GENDER_TEXT,
            reply_markup=gender_keyboard(),
            parse_mode="Markdown"
        )

    # GENDER
    elif data.startswith("gender:"):
        gender = data.split(":")[1]
        users_col.update_one(
            {"_id": user_id},
            {"$set": {"gender": gender}}
        )
        await query.edit_message_text(
            texts.AGE_TEXT,
            reply_markup=age_keyboard(),
            parse_mode="Markdown"
        )

    # AGE
    elif data.startswith("age:"):
        age = int(data.split(":")[1])
        users_col.update_one(
            {"_id": user_id},
            {"$set": {
                "age": age,
                "registered": True
            }}
        )

        user = users_col.find_one({"_id": user_id})
        await log_group1(
            f"✅ Registration Completed\n"
            f"👤 {user['name']} ({user_id})\n"
            f"⚧ {user['gender']} | 🎂 {user['age']}"
        )

        await query.edit_message_text(
            texts.REG_DONE,
            reply_markup=human_ai_keyboard(),
            parse_mode="Markdown"
        )

    # BACK
    elif data.startswith("back:"):
        step = data.split(":")[1]
        if step == "state":
            await query.edit_message_text(
                texts.STATE_TEXT,
                reply_markup=state_keyboard(),
                parse_mode="Markdown"
            )
        elif step == "gender":
            await query.edit_message_text(
                texts.GENDER_TEXT,
                reply_markup=gender_keyboard(),
                parse_mode="Markdown"
  )
