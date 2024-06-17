import sqlite3

conn = sqlite3.connect("database.sqlite", check_same_thread = False)

cursor = conn.cursor()