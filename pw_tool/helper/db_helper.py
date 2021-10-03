import sqlite3

with sqlite3.connect(database="password_vault.db") as db:
    cursor = db.cursor()
