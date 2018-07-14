import requests
import datetime
import telebot
import config
import psycopg2
import exersize_worker
import datetime
import statistics_worker

bot = telebot.TeleBot(config.token)

config.db.autocommit = True


@bot.message_handler(commands=["start"])
def remember_user(message):
    username = message.from_user.username
    config.cur.execute("SELECT * FROM users WHERE name ='%s'" % username)
    record = config.cur.fetchone()
    if record is None:
        config.cur.execute("INSERT INTO users (name) VALUES ('%s')" % username)
        config.db.commit()
    bot.send_message(message.chat.id, "Добро пожаловать в программу для спортивного робота. Для добавления дневника "
                                      "испольузйте команду diary")


@bot.message_handler(commands=['diary'])
def create_diary(message):
    username = message.from_user.username
    config.cur.execute("SELECT * FROM users WHERE name ='%s'" % username)
    user_record = config.cur.fetchone()
    config.cur.execute("SELECT * FROM diaries  WHERE user_id = %s" % user_record[0])
    diary_record = config.cur.fetchone()
    if diary_record is None:
        config.cur.execute("INSERT INTO diaries (user_id) VALUES (%s)" % user_record[0])
        config.db.commit()
        bot.send_message(message.chat.id, "Ваш дневник создан!")
    else:
        bot.send_message(message.chat.id, "У вас уже есть дневник")


@bot.message_handler(commands=['упражнение'])
def use_exersize(message):
    username = message.from_user.username
    config.cur.execute("SELECT * FROM users WHERE name = '%s'" % username)
    record_user = config.cur.fetchone()
    config.cur.execute("SELECT * FROM exersize_status WHERE user_id = %s" % record_user[0])
    record_status = config.cur.fetchone()
    if record_status is None:
        config.cur.execute("INSERT INTO exersize_status (status, user_id) VALUES (%s, %s) " % (0, record_user[0]))
    else:
        exersize_worker.set_state(record_user[0], 0)
    config.cur.execute("SELECT name FROM exersize_types")
    records = config.cur.fetchall()
    i = 0
    set_of_records = "Список возможных возможных упражнений(Если вашего упражнения в списке нет, введите его отдельно)" \
                     ":\r\n"
    while i < len(records):
        set_of_records += records[i][0] + "\r\n"
        i += 1
    bot.send_message(message.chat.id, set_of_records)


@bot.message_handler(commands=['статистика'])
def open_statistics(message):
    config.cur.execute("SELECT * FROM users WHERE name = '%s'" % message.from_user.username)
    record_user = config.cur.fetchone()
    config.cur.execute("SELECT * FROM statistics_status WHERE user_id = %s" % record_user[0])
    record_statistics = config.cur.fetchone()
    if record_statistics is None:
        config.cur.execute("INSERT INTO statistics_status (user_id, status) VALUES (%s, %s)" % (record_user[0], 0))
        config.db.commit()
    else:
        statistics_worker.set_state(record_user[0], config.StatisticsStatus.S_EXERSIZE[0])
    config.cur.execute("SELECT name FROM exersize_types")
    records = config.cur.fetchall()
    i = 0
    set_of_records = "Введите упражнение, для которго хотите посмотреть статистику:\r\n"
    while i < len(records):
        set_of_records += records[i][0] + "\r\n"
        i += 1
    bot.send_message(message.chat.id, set_of_records)


@bot.message_handler(func=lambda message: exersize_worker.get_current_state(message) ==
                                          config.ExersizeStates.S_EXERSIZE[0])
def add_exersize(message):
    config.cur.execute("SELECT * FROM exersize_types WHERE name = '%s'" % message.text)
    record_ex = config.cur.fetchone()
    if record_ex is None:
        config.cur.execute("INSERT INTO exersize_types (name) VALUES ('%s')" % message.text)
    config.cur.execute("SELECT * FROM users WHERE name = '%s'" % message.from_user.username)
    record_user = config.cur.fetchone()
    exersize_worker.set_state(record_user[0], config.ExersizeStates.S_GOT[0])
    date = datetime.date.today()
    config.cur.execute("INSERT INTO exersize (name,user_id, exersize_date) VALUES ('%s',%s,'%s')" %
                       (message.text, record_user[0], date))
    bot.send_message(message.chat.id, "Отлично, теперь введите вес с которым вы делали данное упражнение:")


@bot.message_handler(func=lambda message: exersize_worker.get_current_state(message) ==
                                          config.ExersizeStates.S_GOT[0])
def add_exersize_weight(message):
    if message.text.isdigit() is not True:
        bot.send_message(message.chat.id, "Вес должен представлять из себя число!")
    else:
        weight = int(message.text)
        if weight > 1000:
            bot.send_message(message.chat.id, "Введите корректный вес")
        else:
            config.cur.execute("SELECT * FROM users WHERE name = '%s'" % message.from_user.username)
            record_user = config.cur.fetchone()
            config.cur.execute("SELECT * FROM exersize WHERE user_id = %s ORDER BY id" % record_user[0])
            records_exersize = config.cur.fetchall()
            config.cur.execute("UPDATE exersize SET weight = (%s) WHERE id = (%s)" %
                               (weight, records_exersize[len(records_exersize) - 1][4]))
            bot.send_message(message.chat.id, "Вес добавлен, теперь введите кол-во повторений")
            exersize_worker.set_state(record_user[0], config.ExersizeStates.S_GOT_WEIGHT[0])


@bot.message_handler(func=lambda message: exersize_worker.get_current_state(message) ==
                                          config.ExersizeStates.S_GOT_WEIGHT[0])
def add_exersize_reps(message):
    if message.text.isdigit() is not True:
        bot.send_message(message.chat.id, "Вес должен представлять из себя число!")
    else:
        reps = int(message.text)
        if reps > 100:
            bot.send_message(message.chat.id, "Введите корректное количество повторений")
        else:
            config.cur.execute("SELECT * FROM users WHERE name = '%s'" % message.from_user.username)
            record_user = config.cur.fetchone()
            config.cur.execute("SELECT * FROM exersize WHERE user_id = %s ORDER BY id" % record_user[0])
            records_exersize = config.cur.fetchall()
            config.cur.execute("UPDATE exersize SET reps = (%s) WHERE id = (%s)" %
                               (reps, records_exersize[len(records_exersize) - 1][4]))
            bot.send_message(message.chat.id, "Кол-во повторений добавлено! Упражнение добавлено!")
            exersize_worker.set_state(record_user[0], config.ExersizeStates.S_GOT_REPS[0])


@bot.message_handler(content_types=["text"])
def repeat_all_messages(message):
    bot.send_message(message.chat.id, message.text)


if __name__ == '__main__':
    bot.polling(none_stop=True)
