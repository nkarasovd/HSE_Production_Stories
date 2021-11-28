import os

import telebot

from answer import MessageHandler

with open("environment.env", 'r') as f:
    vars_dict = dict(
        tuple(line.split('='))
        for line in f.readlines() if not line.startswith('#')
    )
os.environ.update(vars_dict)

bot_token = os.getenv("TELEBOT_TOKEN").strip()

bot = telebot.TeleBot(bot_token)

message_handler = MessageHandler()


@bot.message_handler(commands=["start"])
def handle_greeting(message):
    greeting_text = "Привет, можешь спросить у меня погоду в любом городе на несколько дней.\n"
    info_text = "Вот примеры запросов, которые я могу обработать:\n" \
                "   \"Какая будет погода в Санкт-Петербурге 12.01.2021?\"\n" \
                "   \"Погода в Москве завтра\"\n" \
                "   \"Погода в спб с 12.01.2021 по 12.09.2021?\"\n"
    rule_text = "Не забывай, что города и населенные пункты надо писать с заглавной буквы!\n"
    rule_text_2 = "Дата указывается в формате МЕСЯЦ.ДЕНЬ.ГОД.\n"
    rule_text_3 = "Если дата не указана, то вернется прогноз на текущую дату.\n"
    end_text = "Приятного общения, надеюсь, что буду полезен \N{winking face}."

    message_text = greeting_text + info_text + rule_text + rule_text_2 + rule_text_3 + end_text
    bot.send_message(message.chat.id, message_text)


@bot.message_handler(func=lambda m: True)
def handle_message(message):
    answer = message_handler.get_answer(message.text)
    bot.send_message(message.chat.id, answer)


if __name__ == '__main__':
    bot.polling()
