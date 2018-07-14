import psycopg2
token = ('554026510:AAHQahqhMAwffu4qWQSa0JZPJjDLamDtXO4')
params = {
  'database': 'dftilqnoe4t5kg',
  'user': 'jkcvzflxvnhqcq',
  'password': '80af35cf40ad6392d412671a379797fe9891cce47e525b87863aaa9728f0f784',
  'host': 'ec2-54-227-243-210.compute-1.amazonaws.com',
  'port': 5432
}
db = psycopg2.connect(**params)
cur = db.cursor()


class ExersizeStates(enumerate):
    S_EXERSIZE = 0,
    S_GOT = 1,
    S_GOT_WEIGHT = 2,
    S_GOT_REPS = 3,
