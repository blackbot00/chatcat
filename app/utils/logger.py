from telegram import Bot
from app.config import BOT_TOKEN

bot = Bot(BOT_TOKEN)

GROUP_1_LOG = -1001111111111  # replace
GROUP_2_LOG = -1002222222222  # replace

async def log_group1(text: str):
    await bot.send_message(GROUP_1_LOG, text)

async def log_group2(text: str):
    await bot.send_message(GROUP_2_LOG, text)
