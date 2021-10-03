from passwordmanager.helper.db_helper import cursor
from passwordmanager.ui import login_page

if __name__ == "__main__":
    # cursor.execute("""
    # DROP TABLE user_accounts;
    # """)
    # cursor.execute("""
    # DROP TABLE password_vault;
    # """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS user_accounts(
        id INTEGER PRIMARY KEY,
        username TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS password_vault(
        id INTEGER PRIMARY KEY,
        username TEXT NOT NULL,
        website TEXT NOT NULL,
        login_username TEXT NOT NULL,
        password TEXT NOT NULL
    );
    """)

    login_page.LoginPage()
