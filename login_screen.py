import tkinter
from tkinter import ttk

import ttkthemes

import gui_helper
import password_helper


class LoginScreen:
    def __init__(self):
        self.window = ttkthemes.ThemedTk(theme="arc")
        self.window.geometry(newGeometry="640x480")
        self.window.title(string="Password Manager")

        gui_helper.create_style(window=self.window)

        username_label = ttk.Label(master=self.window, text="Username", font=("Arial", 25))
        username_label.pack()

        username_entry = ttk.Entry(master=self.window, font=("Arial", 25))
        username_entry.pack()
        username_entry.focus()

        password_label = ttk.Label(master=self.window, text="Enter Master Password", font=("Arial", 25))
        password_label.pack()

        password_entry = ttk.Entry(master=self.window, show="*", font=("Arial", 25))
        password_entry.pack()
        password_entry.focus()

        another_label = ttk.Label(master=self.window, font=("Arial", 25))
        another_label.config(anchor=tkinter.CENTER)
        another_label.pack()

        login_button = ttk.Button(master=self.window, text="Login", style="TButton",
                                  command=password_helper.verify_login)
        login_button.pack()

        register_button = ttk.Button(master=self.window, text="Register", style="TButton", command="registration")
        register_button.pack()

        gui_helper.centre_window(window=self.window)
        self.window.mainloop()
