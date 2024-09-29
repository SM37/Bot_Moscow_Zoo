import telebot
import telebot.types

from MY_API import *
from config import *
from keyboards import *
from animals import *


bot = telebot.TeleBot(TOKEN)
all_animals = get_animals()

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def handle_start(message: telebot.types.Message):
    bot.send_sticker(message.chat.id, YTKA)
    bot.send_message(message.chat.id, START1, reply_markup=kb_menu)
    bot.send_message(message.chat.id, START2, reply_markup=kb_start)

# Обработчик команды /info
@bot.message_handler(commands=['info'])
def handle_info(message: telebot.types.Message):
    bot.send_message(message.chat.id, START1)

# Обработчик команды /help
@bot.message_handler(commands=['help'])
def handle_help(message: telebot.types.Message):
    bot.send_message(message.chat.id, commands)

# Обработчик текстовых сообщений
@bot.message_handler(content_types=['text'])
def handle_text(message: telebot.types.Message):
    message.text = message.text.lower()

    if message.text in responses:
        response = responses[message.text]
        if isinstance(response, list):
            for chunk in response:
                bot.send_message(message.chat.id, chunk,reply_markup= kb_menu)
        else:
            bot.send_message(message.chat.id, response, reply_markup= kb_menu)

    elif message.text in all_animals:
        
        info = get_info_animals(message.text.lower())
        link = dict_animal_and_img()

        if info:
            if len(info) > 4096:
                words = info.split()
                chunks = []
                current_chunk = []
                current_length = 0

                for word in words:
                    if current_length + len(word) + 1 > 4096:
                        chunks.append(" ".join(current_chunk))
                        current_chunk = [word]
                        current_length = len(word) + 1
                    else:
                        current_chunk.append(word)
                        current_length += len(word) + 1

                if current_chunk:
                    chunks.append(" ".join(current_chunk))

                for chunk in chunks:
                    bot.send_message(message.chat.id, chunk)
                if link:
                    link_value = link[message.text]
                    bot.send_message(message.chat.id, f"Вот оно! Красавец! Выше вы найдете его описание, а здесь – ссылка его фотографии: {link_value}", reply_markup=kb_from_end)
                else:
                    bot.send_message(message.chat.id, "К сожалению, ссылка на этого зверя пока недоступна", reply_markup=kb_from_end)
            else:
                bot.send_message(message.chat.id, info)
                if link:
                    link_value = link[message.text]
                    bot.send_message(message.chat.id, f"Вот оно! Красавец! Выше вы найдете его описание, а здесь – ссылка его фотографии: {link_value}", reply_markup=kb_from_end)
                else:
                    bot.send_message(message.chat.id, "К сожалению, ссылка на этого зверя пока недоступна", reply_markup=kb_from_end)
        else:
            bot.send_message(message.chat.id, info_var, reply_markup=kb_from_end)
            bot.send_message(message.chat.id, info, reply_markup=kb_from_end)

    elif message.text in who:
        bot.send_message(message.chat.id, text_info_from_who)
        text_info = who_info(text_from_p=message.text)
        bot.send_message(message.chat.id, text_info, reply_markup= kb_menu)

    elif message.text == "перейти на сайт":
        bot.send_message(message.chat.id, go_to_site, reply_markup= ks_site )

    else:
        bot.send_message(message.chat.id, not_found)

@bot.callback_query_handler(func=lambda call: call.data == 'start_test')
def callback_check(call):
    bot.send_message(call.message.chat.id, omosn)


def main():
    sait_parsing()
    html_save_animals()
    bot.polling()

if __name__ == "__main__":
    main()