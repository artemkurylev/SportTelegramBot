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


@bot.message_handler(content_types=["text"])
def repeat_all_messages(message):
    bot.send_message(message.chat.id, message.text)


@bot.message_handler(commands=["start"])
def remember_user(message):
    record = cur.execute("Select * from users WHERE id=(%s)", message.chat.id)
    if record is None:
        cur.execute("Insert into users values (%s,%s)", [message.chat.id, message.chat.first_name])


if __name__ == '__main__':
    bot.polling(none_stop=True)
