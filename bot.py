import logging
import random
import re
from aiogram import Bot, Dispatcher, executor, types

from aiogram import types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.types import InputFile, InputMedia
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from telegram import ParseMode
from keyboards import *

import config.config as cf



bot = Bot(token=cf.TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

logging.basicConfig(level=logging.INFO)


@dp.message_handler(commands="start")
async def start_message(message: types.Message):
    if check_sub_channel(await bot.get_chat_member(chat_id=cf.channel_chat_id, user_id=message.from_user.id)):

        await bot.send_message(
                chat_id=message.chat.id,
                text=f"<b>{message.from_user.first_name}, Добро пожаловать!</b>",
                parse_mode=ParseMode.HTML,
                reply_markup=keyboards.main_menu_kb
            )

        photo = InputFile(cf.main_menu_photo)
        await bot.send_photo(
            chat_id=message.chat.id, 
            photo=photo, 
            caption="<b>Всю актуальную информацию вы сможете узнать здесь!\nБот всегда обновляется и доносит самую актуальную информацию.\n\nСтатус проекта:</b> <code>Работаю👌</code>", 
            parse_mode=ParseMode.HTML, 
            reply_markup=keyboards.menu_kb
        )
    else:
        link = f'<a href="{cf.channel_link}">канал</a>'
        text = f"<b>❕ Для того чтобы пользоваться ботом, вы должны быть подписаны на {link}.</b>"
        await bot.send_message(
            chat_id=message.chat.id,
            text=text,
            parse_mode=ParseMode.HTML,
            reply_markup=keyboards.check_sub_kb
        )

@dp.message_handler()
async def message_handler(message: types.Message):
    if check_sub_channel(await bot.get_chat_member(chat_id=cf.channel_chat_id, user_id=message.from_user.id)):
        if message.text == "🏠 Меню":
            await bot.send_message(
                chat_id=message.chat.id,
                text=f"<b>{message.from_user.first_name}, Добро пожаловать!</b>",
                parse_mode=ParseMode.HTML,
                reply_markup=keyboards.main_menu_kb
            )

            photo = InputFile(cf.main_menu_photo)
            await bot.send_photo(
                chat_id=message.chat.id, 
                photo=photo, 
                caption="<b>Всю актуальную информацию вы сможете узнать здесь!\nБот всегда обновляется и доносит самую актуальную информацию.\n\nСтатус проекта:</b> <code>Работаю👌</code>", 
                parse_mode=ParseMode.HTML, 
                reply_markup=keyboards.menu_kb
            )
    else:
        link = f'<a href="{cf.channel_link}">канал</a>'
        text = f"<b>❕ Для того чтобы пользоваться ботом, вы должны быть подписаны на {link}.</b>"
        await bot.send_message(
            chat_id=message.chat.id,
            text=text,
            parse_mode=ParseMode.HTML,
            reply_markup=keyboards.check_sub_kb
        )
@dp.callback_query_handler()
async def call_back(call: types.CallbackQuery):
    if check_sub_channel(await bot.get_chat_member(chat_id=cf.channel_chat_id, user_id=call.from_user.id)):
        if call.data == "prices":

            text = "<b>СУВЕНИРНЫЕ ПРАВА 🪪</b>\n✅ Голографический ламинат - переливающиеся знаки.\n✅ Присутствует микротекст - очень качественная печать.\n<b>❗️ПЕЧАТЬ ПО МИКРО-ВОЛОКОННОЙ ПЛОТНОЙ БУМАГЕ ПОВЫШЕННОГО КАЧЕСТВА (как оригинал)❗️</b>\n\n<u>Подходит для: </u>\n<b>✔️ Клубов\n✔️ Покупки табачки везде\n✔️ Приёма посылок\n✔️ Понтов перед друзьями\n✔️ Всего, где нужно быть немного старше</b>"

            file = InputMedia(media=InputFile(cf.price_photo))
            await bot.edit_message_media(
                chat_id=call.from_user.id,
                message_id=call.message.message_id,
                media=file
            )
            await bot.edit_message_caption(
                chat_id=call.from_user.id,
                message_id=call.message.message_id,
                caption=text,
                parse_mode=ParseMode.HTML,
                reply_markup=keyboards.prices_kb
            )

        
        elif call.data == "contacts":
            await bot.edit_message_caption(
                chat_id=call.from_user.id,
                message_id=call.message.message_id,
                caption="<b>Наши контакты:</b>",
                parse_mode=ParseMode.HTML,
                reply_markup=keyboards.contacts_kb
            )


        elif call.data == "info":
            
            text = "<b>Вас приветствует сервис по продаже сувенирных прав! Немного расскажем, чем мы занимаемся.\n\nНаша команда изготавливает сувенирные водительские права. Во время работы использовать профессиональное оборудование. Над каждым заказом трудятся и выполняют его качественно. Мы прислушиваемся к пожеланиям клиента и делаем так, чтобы он был полностью доволен выполненной работы. Совершив у нас покупку, вы получаете качественный товар, который сможете использовать без всяких сомнений.\nP.S. Права являются сувенирными и могут использоваться исключительно для розыгрышей и постановок.\nОтветственность за использование сувениров изготовитель не несёт!</b>\n\n<u>Для заказа потребудется:</u>\n<b>1.</b> <code>Желаемое ФИО</code>\n<b>2.</b> <code>Город выдачи</code>\n<b>3.</b> <code>Желаемая дата рождения</code>\n<b>4.</b> <code>Фото</code>\n\nФото не обязательно делать в студии. Подойдёт селфи ровно спереди с хорошем освещением."

            await bot.edit_message_caption(
                chat_id=call.from_user.id,
                message_id=call.message.message_id,
                caption=text,
                parse_mode=ParseMode.HTML,
                reply_markup=keyboards.info_kb
            )


        elif call.data == "back_to_menu":

            file = InputMedia(media=InputFile(cf.main_menu_photo))
            await bot.edit_message_media(
                chat_id=call.from_user.id,
                message_id=call.message.message_id,
                media=file
            )
            await bot.edit_message_caption(
                chat_id=call.from_user.id,
                message_id=call.message.message_id,
                caption="<b>Всю актуальную информацию вы сможете узнать здесь!\nБот всегда обновляется и доносит самую актуальную информацию.\n\nСтатус проекта:</b> <code>Работаю👌</code>",
                parse_mode=ParseMode.HTML,
                reply_markup=keyboards.menu_kb
            )

        elif call.data == "check_sub":
            await bot.send_message(
                chat_id=call.from_user.id,
                text=f"<b>{call.from_user.first_name}, Добро пожаловать!</b>",
                parse_mode=ParseMode.HTML,
                reply_markup=keyboards.main_menu_kb
            )

            photo = InputFile(cf.main_menu_photo)
            await bot.send_photo(
                chat_id=call.from_user.id,
                photo=photo, 
                caption="<b>Всю актуальную информацию вы сможете узнать здесь!\nБот всегда обновляется и доносит самую актуальную информацию.\n\nСтатус проекта:</b> <code>Работаю👌</code>", 
                parse_mode=ParseMode.HTML, 
                reply_markup=keyboards.menu_kb
            )
    else:
        link = f'<a href="{cf.channel_link}">канал</a>'
        text = f"<b>❕ Для того чтобы пользоваться ботом, вы должны быть подписаны на {link}.</b>"
        await bot.send_message(
            chat_id=call.from_user.id,
            text=text,
            parse_mode=ParseMode.HTML,
            reply_markup=keyboards.check_sub_kb
        )

def check_sub_channel(chat_member):
	if chat_member['status'] != 'left':
		return True
	else:
		return False


if __name__ == "__main__":
    # Запуск бота
    executor.start_polling(dp, skip_updates=True)