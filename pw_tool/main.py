from pw_tool.helper.db_helper import cursor
from pw_tool.ui.login import login_page


def main():
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


if __name__ == "__main__":
    main()
