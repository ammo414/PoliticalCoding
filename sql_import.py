import psycopg2
from sqlalchemy import create_engine

import constants


## sql connection is still in progress
db_params = {
    'host': constants.HOST,
    'database': 'postgres',
    'user': constants.USER,
    'password': constants.PASSWORD
}

conn = psycopg2.connect(
    host = db_params['host'],
    database = 'postgres',
    user = db_params['user'],
    password = db_params['password']
)


cur = conn.cursor()

conn.set_session(autocommit=True)

cur.execute('create DATABASE political_coding')

conn.commit()
cur.close()
conn.close()

engine = create_engine(constants.DATABASE_URL)