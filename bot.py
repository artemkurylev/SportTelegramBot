import requests
import datetime
import telebot
import config
import psycopg2

bot = telebot.TeleBot(config.token)
params = {
  'database': 'dftilqnoe4t5kg',
  'user': 'jkcvzflxvnhqcq',
  'password': '80af35cf40ad6392d412671a379797fe9891cce47e525b87863aaa9728f0f784',
  'host': 'ec2-54-227-243-210.compute-1.amazonaws.com',
  'port': 5432
}
db = psycopg2.connect(**params)
cur = db.cursor()
db.autocommit = True


@bot.message_handler(commands=["start"])
def remember_user(message):
    username = message.from_user.username
    cur.execute("SELECT * FROM users WHERE name ='%s'" % username)
    record = cur.fetchone()
    if record is None:
        cur2 = db.cursor()
        cur2.execute("INSERT INTO users (name) VALUES ('%s')" % username)
        db.commit()
    bot.send_message(message.chat.id, "Добро пожаловать в программу для спортивного робота. Для добавления дневника "
                                      "испольузйте команду diary")


@bot.message_handler(commands=['diary'])
def create_diary(message):
    username = message.from_user.username
    cur.execute("SELECT * FROM users WHERE name ='%s'" % username)
    user_record = cur.fetchone()
    cur.execute("SELECT * FROM diaries  WHERE user_id = %s" % user_record[0])
    diary_record = cur.fetchone()
    if diary_record is None:
        cur.execute("INSERT INTO diaries (user_id) VALUES (%s)" % user_record[0])
        db.commit()
        bot.send_message(message.chat.id, "Ваш дневник создан!")
    else:
        bot.send_message(message.chat.id, "У вас уже есть дневник")


@bot.message_handler(content_types=["text"])
def repeat_all_messages(message):
    bot.send_message(message.chat.id, message.text)


if __name__ == '__main__':
    bot.polling(none_stop=True)
