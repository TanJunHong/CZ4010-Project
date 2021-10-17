import json
import tkinter
import tkinter.ttk

import requests

import pw_tool.helper.firebase_helper
import pw_tool.helper.ui_helper
import pw_tool.helper.vault_helper


class RegistrationPage:
    def __init__(self, master):
        self.__master = master
        self.__window = tkinter.Toplevel()
        self.__window.geometry(newGeometry="640x480")
        self.__window.title(string="Registration Page")

        self.__email_label = tkinter.ttk.Label(master=self.__window, text="Email", font=("Arial", 25),
                                               background=pw_tool.helper.ui_helper.background_color)
        self.__email_label.pack()

        self.__email_entry = tkinter.ttk.Entry(master=self.__window, font=("Arial", 25))
        self.__email_entry.pack()
        self.__email_entry.focus()

        self.__password_label = tkinter.ttk.Label(master=self.__window, text="Enter Password", font=("Arial", 25),
                                                  background=pw_tool.helper.ui_helper.background_color)
        self.__password_label.pack()

        self.__password_entry = tkinter.ttk.Entry(master=self.__window, show="*", font=("Arial", 25))
        self.__password_entry.pack()

        self.confirm_password_label = tkinter.ttk.Label(master=self.__window, text="Confirm password",
                                                        font=("Arial", 25),
                                                        background=pw_tool.helper.ui_helper.background_color)
        self.confirm_password_label.pack()

        self.confirm_password_entry = tkinter.ttk.Entry(master=self.__window, show="*", font=("Arial", 25))
        self.confirm_password_entry.pack()

        self.__notification_label = tkinter.ttk.Label(master=self.__window, font=("Arial", 25),
                                                      background=pw_tool.helper.ui_helper.background_color)
        self.__notification_label.pack()

        self.create_account_button = tkinter.ttk.Button(master=self.__window, text="Create Account", style="TButton",
                                                        command=self.__create_account)
        self.create_account_button.pack()

        pw_tool.helper.ui_helper.centre_window(window=self.__window)

        self.__window.protocol(func=lambda: pw_tool.helper.ui_helper.back(root=master, me=self.__window),
                               name="WM_DELETE_WINDOW")

    def __create_account(self):
        if not self.__email_entry.get() or not self.__password_entry.get() or not self.confirm_password_entry.get():
            self.__notification_label.config(text="Please ensure all fields are filled!")
            return

        if self.__password_entry.get() != self.confirm_password_entry.get():
            self.__notification_label.config(text="Passwords do not match!")
            return

        try:
            pw_tool.helper.firebase_helper.register(email=self.__email_entry.get(),
                                                    password=self.__password_entry.get())
        except requests.HTTPError as error:
            error_json = error.args[1]
            message = json.loads(error_json)["error"]["message"]
            formatted_message = message.replace("_", " ").replace(" : ", "\n").capitalize()
            self.__notification_label.config(text=formatted_message)
            return

        pw_tool.helper.ui_helper.clear_fields(window=self.__window)

        self.__notification_label.config(text="Successfully Created!")
        self.__window.after(ms=1000, func=lambda: pw_tool.helper.ui_helper.back(root=self.__master, me=self.__window))
