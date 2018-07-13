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
def add_exersize(message):
    return None


@bot.message_handler(content_types=["text"])
def repeat_all_messages(message):
    bot.send_message(message.chat.id, message.text)


if __name__ == '__main__':
    bot.polling(none_stop=True)
