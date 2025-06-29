import asyncio
import logging
import datetime
import random
from aiogram import Bot, Dispatcher, types
from states import d
from secret import token
from db import users, profiles
from aiogram.types import BotCommand
from aiogram.filters.command import Command
from aiogram import F
from aiogram import html
from aiogram.filters import Command
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.client.default import DefaultBotProperties
from aiogram.utils.formatting import Text, Bold
from aiogram.enums.parse_mode import ParseMode
from aiogram.utils.keyboard import ReplyKeyboardBuilder

sts = list(d.keys())
logging.basicConfig(level=logging.INFO)
session = AiohttpSession()
bot = Bot(
    token=token,
    default=DefaultBotProperties(
        parse_mode=ParseMode.HTML
    ),
    session=session
)
dp = Dispatcher()


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
    content = Text(
        Bold(message.from_user.full_name),
        f" приговаривается к статье {cur1.split()[-1][:-1]}: {d[cur].strip()}"
    )
    await message.reply(
        **content.as_kwargs()
        )

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    if (message.from_user.full_name) not in users:
        users.add(message.from_user.full_name)
        profiles[message.from_user.full_name] = 0

    kb = [
        [
            types.KeyboardButton(text="Узнать статью"),
            types.KeyboardButton(text="В личное дело")
        ],
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder="Куда дальше?"
    )
    await message.answer(f"Здравствуйте, {html.bold(html.quote(message.from_user.full_name))}!", reply_markup=keyboard)

@dp.message(F.text.lower() == "узнать статью")
async def state(message: types.Message):
    usrtime = profiles[message.from_user.full_name]
    if (usrtime == 0 or datetime.datetime.now() - usrtime >= datetime.timedelta(hours=8)):
        profiles[message.from_user.full_name] = datetime.datetime.now()
        await cmd_reply3(message)
    else:
        await message.answer("Рано статью узнавать! Ещё ту не отбыли!")

@dp.message(F.text.lower() == "узнать статью")
async def state(message: types.Message):
    usrtime = profiles[message.from_user.full_name]
    if (usrtime == 0 or datetime.datetime.now() - usrtime >= datetime.timedelta(hours=8)):
        profiles[message.from_user.full_name] = datetime.datetime.now()
        await cmd_reply3(message)
    else:
        await message.answer("Рано статью узнавать! Ещё ту не отбыли!")

@dp.message(F.text.lower() == "в личное дело")
async def profile(message: types.Message):
    await message.reply("Данный раздел в разработке, ждите")

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