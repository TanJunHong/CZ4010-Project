import sqlite3
import tkinter
from tkinter import ttk
from functools import partial

# import the Fernet class
import cryptography.fernet
import passlib.context
import passlib.hash
from ttkthemes import ThemedTk

import gui_helper

with sqlite3.connect("password_vault.db") as db:
    cursor = db.cursor()

site_wide_salt = bytes("CZ4010", "utf8")

# cursor.execute("""
# DROP TABLE user_accounts;
# """)

username_hash = ""

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

context = passlib.context.CryptContext(
    schemes=["pbkdf2_sha256"],
    default="pbkdf2_sha256",
    pbkdf2_sha256__default_rounds=50000
)



def clear_fields(window):
    for widget in window.winfo_children():
        if type(widget) == ttk.Entry:
            widget.delete(0, tkinter.END)


def registration():
    def create_account():
        if not username_entry.get() or not password_entry.get() or not confirm_password_entry.get():
            another_label.config(text="Please ensure all fields are filled!")
            return
        cursor.execute("SELECT 1 FROM user_accounts WHERE username = ? LIMIT 1", [username_entry.get()])
        if len(cursor.fetchall()) > 0:
            another_label.config(text="Username already exists!")
            return
        if password_entry.get() != confirm_password_entry.get():
            another_label.config(text="Passwords do not match!")
            return

        username_hash = passlib.hash.pbkdf2_sha256.hash(username_entry.get(), salt=site_wide_salt).split("$")[-1]
        password_hash = context.hash(password_entry.get())
        insert_password = """INSERT INTO user_accounts (username, password) VALUES (?, ?) """
        cursor.execute(insert_password, [username_hash, password_hash])
        db.commit()
        another_label.config(text="Successfully Created!")
        new_window.destroy()
        curr_window.deiconify()

    clear_fields(curr_window)

    curr_window.withdraw()
    new_window = tkinter.Toplevel()
    new_window.geometry("640x480")
    new_window.title(string="Registration Page")
    username_label = ttk.Label(new_window, text="Username", font=("Arial", 25))
    # password_label.config(anchor=tkinter.CENTER)
    username_label.pack()

    username_entry = ttk.Entry(new_window, font=("Arial", 25))
    username_entry.pack()
    username_entry.focus()

    password_label = ttk.Label(new_window, text="Enter Password", font=("Arial", 25))
    # password_label.config(anchor=tkinter.CENTER)
    password_label.pack()

    password_entry = ttk.Entry(new_window, show="*", font=("Arial", 25))
    password_entry.pack()
    password_entry.focus()

    confirm_password_label = ttk.Label(new_window, text="Confirm password", font=("Arial", 25))
    # confirm password_label.config(anchor=tkinter.CENTER)
    confirm_password_label.pack()

    confirm_password_entry = ttk.Entry(new_window, show="*", font=("Arial", 25))
    confirm_password_entry.pack()
    confirm_password_entry.focus()

    another_label = ttk.Label(new_window, font=("Arial", 25))
    another_label.config(anchor=tkinter.CENTER)
    another_label.pack()

    style = ttk.Style(new_window)
    style.configure("TButton", font=("Arial", 25))
    create_account_button = ttk.Button(new_window, text="Create Account", style="TButton",
                                       command=create_account)
    create_account_button.pack()

    gui_helper.centre_window(new_window)

    new_window.protocol(
        func=lambda root=curr_window, window=new_window: gui_helper.back(root=curr_window, me=new_window),
        name="WM_DELETE_WINDOW")


def login_screen():
    main_window = ThemedTk(theme="arc")
    # ttk.Button(main_window, text="Quit", ).pack()
    # main_window.mainloop()

    # main_window = tkinter.Tk()
    main_window.geometry("640x480")
    main_window.title(string="Password Manager")

    username_label = ttk.Label(main_window, text="Username", font=("Arial", 25))
    # password_label.config(anchor=tkinter.CENTER)
    username_label.pack()

    username_entry = ttk.Entry(main_window, font=("Arial", 25))
    username_entry.pack()
    username_entry.focus()

    password_label = ttk.Label(main_window, text="Enter Master Password", font=("Arial", 25))
    # password_label.config(anchor=tkinter.CENTER)
    password_label.pack()

    password_entry = ttk.Entry(main_window, show="*", font=("Arial", 25))
    password_entry.pack()
    password_entry.focus()

    another_label = ttk.Label(main_window, font=("Arial", 25))
    another_label.config(anchor=tkinter.CENTER)
    another_label.pack()

    def verify_login():
        username_hash = passlib.hash.pbkdf2_sha256.hash(username_entry.get(), salt=site_wide_salt).split("$")[-1]
        cursor.execute("SELECT password FROM user_accounts WHERE username = ?", [username_hash])
        password_hash = cursor.fetchone()
        if not username_entry.get() or not password_entry.get():
            another_label.config(text="Please ensure all fields are filled!")
            return
        if not password_hash or not context.verify(password_entry.get(), password_hash[0]):
            another_label.config(text="Wrong Username or Password!")
            return
        another_label.config(text="Login Successful! Redirecting you...")
        curr_window.after(1000, lambda: another_label.config(text=""))
        curr_window.after(1000, password_vault)

    style = ttk.Style(main_window)
    style.configure("TButton", font=("Arial", 25))

    login_button = ttk.Button(main_window, text="Login", style="TButton", command=verify_login)
    login_button.pack()

    register_button = ttk.Button(main_window, text="Register", style="TButton", command=registration)
    register_button.pack()

    return main_window


