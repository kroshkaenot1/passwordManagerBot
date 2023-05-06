import asyncio
import os
import telebot
import serviceLayer

bot = telebot.TeleBot(os.getenv('PMBTOKEN'))


@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(message.chat.id, "Доброго времени суток! Я могу помочь вам запомнить ваши пароли,просто "
                                      "доверьтесь мне! К вашим паролям доступ имеете только вы.\n"
                                      "Все пароли хранятся в зашифрованном виде, ваши данные будут в безопасности!\n\n"
                                      "Вы можете использовать следующие комманды:\n"
                                      "/set - добавляет логин и пароль к сервису\n"
                                      "/get - получает логин и пароль по названию сервиса\n"
                                      "/del - удаляет данные для сервиса\n")


@bot.message_handler(commands=["set"])
def addRecord(message):
    chat_id = message.chat.id
    bot.send_message(chat_id=chat_id, text="Введите название сервиса")
    bot.register_next_step_handler(message, select_service)


def select_service(message):
    chat_id = message.chat.id
    if message.text is None or message.text.startswith("/"):
        bot.send_message(chat_id=chat_id, text="Вы ввели некорректное значение")
        return
    service_name = message.text
    bot.send_message(chat_id=chat_id, text="Введите логин")
    bot.register_next_step_handler(message, input_login, service_name)


def input_login(message, service_name):
    chat_id = message.chat.id
    if message.text is None or message.text.startswith("/"):
        bot.send_message(chat_id=chat_id, text="Вы ввели некорректное значение")
        return
    login = message.text
    bot.send_message(chat_id=chat_id, text="Введите пароль")
    bot.register_next_step_handler(message, input_password, service_name, login)


def input_password(message, service_name, login):
    user_id = message.from_user.id
    chat_id = message.chat.id

    if message.text is None or message.text.startswith("/"):
        bot.send_message(chat_id=chat_id, text="Вы ввели некорректное значение")
        return

    password = message.text
    result = serviceLayer.set_data(user_id, service_name, login, password)
    if result == "added":
        bot.send_message(chat_id=chat_id, text="Вы успешно добавили новую запись для {}\nЛогин: {}"
                         .format(service_name, login))
        info = bot.send_message(chat_id=chat_id, text="Пароль: {}".format(password))

        asyncio.new_event_loop().run_until_complete(
            serviceLayer.delete_messages(info, message, bot=bot, loop=asyncio.new_event_loop()))

    elif result == "updated":
        bot.send_message(chat_id=chat_id, text="Вы успешно обновили свои данные для {}\nЛогин: {}"
                         .format(service_name, login))
        info = bot.send_message(chat_id=chat_id, text="Пароль: {}".format(password))

        asyncio.new_event_loop().run_until_complete(
            serviceLayer.delete_messages(info, message, bot=bot, loop=asyncio.new_event_loop()))

    elif result == "invalid":
        bot.send_message(chat_id=chat_id, text="Вы ввели значение/значения недопустимой длины")


@bot.message_handler(commands=["get"])
def get(message):
    chat_id = message.chat.id
    bot.send_message(chat_id=chat_id, text="Введите название сервиса")
    bot.register_next_step_handler(message, search_data)


def search_data(message):
    user_id = message.from_user.id
    chat_id = message.chat.id

    if message.text is None or message.text.startswith("/"):
        bot.send_message(chat_id=chat_id, text="Вы ввели некорректное значение")
        return

    service_name = message.text
    result = serviceLayer.get_data(service_name, user_id)

    if len(result) == 0:
        bot.send_message(chat_id=chat_id, text="Записей для этого сервиса не найдено")

    else:
        bot.send_message(chat_id=chat_id, text="Найдена запись для {}\nЛогин: {}"
                         .format(result[0][8], result[0][3]))
        info = bot.send_message(chat_id=chat_id, text="Пароль: {}"
                                .format(result[0][4]))
        asyncio.new_event_loop().run_until_complete(
            serviceLayer.delete_messages(info, bot=bot, loop=asyncio.new_event_loop()))


@bot.message_handler(commands=["del"])
def dell(message):
    chat_id = message.chat.id
    bot.send_message(chat_id=chat_id, text="Введите название сервиса для удаления записи")
    bot.register_next_step_handler(message, del_data)


def del_data(message):
    user_id = message.from_user.id
    chat_id = message.chat.id

    if message.text is None or message.text.startswith("/"):
        bot.send_message(chat_id=chat_id, text="Вы ввели некорректное значение")
        return

    service_name = message.text
    result = serviceLayer.delete_data(service_name, user_id)

    if result == 0:
        bot.send_message(chat_id=chat_id, text="Записи с таким названием сервиса не найдено")

    elif result == 1:
        bot.send_message(chat_id=chat_id,
                         text="Запись с логином и паролем для сервиса {} была удалена".format(service_name))


if __name__ == '__main__':
    bot.polling()
