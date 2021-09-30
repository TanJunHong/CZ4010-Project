import sqlite3
import tkinter

import passlib.context
import passlib.hash

with sqlite3.connect("password_vault.db") as db:
    cursor = db.cursor()

site_wide_salt = bytes("CZ4010", "utf8")

# cursor.execute("""
# DROP TABLE user_accounts;
# """)

cursor.execute("""
CREATE TABLE IF NOT EXISTS user_accounts(
    id INTEGER PRIMARY KEY,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL
);
""")

context = passlib.context.CryptContext(
    schemes=["pbkdf2_sha256"],
    default="pbkdf2_sha256",
    pbkdf2_sha256__default_rounds=50000
)


def centre_window(window):
    """Centres main window given 'window'
    Function centre_window(window) centres the given 'window' by taking into account main window geometry and screen
    geometry. winfo_screenwidth(), winfo_screenheight(), winfo_width(), winfo_height() are used. The main window is
    hidden using withdraw() then displayed again using deiconify().
    """

    # Hide window
    window.withdraw()

    # Update
    window.update_idletasks()

    # Calculations to centre the window
    x = (window.winfo_screenwidth() - max(window.winfo_width(), window.winfo_reqwidth())) / 2
    y = (window.winfo_screenheight() - max(window.winfo_height(), window.winfo_reqheight())) / 2
    window.geometry(newGeometry='+%d+%d' % (x, y))

    # Show window
    window.deiconify()


def clear_fields(window):
    for widget in window.winfo_children():
        if type(widget) == tkinter.Entry:
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
    username_label = tkinter.Label(new_window, text="Username", font=("Arial", 25))
    # password_label.config(anchor=tkinter.CENTER)
    username_label.pack()

    username_entry = tkinter.Entry(new_window, font=("Arial", 25))
    username_entry.pack()
    username_entry.focus()

    password_label = tkinter.Label(new_window, text="Enter Password", font=("Arial", 25))
    # password_label.config(anchor=tkinter.CENTER)
    password_label.pack()

    password_entry = tkinter.Entry(new_window, show="*", font=("Arial", 25))
    password_entry.pack()
    password_entry.focus()

    confirm_password_label = tkinter.Label(new_window, text="Confirm password", font=("Arial", 25))
    # confirm password_label.config(anchor=tkinter.CENTER)
    confirm_password_label.pack()

    confirm_password_entry = tkinter.Entry(new_window, show="*", font=("Arial", 25))
    confirm_password_entry.pack()
    confirm_password_entry.focus()

    another_label = tkinter.Label(new_window, font=("Arial", 25))
    another_label.config(anchor=tkinter.CENTER)
    another_label.pack()

    create_account_button = tkinter.Button(new_window, text="Create Account", font=("Arial", 25),
                                           command=create_account)
    create_account_button.pack()

    centre_window(new_window)

    new_window.protocol(func=lambda root=curr_window, window=new_window: back(root=curr_window, me=new_window),
                        name="WM_DELETE_WINDOW")


def login_screen():
    main_window = tkinter.Tk()
    main_window.geometry("640x480")
    main_window.title(string="Password Manager")

    username_label = tkinter.Label(main_window, text="Username", font=("Arial", 25))
    # password_label.config(anchor=tkinter.CENTER)
    username_label.pack()

    username_entry = tkinter.Entry(main_window, font=("Arial", 25))
    username_entry.pack()
    username_entry.focus()

    password_label = tkinter.Label(main_window, text="Enter Master Password", font=("Arial", 25))
    # password_label.config(anchor=tkinter.CENTER)
    password_label.pack()

    password_entry = tkinter.Entry(main_window, show="*", font=("Arial", 25))
    password_entry.pack()
    password_entry.focus()

    another_label = tkinter.Label(main_window, font=("Arial", 25))
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
        # another_label.config(text="Login Successful! Redirecting you...")
        curr_window.after(1000, password_vault)

    submit_button = tkinter.Button(main_window, text="Submit", font=("Arial", 25), command=verify_login)
    submit_button.pack()

    register_button = tkinter.Button(main_window, text="Register", font=("Arial", 25), command=registration)
    register_button.pack()

    return main_window


curr_window = login_screen()


def password_vault():
    clear_fields(curr_window)

    curr_window.withdraw()
    # curr_window.destroy()
    new_window = tkinter.Toplevel()
    new_window.geometry("640x480")
    new_window.title(string="Password Manager")
    welcome_label = tkinter.Label(new_window, text="Password Vault")
    welcome_label.config(anchor=tkinter.CENTER)
    welcome_label.pack()
    centre_window(new_window)
    # new_window.mainloop()

    new_window.protocol(func=lambda root=curr_window, window=new_window: back(root=curr_window, me=new_window),
                        name="WM_DELETE_WINDOW")


def back(root, me):
    """Goes Back to main page, given 'root' and 'me'.
    Function back(root,me) takes in 'root' and 'me', destroys 'me' and shows 'root'
    """

    me.destroy()
    root.deiconify()


if __name__ == "__main__":
    centre_window(curr_window)
    curr_window.mainloop()
