import asyncio
import logging
import random
from aiogram import Bot, Dispatcher, types
from states import d
from aiogram.types import BotCommand
from aiogram.filters.command import Command
from aiogram import F
from aiogram import html
from aiogram.filters import Command
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.client.default import DefaultBotProperties
from aiogram.enums.parse_mode import ParseMode

sts = list(d.keys())
logging.basicConfig(level=logging.INFO)
session = AiohttpSession()
bot = Bot(
    token='7363480889:AAFPN-NfCyYQ9phBaGy2fzL6oETL8BTEaWo',
    default=DefaultBotProperties(
        parse_mode=ParseMode.HTML
    ),
    session=session
)
dp = Dispatcher()

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Hello!")

@dp.message(Command("reply"))
async def cmd_reply1(message: types.Message):
    await message.reply('Это ответ с "ответом"')

@dp.message(Command("kardano"))
async def cmd_reply2(message: types.Message):
    await message.reply('1000-7 ZXC')

@dp.message(Command("my_statia"))
async def cmd_reply3(message: types.Message):
    cur = random.choice(sts)
    cur1 = cur.replace("_", ".")
    await message.reply(
        f"<b>{message.from_user.full_name}</b> приговаривается к статье {cur1.split()[-1][:-1]}: {d[cur].strip()}",
        parse_mode=ParseMode.HTML
        )

# Debug!
async def set_main_menu(bot: Bot):
    main_menu_commands = [
        BotCommand(command='/start',
                   description='Справка по работе бота'),
        BotCommand(command='моя статья',
                   description='Ваша статья сегодня'),
        BotCommand(command='/contacts',
                   description='Другие способы связи'),
        BotCommand(command='/payments',
                   description='Платежи')
    ]
    await bot.set_my_commands(main_menu_commands)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())