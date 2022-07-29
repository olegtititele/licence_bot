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
from db.db import DB



bot = Bot(token=cf.TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

logging.basicConfig(level=logging.INFO)

class Admin(StatesGroup):
    alert = State()

@dp.message_handler(commands="start")
async def start_message(message: types.Message):
    db = DB()
    if not db.check_user(message.from_user.id):
        db.add_user(message.from_user.id)
    else:
        pass
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

@dp.message_handler(commands="admin")
async def admin_message(message: types.Message):
    db = DB()
    
    if message.chat.id in cf.admins_chat_id:
        await bot.send_message(
            chat_id=message.chat.id,
            text=f"<b>👑 Админ-панель \n\nВсего пользователей: {db.get_users_len()}</b>",
            parse_mode=ParseMode.HTML,
            reply_markup=keyboards.admin_kb
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

            file = InputFile(cf.price_video)
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

        elif call.data == "delivery":
            text = "<b>ДОСТАВКА 🚚</b>\n\nНемного расскажем как происходит доставка. Отправка происходит с помощью Почты России 1 класса. Сроки занимают примерно от 2 до 5 дней(зависит от города). Конкретное время доставки в ваш город можно будет узнать во время оформлении заказа."

            file = InputMedia(media=InputFile(cf.delivery_photo))
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
                reply_markup=keyboards.delivery_kb
            )
			
        elif call.data == "contacts":
            file = InputMedia(media=InputFile(cf.contacts_photo))
            await bot.edit_message_media(
                chat_id=call.from_user.id,
                message_id=call.message.message_id,
                media=file
            )
            await bot.edit_message_caption(
                chat_id=call.from_user.id,
                message_id=call.message.message_id,
                caption="<b>Наши контакты:</b>",
                parse_mode=ParseMode.HTML,
                reply_markup=keyboards.contacts_kb
            )


        elif call.data == "info":
            
            text = "<b>Вас приветствует сервис по продаже сувенирных прав! Немного расскажем, чем мы занимаемся.\n\nНаша команда изготавливает сувенирные водительские права. Во время работы используется профессиональное оборудование. Мы трудимся над каждым заказом и выполняем его качественно. Клиент всегда может рассказать свои пожелания, чтобы он остался доволен выполненной работой. Совершив у нас покупку, вы получаете качественный товар, который сможете использовать без всяких сомнений.\nP.S. Права являются сувенирными и могут использоваться исключительно для розыгрышей и постановок.\nОтветственность за использование сувениров изготовитель не несёт!</b>\n\n<u>Для заказа потребудется:</u>\n<b>1.</b> <code>Желаемое ФИО</code>\n<b>2.</b> <code>Город выдачи</code>\n<b>3.</b> <code>Желаемая дата рождения</code>\n<b>4.</b> <code>Фото</code>\n\nФото не обязательно делать в студии. Подойдёт селфи ровно спереди с хорошем освещением."

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
        elif call.data == "alert":
            await Admin.alert.set()
            
            await bot.edit_message_text(
                chat_id=call.from_user.id,
                message_id=call.message.message_id,
                text=f"<b>📝 Отправьте текст/фото с текстом рассылки:</b>",
                parse_mode=ParseMode.HTML,
                reply_markup=back_to_adm
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


@dp.message_handler(state=Admin.alert, content_types=types.ContentTypes.TEXT)
async def admin_alert(message: types.Message, state: FSMContext):

    db = DB()
    users = db.get_all_users()

    success, error, total = 0, 0, 0
    text = message.text
    for i in users:
        total+=1
        try:
            await bot.send_message(i[0], text)
            success+=1
        except:
            error+=1
    await state.finish()
    await bot.send_message(message.chat.id, f'Всего рассылок: {total}\nУспешно: {success}\nНеудачно: {error}')

@dp.message_handler(state=Admin.alert, content_types=types.ContentTypes.PHOTO)
async def admin_alert(message: types.Message, state: FSMContext):

    db = DB()
    users = db.get_all_users()

    success, error, total = 0, 0, 0
    file_id = message.photo[0].file_id
    text = message.caption
    for i in users:
        total+=1
        try:
            await bot.send_photo(i[0], file_id, caption=text)
            success+=1
        except:
            error+=1
    await state.finish()
    await bot.send_message(message.chat.id, f'Всего рассылок: {total}\nУспешно: {success}\nНеудачно: {error}')


@dp.callback_query_handler(state='*')
async def call_back(call: types.CallbackQuery, state: FSMContext):
    if call.data == "decline":
        await state.finish()
        await bot.delete_message(
            chat_id=call.from_user.id,
            message_id=call.message.message_id,
        )

def check_sub_channel(chat_member):
	if chat_member['status'] != 'left':
		return True
	else:
		return False


if __name__ == "__main__":
    # Запуск бота
    db = DB()
    db.create_users_table()
    executor.start_polling(dp, skip_updates=True)
