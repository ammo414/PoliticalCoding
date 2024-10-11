"""test"""

from utils.db_utils import PostGreManager as pgm
from utils.constants import db_config as dbc

db = pgm(dbc)

QUERY = "CREATE TABLE {} (test text PRIMARY KEY)"

db.connect()
db.execute_query(QUERY, 'testing', parameters=[])
