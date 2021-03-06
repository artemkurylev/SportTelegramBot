import psycopg2
import config


def get_current_state(message):
    config.cur.execute("SELECT * FROM users WHERE name = '%s'" % message.from_user.username)
    rec = config.cur.fetchone()
    config.cur.execute("SELECT * FROM training_status WHERE user_id = %s" % rec[0])
    record = config.cur.fetchone()
    return record[2]


def set_state(user_id, value):
    config.cur.execute("UPDATE training_status SET training_status = (%s) WHERE user_id = (%s)" % (value, user_id))
    config.db.commit()
