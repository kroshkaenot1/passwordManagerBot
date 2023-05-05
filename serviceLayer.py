import asyncio
import logging

import dbconfig


def find_user(tg_id):
    try:
        sql = 'SELECT * FROM users WHERE tg_id = {}'.format(tg_id)
        dbconfig.cursor.execute(sql)
        result = dbconfig.cursor.fetchall()
        if len(result) == 0:
            sql = 'INSERT INTO users (tg_id) VALUES ({})'.format(tg_id)
            dbconfig.cursor.execute(sql)
            dbconfig.connectDB.commit()
    except Exception as e:
        logging.error(e)
        raise e


def find_service(service_name):
    try:
        sql = 'SELECT * FROM services WHERE name = "{}"'.format(service_name)
        dbconfig.cursor.execute(sql)
        result = dbconfig.cursor.fetchall()
        if len(result) == 0:
            sql = 'INSERT INTO services (name) VALUES ("{}")'.format(service_name)
            dbconfig.cursor.execute(sql)
            dbconfig.connectDB.commit()
    except Exception as e:
        logging.error(e)
        raise e


def set_data(tg_id, service_name, login, password):
    if len(service_name) > 100 or len(login) > 50 or len(password) > 50:
        return "invalid"
    try:
        sql = 'SELECT * FROM passwords_info ' \
              'LEFT JOIN users ON passwords_info.user_id = users.id ' \
              'LEFT JOIN services ON passwords_info.service_id = services.id ' \
              'WHERE users.tg_id = {} AND services.name = "{}"'.format(tg_id, service_name)
        dbconfig.cursor.execute(sql)
        result = dbconfig.cursor.fetchall()

        if len(result) == 0:
            find_user(tg_id)
            find_service(service_name)
            sql = 'INSERT INTO passwords_info (user_id,service_id,login,password)' \
                  ' VALUES ((SELECT id FROM users WHERE tg_id = {}),' \
                  '(SELECT id FROM services WHERE name = "{}"),"{}","{}")' \
                  ''.format(tg_id, service_name, login, password)

            dbconfig.cursor.execute(sql)
            dbconfig.connectDB.commit()
            return "added"
        else:
            sql = 'UPDATE passwords_info ' \
                  'JOIN users ON passwords_info.user_id = users.id ' \
                  'JOIN services ON passwords_info.service_id = services.id ' \
                  'SET passwords_info.user_id = users.id, passwords_info.service_id = services.id, login = "{}",password = "{}"' \
                  'WHERE users.tg_id = {} AND services.name = "{}"'.format(login, password, tg_id, service_name)
            dbconfig.cursor.execute(sql)
            dbconfig.connectDB.commit()
            return "updated"
    except Exception as e:
        logging.error(e)
        raise e


def get_data(service_name, tg_id):
    try:
        sql = 'SELECT * FROM passwords_info ' \
              'LEFT JOIN users ON passwords_info.user_id = users.id ' \
              'LEFT JOIN services ON passwords_info.service_id = services.id ' \
              'WHERE users.tg_id = {} AND services.name = "{}"'.format(tg_id, service_name)
        dbconfig.cursor.execute(sql)
        return dbconfig.cursor.fetchall()
    except Exception as e:
        logging.error(e)
        raise e


def delete_data(service_name, tg_id):
    try:
        sql = 'DELETE passwords_info FROM passwords_info ' \
              'JOIN users ON passwords_info.user_id = users.id ' \
              'JOIN services ON passwords_info.service_id = services.id ' \
              'WHERE users.tg_id = {} AND services.name = "{}"'.format(tg_id, service_name)
        dbconfig.cursor.execute(sql)
        dbconfig.connectDB.commit()
        return dbconfig.cursor.rowcount
    except Exception as e:
        logging.error(e)
        raise e


async def delete_messages(*args, bot, loop):
    await asyncio.sleep(60)
    for message in args:
        bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    loop.stop()
