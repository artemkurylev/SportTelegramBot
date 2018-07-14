import requests
import datetime
import telebot
import config
import psycopg2
import exersize_worker

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
    set_of_records = "Список возможных возможных упажнений(Если вашего упражнения в списке нет, введите его отдельно)" \
                     ":\r\n"
    while i < len(records):
        set_of_records += records[i][0] + "\r\n"
        i += 1
    bot.send_message(message.chat.id, set_of_records)


@bot.message_handler(func=lambda message: exersize_worker.get_current_state(message ==
                                                                            config.ExersizeStates.S_EXERSIZE.value))
def add_exersize(message):
    return None


@bot.message_handler(content_types=["text"])
def repeat_all_messages(message):
    bot.send_message(message.chat.id, message.text)


if __name__ == '__main__':
    bot.polling(none_stop=True)
