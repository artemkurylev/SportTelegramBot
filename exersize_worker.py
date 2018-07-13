import psycopg2
import config


def get_current_state(user_id):
    config.cur.execute("SELECT * FROM exersize_status WHERE user_id = %s" % user_id)
    record = config.cur.fetchone()
    return record[0]


def set_state(user_id, value):
    config.cur.execute("UPDATE exersize_status SET status = %s WHERE  = %s" % user_id, value)
