from aiogram.types import ReplyKeyboardRemove, \
	ReplyKeyboardMarkup, KeyboardButton, \
	InlineKeyboardMarkup, InlineKeyboardButton
from aiogram import types

import config.config as cf


back_to_menu_btn = InlineKeyboardButton("🔙 Назад", callback_data="back_to_menu")

# Клавиатура главного меню
prices_btn = InlineKeyboardButton('Цена', callback_data='prices')
delivery_btn = InlineKeyboardButton('Доставка', callback_data='delivery')
contacts_btn = InlineKeyboardButton('Контакты', callback_data='contacts')
info_btn = InlineKeyboardButton('Info', callback_data='info')
menu_kb = InlineKeyboardMarkup()
menu_kb.add(prices_btn, delivery_btn)
menu_kb.add(contacts_btn, info_btn)


# Клавиатура цен
prices_kb = InlineKeyboardMarkup()
# for key in cf.price_dict:
#     inline_btn = InlineKeyboardButton(key, callback_data=cf.price_dict[key])
#     prices_kb.add(inline_btn)
prices_kb.add(back_to_menu_btn)


# Клавиатура контактов

contacts_kb = InlineKeyboardMarkup()
admin_btn = InlineKeyboardButton('Покупка', url=f"{cf.admin_link}")
channel_btn = InlineKeyboardButton('Канал', url=f"{cf.channel_link}")

contacts_kb.add(admin_btn, channel_btn)
contacts_kb.add(back_to_menu_btn)

# Клавиатура информации

info_kb = InlineKeyboardMarkup()
info_kb.add(back_to_menu_btn)

# Клавиатура информации

check_sub_kb = InlineKeyboardMarkup()

check_sub_btn = InlineKeyboardButton('Проверить подписку', callback_data="check_sub")
check_sub_kb.add(check_sub_btn)

# Кнопка меню

menu_btn = KeyboardButton('🏠 Меню')
main_menu_kb = ReplyKeyboardMarkup(
    resize_keyboard=True, one_time_keyboard=False
).add(menu_btn)

# Админ кнопки

admin_kb = InlineKeyboardMarkup()

alert_btn = InlineKeyboardButton('Рассылка', callback_data="alert")
admin_kb.add(alert_btn)

# fefeef
back_to_adm = InlineKeyboardMarkup()

back_btn = InlineKeyboardButton('Отменить', callback_data="decline")
back_to_adm.add(back_btn)
