from tkinter import ttk

import ttkthemes
from passlib import hash

import gui_helper
import helper
import password_helper
import registration_screen
from main import password_vault
from password_helper import context


class LoginScreen:
    def __init__(self):
        self.window = ttkthemes.ThemedTk(theme="arc")
        self.window.geometry(newGeometry="640x480")
        self.window.title(string="Password Manager")

        gui_helper.create_style()

        self.username_label = ttk.Label(master=self.window, text="Username", font=("Arial", 25),
                                        background="SystemButtonFace")
        self.username_label.pack()

        self.username_entry = ttk.Entry(master=self.window, font=("Arial", 25))
        self.username_entry.pack()
        self.username_entry.focus()

        self.password_label = ttk.Label(master=self.window, text="Enter Master Password", font=("Arial", 25),
                                        background="SystemButtonFace")
        self.password_label.pack()

        self.password_entry = ttk.Entry(master=self.window, show="*", font=("Arial", 25))
        self.password_entry.pack()
        self.password_entry.focus()

        self.notification_label = ttk.Label(master=self.window, font=("Arial", 25), background="SystemButtonFace")
        self.notification_label.pack()

        self.login_button = ttk.Button(master=self.window, text="Login", style="TButton",
                                       command=self.verify_login)
        self.login_button.pack()

        self.register_button = ttk.Button(master=self.window, text="Register", style="TButton",
                                          command=self.to_register_screen)
        self.register_button.pack()

        gui_helper.centre_window(window=self.window)
        self.window.mainloop()

    def to_register_screen(self):
        gui_helper.clear_fields(window=self.window)
        self.window.withdraw()
        registration_screen.RegistrationScreen(master=self.window)

    def verify_login(self):
        if not self.username_entry.get() or not self.password_entry.get():
            self.notification_label.config(text="Please ensure all fields are filled!")
            return

        username_hash = \
        hash.pbkdf2_sha256.hash(secret=self.username_entry.get(), salt=password_helper.site_wide_salt).split("$")[-1]

        helper.cursor.execute("SELECT password FROM user_accounts WHERE username = ?", [username_hash])
        password_hash = helper.cursor.fetchone()

        if not password_hash or not context.verify(self.password_entry.get(), password_hash[0]):
            self.notification_label.config(text="Wrong Username or Password!")
            return

        gui_helper.clear_fields(self.window)

        self.notification_label.config(text="Login Successful! Redirecting you...")
        self.window.after(1000, lambda: self.notification_label.config(text=""))
        self.window.after(1000, self.window.withdraw)
        self.window.after(1000, password_vault)
