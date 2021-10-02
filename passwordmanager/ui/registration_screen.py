import tkinter
from tkinter import ttk

from passlib import hash

from passwordmanager.helper import db_helper, gui_helper, password_helper


class RegistrationScreen:
    def __init__(self, master):
        self.master = master
        self.window = tkinter.Toplevel()
        self.window.geometry(newGeometry="640x480")
        self.window.title(string="Registration Page")

        self.username_label = ttk.Label(master=self.window, text="Username", font=("Arial", 25),
                                        background="SystemButtonFace")
        self.username_label.pack()

        self.username_entry = ttk.Entry(master=self.window, font=("Arial", 25))
        self.username_entry.pack()
        self.username_entry.focus()

        self.password_label = ttk.Label(master=self.window, text="Enter Password", font=("Arial", 25),
                                        background="SystemButtonFace")
        self.password_label.pack()

        self.password_entry = ttk.Entry(master=self.window, show="*", font=("Arial", 25))
        self.password_entry.pack()
        self.password_entry.focus()

        self.confirm_password_label = ttk.Label(master=self.window, text="Confirm password", font=("Arial", 25),
                                                background="SystemButtonFace")
        self.confirm_password_label.pack()

        self.confirm_password_entry = ttk.Entry(master=self.window, show="*", font=("Arial", 25))
        self.confirm_password_entry.pack()
        self.confirm_password_entry.focus()

        self.notification_label = ttk.Label(master=self.window, font=("Arial", 25), background="SystemButtonFace")
        self.notification_label.config(anchor=tkinter.CENTER)
        self.notification_label.pack()

        self.create_account_button = ttk.Button(master=self.window, text="Create Account", style="TButton",
                                                command=self.create_account)
        self.create_account_button.pack()

        gui_helper.centre_window(window=self.window)

        self.window.protocol(func=lambda root=master, window=self.window: gui_helper.back(root=master, me=self.window),
                             name="WM_DELETE_WINDOW")
        self.window.mainloop()

    def create_account(self):
        if not self.username_entry.get() or not self.password_entry.get() or not self.confirm_password_entry.get():
            self.notification_label.config(text="Please ensure all fields are filled!")
            return

        username_hash = \
            hash.pbkdf2_sha256.hash(secret=self.username_entry.get(), salt=password_helper.site_wide_salt).split("$")[
                -1]

        db_helper.cursor.execute("SELECT 1 FROM user_accounts WHERE username = ? LIMIT 1", [username_hash])
        if len(db_helper.cursor.fetchall()) > 0:
            self.notification_label.config(text="Username already exists!")
            return
        if self.password_entry.get() != self.confirm_password_entry.get():
            self.notification_label.config(text="Passwords do not match!")
            return

        password_hash = password_helper.context.hash(self.password_entry.get())

        gui_helper.clear_fields(self.window)

        db_helper.cursor.execute("""INSERT INTO user_accounts (username, password) VALUES (?, ?) """,
                                 [username_hash, password_hash])
        db_helper.db.commit()

        self.notification_label.config(text="Successfully Created!")
        self.window.after(1000, lambda: gui_helper.back(root=self.master, me=self.window))
