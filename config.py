import psycopg2
# token = ('612505438:AAHelG_wqIDR8Lop_Vdc9MXOLiODN1IosZU')
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


class StatisticsStatus(enumerate):
    S_EXERSIZE = 0,
    S_STATISTICS = 1


class TrainingStates(enumerate):
    S_ENTER_DATE = 0,
    S_READY = 1
