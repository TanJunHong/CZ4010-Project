import sqlite3

with sqlite3.connect("password_vault.db") as db:
    cursor = db.cursor()
