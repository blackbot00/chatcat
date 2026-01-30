from fastapi import FastAPI, Request
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler
)

from app.handlers.registration import registration_callback

telegram_app.add_handler(CallbackQueryHandler(registration_callback))

from app.handlers.human_chat import human_callback
from app.handlers.human_message import human_message

telegram_app.add_handler(CallbackQueryHandler(human_callback))
telegram_app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, human_message))

from telegram.ext import MessageHandler, filters
from app.handlers.ai_chat import ai_callback
from app.handlers.ai_message import ai_message

telegram_app.add_handler(CallbackQueryHandler(ai_callback))
telegram_app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, ai_message))

from app.handlers.premium import premium_cmd, premium_callback
from app.webhook import cashfree_webhook

telegram_app.add_handler(CommandHandler("premium", premium_cmd))
telegram_app.add_handler(CallbackQueryHandler(premium_callback))

@app.post("/cashfree/webhook")
async def cashfree_hook(request: Request):
    return await cashfree_webhook(request)

from app.handlers.admin_status import status_cmd
from app.handlers.admin_id import id_cmd
from app.handlers.broadcast import broadcast_cmd
from app.handlers.admin_actions import ban_cmd, unban_cmd, warn_cmd

telegram_app.add_handler(CommandHandler("status", status_cmd))
telegram_app.add_handler(CommandHandler("id", id_cmd))
telegram_app.add_handler(CommandHandler("broadcast", broadcast_cmd))
telegram_app.add_handler(CommandHandler("ban", ban_cmd))
telegram_app.add_handler(CommandHandler("unban", unban_cmd))
telegram_app.add_handler(CommandHandler("warn", warn_cmd))

from app.config import BOT_TOKEN, BASE_URL, WEBHOOK_SECRET
from app.handlers.start import start
from app.handlers.chat import chat_cmd
from app.handlers.admin import ai_on, ai_off

app = FastAPI()
telegram_app = Application.builder().token(BOT_TOKEN).build()

telegram_app.add_handler(CommandHandler("start", start))
telegram_app.add_handler(CommandHandler("chat", chat_cmd))
telegram_app.add_handler(CommandHandler("ai_on", ai_on))
telegram_app.add_handler(CommandHandler("ai_off", ai_off))
telegram_app.add_handler(CommandHandler("giveaway", giveaway))

@app.on_event("startup")
async def on_startup():
    await telegram_app.initialize()
    await telegram_app.bot.set_webhook(
        url=f"{BASE_URL}/webhook",
        secret_token=WEBHOOK_SECRET
    )

@app.post("/webhook")
async def webhook(request: Request):
    update = Update.de_json(await request.json(), telegram_app.bot)
    await telegram_app.process_update(update)
    return {"ok": True}

@app.get("/health")
async def health():
    return {"status": "ok"}
