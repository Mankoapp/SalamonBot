import json

from aiogram import Bot, Dispatcher, executor, types
import os
from aiogram.dispatcher.filters import Text
from main import collect_data
from aiogram.utils.markdown import hbold, hlink

bot = Bot(token="2098206295:AAGZOSJV44fdGMx1HfvbWt2NTcPwJwLFNlE", parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)

@dp.message_handler(commands="start")
async def start(message: types.Message):
    start_buttons = ["Кроссовки", "Видеокарты", "Гречка"]
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*start_buttons)
    await message.answer("Товары со скидкой", reply_markup=keyboard)


@dp.message_handler(Text(equals="Кроссовки"))
async def get_discount_sneakers(message: types.Message):
    await message.answer("Подождите..")

    collect_data()

    with open("result_data.json", encoding='utf-8') as file:
        data = json.load(file)

    for item in data:
        card = f"{hlink(item.get('title'), item.get('link'))}\n" \
               f"{hbold('Категория: ')} {item.get('category')}\n" \
               f"{hbold('Цена:')} {item.get('price_base')}\n" \
               f"{hbold('Цена со скидкой:')}- {item.get('discount_persent')}%: {item.get('price_sale')}"

        await message.answer(card)


def main():
    executor.start_polling(dp)


if __name__ == "__main__":
    main()