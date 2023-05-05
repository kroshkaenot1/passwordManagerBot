import dbconfig
import telebot
import dbfuncs
TOKEN = '6081656901:AAFhUzEE_gjEeW1Xe2AnGYAIZ_wuSE7N8og'

bot = telebot.TeleBot(TOKEN)


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
    service_name = message.text
    bot.send_message(chat_id=chat_id, text="Введите логин")
    bot.register_next_step_handler(message, input_login, service_name)


def input_login(message, service_name):
    chat_id = message.chat.id
    login = message.text
    bot.send_message(chat_id=chat_id, text="Введите пароль")
    bot.register_next_step_handler(message, input_password, service_name, login)


def input_password(message, service_name, login):
    user_id = message.from_user.id
    chat_id = message.chat.id
    password = message.text
    result = dbfuncs.set_data(user_id,service_name,login,password)
    if result == "added":
        bot.send_message(chat_id=chat_id, text="Вы успешно добавили новую запись для {}\nЛогин: {}\nПароль: {}"
                     .format(service_name, login, password))
    elif result == "updated":
        bot.send_message(chat_id=chat_id, text="Вы успешно обновили свои данные для {}\nЛогин: {}\nПароль: {}"
                         .format(service_name, login, password))
    elif result == "invalid":
        bot.send_message(chat_id=chat_id, text="Вы ввели значение/значения недопустимой длины")

@bot.message_handler(commands=["get"])
def get(message):
    pass


@bot.message_handler(commands=["del"])
def dell(message):
    pass


if __name__ == '__main__':
    bot.polling()
