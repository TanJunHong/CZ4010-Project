from tkinter import ttk

import ttkthemes

import gui_helper
import password_helper
import registration_screen


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
                                       command=password_helper.verify_login)
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
