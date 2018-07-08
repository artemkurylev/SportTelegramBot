import requests
import datetime
import psycopg2


class BotHandler:

    def __init__(self, token):
        self.token = token
        self.api_url = "https://api.telegram.org/bot{}/".format(token)

    def get_updates(self, offset=None, timeout=30):
        method = 'getUpdates'
        params = {'timeout': timeout, 'offset': offset}
        response = requests.get(self.api_url + method, params)
        result_json = response.json()['result']
        return result_json

    def get_last_update(self):
        get_result = self.get_updates()
        if len(get_result) > 0:
            last_update = get_result[-1]
        else:
            last_update = get_result[len(get_result)]

        return last_update

    def send_message(self, chat_id, text):
        params = {'chat_id': chat_id, 'text': text}
        method = 'sendMessage'
        response = requests.post(self.api_url + method, params)
        return response


myBot = BotHandler('554026510:AAHQahqhMAwffu4qWQSa0JZPJjDLamDtXO4')
greetings = ('здравствуй', 'привет', 'ку', 'здорово')
now = datetime.datetime.now()
params = {
  'database': 'dftilqnoe4t5kg',
  'user': 'jkcvzflxvnhqcq',
  'password': '80af35cf40ad6392d412671a379797fe9891cce47e525b87863aaa9728f0f784',
  'host': 'ec2-54-227-243-210.compute-1.amazonaws.com',
  'port': 5324
}
db = psycopg2.connect(**params)


def main():
    new_offset = None
    today = now.day
    hour = now.hour
    while True:
        myBot.get_updates(new_offset)

        last_update = myBot.get_last_update()

        last_update_id = last_update['update_id']
        last_chat_text = last_update['message']['text']
        last_chat_id = last_update['message']['chat']['id']
        last_chat_name = last_update['message']['chat']['first_name']
        cur = db.cursor()
        data = cur.execute("Select * FROM users where  user.id == %s", 'last_update_id')
        if data is None:
            cur.execute("Insert Into users values (:id, :name)", {"id": last_update_id, "name": last_chat_name})
        if last_chat_text.lower() in greetings and today == now.day and 6 <= hour < 12:
            myBot.send_message(last_chat_id, 'Доброе утро{}'.format(last_chat_name))
            today += 1
        elif last_chat_text.lower() in greetings and today == now.day and 12 <= hour < 17:
            myBot.send_message(last_chat_id, 'Добрый день{}'.format(last_chat_name))
            today += 1
        elif last_chat_text.lower() in greetings and today == now.day and 17 <= hour < 23:
            myBot.send_message(last_chat_id, 'Добрый вечер{}'.format(last_chat_name))
            today += 1

        new_offset = last_update_id + 1


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        exit()