curr_window = login_screen()


def password_vault():
    def get_data():
        cursor.execute("SELECT * FROM password_vault WHERE username = ?", [username_hash])
        result = cursor.fetchall()

    def add_page():
        def add_to_vault():
            # username_hash = passlib.hash.pbkdf2_sha256.hash(username_entry.get(), salt=site_wide_salt).split("$")[-1]
            # generate key
            key = cryptography.fernet.Fernet.generate_key()
            f = cryptography.fernet.Fernet(key)
            encrypted_password = f.encrypt(bytes(password_entry.get(), "utf8"))
            insert_query = """INSERT INTO password_vault (username, website, login_username, password) VALUES (?, ?, ?, ?) """
            cursor.execute(insert_query, [username_hash, website_entry.get(), username_entry.get(), encrypted_password])
            db.commit()

        new_window = tkinter.Toplevel()
        new_window.geometry("640x480")
        new_window.title(string="Add Item")
        website_label = ttk.Label(new_window, text="Website", font=("Arial", 25))
        website_label.pack()

        website_entry = ttk.Entry(new_window, font=("Arial", 25))
        website_entry.pack()
        website_entry.focus()

        username_label = ttk.Label(new_window, text="Login Username", font=("Arial", 25))
        username_label.pack()

        username_entry = ttk.Entry(new_window, font=("Arial", 25))
        username_entry.pack()
        username_entry.focus()

        password_label = ttk.Label(new_window, text="Password", font=("Arial", 25))
        password_label.pack()

        password_entry = ttk.Entry(new_window, show="*", font=("Arial", 25))
        password_entry.pack()
        password_entry.focus()

        notification_label = ttk.Label(new_window, font=("Arial", 25))
        notification_label.config(anchor=tkinter.CENTER)
        notification_label.pack()

        add_button = ttk.Button(new_window, text="Add To Vault", style="TButton", command=add_to_vault)
        add_button.pack()

        gui_helper.centre_window(new_window)

    def delete_page():
        def delete_from_vault():
            cursor.execute("DELETE FROM password_vault WHERE id =?", (input,))
            db.commit()

        new_window = tkinter.Toplevel()
        new_window.geometry("640x480")
        new_window.title(string="Delete Item")

        website_lbl = ttk.Label(new_window, text="Website")
        website_lbl.grid(row=2, column=0, padx=80)

        username_lbl = ttk.Label(new_window, text="Username")
        username_lbl.grid(row=2, column=1, padx=80)

        password_lbl = ttk.Label(new_window, text="Password")
        password_lbl.grid(row=2, column=2, padx=80)

        cursor.execute('SELECT website, username, password FROM password_vault')
        if (cursor.fetchall() != None):
            i = 0
            while True:
                cursor.execute('SELECT website, username,password FROM password_vault')
                array = cursor.fetchall()
                website_lbl1 = ttk.Label(new_window, text=(array[i][0]), font=("Arial", 12))
                website_lbl1.grid(column=0, row=(i + 3))

                username_lbl2 = ttk.Label(new_window, text=(array[i][1]), font=("Arial", 12))
                username_lbl2.grid(column=1, row=(i + 3))

                password_lbl3 = ttk.Label(new_window, text=(array[i][2]), font=("Arial", 12))
                password_lbl3.grid(column=2, row=(i + 3))

                delete_btn = ttk.Button(new_window, text="Delete", command=partial(delete_from_vault, array[i][0]))
                delete_btn.grid(column=3, row=(i + 3), pady=10)

                i = i + 1
                cursor.execute('SELECT website, username, password FROM password_vault')
                if (len(cursor.fetchall()) <= i):
                    break

        gui_helper.centre_window(new_window)

    clear_fields(curr_window)

    curr_window.withdraw()
    # curr_window.destroy()
    new_window = tkinter.Toplevel()
    new_window.geometry("640x480")
    new_window.title(string="Password Manager")
    welcome_label = ttk.Label(new_window, text="Password Vault")
    welcome_label.config(anchor=tkinter.CENTER)
    welcome_label.pack()

    style = ttk.Style(new_window)
    style.configure("TButton", font=("Arial", 25))

    add_button = ttk.Button(new_window, text="Add Vault", style="TButton", command=add_page)
    add_button.pack()

    delete_button = ttk.Button(new_window, text="Delete Vault", style="TButton", command=delete_page)
    delete_button.pack()
    gui_helper.centre_window(new_window)
    # new_window.mainloop()

    new_window.protocol(
        func=lambda root=curr_window, window=new_window: gui_helper.back(root=curr_window, me=new_window),
        name="WM_DELETE_WINDOW")


if __name__ == "__main__":
    gui_helper.centre_window(curr_window)
    curr_window.mainloop()
