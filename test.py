from tinymongo import TinyMongoClient
from flask import session, jsonify
from functools import wraps
from game.helpers import csv_to_json
from config import *

# /tmp is accessible in lambda
connection = TinyMongoClient(DB_PATH)
db = connection[DBNAME]
users_collection = db.users
matches_collection = db.matches

db_all_users = list(db.users.find({}))
users_available = csv_to_json(DATA_FILE)

print('\n'*10)
for u in db_all_users:
    print(u)
