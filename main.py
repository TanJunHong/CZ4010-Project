import tkinter
from functools import partial
from tkinter import ttk

# import the Fernet class
import cryptography.fernet

import gui_helper
import login_screen
# cursor.execute("""
# DROP TABLE user_accounts;
# """)
# cursor.execute("""
# DROP TABLE password_vault;
# """)
from helper import cursor, db

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

instance = None

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

    def pgenerator_page():
        def pgenerator():
            print("bIJ")
        new_window = tkinter.Toplevel()
        new_window.geometry("640x480")
        new_window.title(string="Password Generator")

        # Get length of password to generate
        plength_label = ttk.Label(new_window, text="Length of password:", font=("Arial", 12))
        plength_label.grid(row=0, column=0, padx=10)

        plength_entry = ttk.Entry(new_window, font=("Arial", 12))
        plength_entry.grid(row=0, column=1)

        # Get type of characters to include in password
        ptype_label = ttk.Label(new_window, text="Type of characters:", font=("Arial",12))
        ptype_label.grid(row=1, column=0, padx=10)

        ptype1_cbox = ttk.Checkbutton(new_window, text="Upper Case A-Z")
        ptype1_cbox.grid(row=1, column=1)

        ptype2_cbox = ttk.Checkbutton(new_window, text="Lower Case a-z")
        ptype2_cbox.grid(row=1, column=2)

        ptype3_cbox = ttk.Checkbutton(new_window, text="Numeric 0-9")
        ptype3_cbox.grid(row=2, column=1)

        ptype4_cbox = ttk.Checkbutton(new_window, text="!@#$%^&*")
        ptype4_cbox.grid(row=2, column=2)

        # Generate password
        generate_button = ttk.Button(new_window, text="Generate", style="TButton", command=pgenerator)
        generate_button.grid(row=3, column=1)

        gui_helper.centre_window(new_window)

    # curr_window.withdraw()
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

    pgenerator_button = ttk.Button(new_window, text="Password Generator", style="TButton", command=pgenerator_page)
    pgenerator_button.pack()

    gui_helper.centre_window(new_window)
    # new_window.mainloop()

    new_window.protocol(
        func=lambda: gui_helper.back(root=instance, me=new_window),
        name="WM_DELETE_WINDOW")


if __name__ == "__main__":
    login_screen.LoginScreen()
