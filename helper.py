import sqlite3

from passlib import context

with sqlite3.connect("password_vault.db") as db:
    cursor = db.cursor()

site_wide_salt = bytes("CZ4010", "utf8")

context = context.CryptContext(
    schemes=["pbkdf2_sha256"],
    default="pbkdf2_sha256",
    pbkdf2_sha256__default_rounds=50000
)
