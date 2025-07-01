import asyncio
import logging
import datetime
import random
import base64
import re
from aiogram import Bot, Dispatcher, types
from states import d, get_full
from secret import token
from db import users, profiles
from aiogram.types import BotCommand
from aiogram.filters.command import Command
from aiogram import F
from aiogram import html
from aiogram.utils import deep_linking 
from aiogram.filters import Command, CommandStart
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.client.default import DefaultBotProperties
from aiogram.utils.formatting import Text, Bold
from aiogram.enums.parse_mode import ParseMode
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

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
user_data = {}

@dp.message(Command("reply"))
async def cmd_reply1(message: types.Message):
    await message.reply('Это ответ с "ответом"')

@dp.message(Command("kardano"))
async def cmd_reply2(message: types.Message):
    await message.reply('1000-7 ZXC')

# For testing only!!!
@dp.message(Command("my_statia"))
async def cmd_reply3(message: types.Message):
    cur = random.choice(sts)
    cur1 = cur.replace("_", ".")
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(
        text="Полный текст статьи",
        callback_data="num_" + str(cur) + "_" + str(message.from_user.id))
    )
    st_numb: int = cur1.split()[-1][:-1]
    profiles[message.from_user.full_name]["stl"] = cur
    await message.answer(

        f"{html.bold(html.quote(message.from_user.full_name))} приговаривается к статье {st_numb}: {d[cur].strip()}",
        reply_markup=builder.as_markup()
    )

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    usr = message.from_user.full_name
    com, *args = message.text.split()
    if (usr) not in users:
        users.add(usr)
        profiles[usr] = {"stl": None, "time": datetime.datetime(2000, 1, 1),
                         "till_upd": datetime.timedelta(hours=8), "years": None, "invited":  0}
    kb = [
        [types.KeyboardButton(text="Узнать статью"), types.KeyboardButton(text="В личное дело"), types.KeyboardButton(text="Донат")],
        [types.KeyboardButton(text="Реферальная программа")]
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder="Куда дальше?"
    )
    print(profiles, message.text)
    if args: 
        ref_nm = args[0].encode('utf-8')
        print(ref_nm)
        padding_needed = (4 - len(ref_nm) % 4) % 4
        padded_string = ref_nm + b'=' * padding_needed
        ref_nm = base64.b64decode(padded_string).decode('utf-8')
        print(ref_nm, "addded_user")
        profiles[ref_nm]["invited"] += 1

    await message.answer(f"Здравствуйте, {html.bold(html.quote(message.from_user.full_name))}!", reply_markup=keyboard)

def decode_base64(ref_nm):
  try:
    decoded_bytes = base64.b64decode(ref_nm)
    decoded_string = decoded_bytes.decode('utf-8')
    return decoded_string
  except (TypeError, ValueError) as e:
    print(f"Ошибка при декодировании: {e}")
    return None

@dp.message(F.text.lower() == "узнать статью")
@dp.message(F.text.lower() == "моя статья")
@dp.message(F.text.lower() == "мая статья")
async def state(message: types.Message):
    usr = message.from_user.full_name
    usrtime = profiles[user]["time"]
    if (usrtime == 0 or datetime.datetime.now() - usrtime >= profiles[usr]["till_upd"]):
        profiles[message.from_user.full_name]["time"] = datetime.datetime.now()
        await cmd_reply3(message)
    else:
        await message.answer("Рано статью узнавать! Ещё ту не отбыли!")

@dp.callback_query(F.data.startswith("num_"))
async def callbacks_num(callback: types.CallbackQuery):
    action = callback.data.split("_")
    print(action)
    await bot.send_message(action[2], get_full(str(action[1].split()[-1]).strip(".") + "."))

@dp.message(F.text.lower() == "в личное дело")
async def profile(message: types.Message):
    usr = message.from_user.full_name
    print(datetime.timedelta(hours=8) - (datetime.datetime.now() - profiles[usr]['time']))
    text = (
        f"Ваше имя: <u>{usr}</u>\nПоследняя статья: {profiles[usr]['stl']}\n\
Ваш ожидаемый срок: {profiles[usr]['years']}\n\
До следующей статьи: {max(datetime.timedelta(hours=0), datetime.timedelta(hours=8) - (datetime.datetime.now() - profiles[usr]['time']))}"
        )
    await message.reply(text, parse_mode="HTML")

@dp.message(F.text.lower() == "реферальная программа") 
async def referral(message: types.Message): 
    link = await deep_linking.create_start_link(bot, str(message.from_user.full_name), encode=True) 
    await message.answer(
        f"<i>Ваша пригласительная ссылка: </i> {link}\n{'-' * (len(link) + 56)}\n"
        
        f"<i>Приглашено ползователей: </i> {profiles[message.from_user.full_name]['invited']}", parse_mode="HTML"
        ) 
    
@dp.message(F.text.lower() == "донат")
async def donate(message: types.Message):
    await message.reply("Раздел донатов пока в разработке.")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
    print(profiles)
