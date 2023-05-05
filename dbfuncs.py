import dbconfig


def find_user(user_id):
    sql = 'SELECT * FROM users WHERE tg_id = {}'.format(user_id)
    dbconfig.cursor.execute(sql)
    result = dbconfig.cursor.fetchall()
    if len(result) == 0:
        sql = 'INSERT INTO users (tg_id) VALUES ({})'.format(user_id)
        dbconfig.cursor.execute(sql)
        dbconfig.connectDB.commit()


def find_service(service_name):
    sql = 'SELECT * FROM services WHERE name = "{}"'.format(service_name)
    dbconfig.cursor.execute(sql)
    result = dbconfig.cursor.fetchall()
    if len(result) == 0:
        sql = 'INSERT INTO services (name) VALUES ("{}")'.format(service_name)
        dbconfig.cursor.execute(sql)
        dbconfig.connectDB.commit()


def set_data(user_id, service_name, login, password):
    if len(service_name) > 100 or len(login) > 50 or len(password) > 50:
        return "invalid"

    sql = 'SELECT * FROM passwords_info ' \
          'LEFT JOIN users ON passwords_info.user_id = users.id ' \
          'LEFT JOIN services ON passwords_info.service_id = services.id ' \
          'WHERE users.tg_id = {} AND services.name = "{}"'.format(user_id, service_name)
    dbconfig.cursor.execute(sql)
    result = dbconfig.cursor.fetchall()

    if len(result) == 0:
        find_user(user_id)
        find_service(service_name)
        sql = 'INSERT INTO passwords_info (user_id,service_id,login,password)' \
              ' VALUES ((SELECT id FROM users WHERE tg_id = {}),' \
              '(SELECT id FROM services WHERE name = "{}"),"{}","{}")' \
              ''.format(user_id, service_name, login, password)

        dbconfig.cursor.execute(sql)
        dbconfig.connectDB.commit()
        return "added"
    else:
        sql = 'UPDATE passwords_info ' \
              'JOIN users ON passwords_info.user_id = users.id ' \
              'JOIN services ON passwords_info.service_id = services.id ' \
              'SET passwords_info.user_id = users.id, passwords_info.service_id = services.id, login = "{}",password = "{}"' \
              'WHERE users.tg_id = {} AND services.name = "{}"'.format(login, password, user_id, service_name)
        dbconfig.cursor.execute(sql)
        dbconfig.connectDB.commit()
        return "updated"
