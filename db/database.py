from decouple import config
from orm import Database

db = Database(config("DB_NAME",  default="db.sqlite3"))
