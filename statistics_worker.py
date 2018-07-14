import config


def get_current_state(message):
    config.cur.execute("SELECT * FROM users WHERE name = '%s'" % message.from_user.username)
    user_record = config.cur.fetchone()
    config.cur.execute("SELECT * FROM statistics_status WHERE user_id = %s" % user_record[0])
    statistics_record = config.cur.fetchone()
    return statistics_record[2]


def set_state(user_id, value):
    config.cur.execute("UPDATE statistics_status SET status = %s WHERE user_id = %s" % (value, user_id))
    config.db.commit()
