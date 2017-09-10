from tinymongo import TinyMongoClient
connection = TinyMongoClient('/tmp/game')

db = connection.pingpong

