import telebot
from telebot import types


# Обычные клавиатуры
kb_menu = types.ReplyKeyboardMarkup(resize_keyboard=True)
kb_menu.add(types.KeyboardButton(text='Пройти тест'))
kb_menu.add(types.KeyboardButton(text='Кто такие...'))
kb_menu.add(types.KeyboardButton(text='Перейти на сайт'))

kb_from1 = types.ReplyKeyboardMarkup(resize_keyboard=True)
kb_from1.add(types.KeyboardButton(text='Пройти тест'))
kb_from1.add(types.KeyboardButton(text='Перейти на сайт'))

kb_test1 = types.ReplyKeyboardMarkup(resize_keyboard=True)
kb_test1.add(types.KeyboardButton(text='Кто такие...'))

kb_from_end = types.ReplyKeyboardMarkup(resize_keyboard=True)
kb_from_end.add(types.KeyboardButton(text='Пройти еще раз'))
kb_from_end.add(types.KeyboardButton(text='Перейти на сайт'))
kb_from_end.add(types.KeyboardButton(text='Кто такие...'))
kb_from_end.add(types.KeyboardButton(text='Назад'))

# Инлайн-клавиатуры
ks_site = types.InlineKeyboardMarkup()
ks_site.add(types.InlineKeyboardButton(text='Перейти на сайт', url='https://moscowzoo.ru/'))
ks_site.add(types.InlineKeyboardButton(text='Назад', callback_data='back'))

kb_start = types.InlineKeyboardMarkup()
kb_start.add(types.InlineKeyboardButton(text='Начать тест', callback_data='start_test'))
kb_start.add(types.InlineKeyboardButton(text='Перейти на сайт', url='https://moscowzoo.ru/'))

