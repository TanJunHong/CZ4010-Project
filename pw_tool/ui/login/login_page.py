import json
import tkinter.ttk

import requests
import ttkthemes

import pw_tool.helper.fb_helper
import pw_tool.helper.ui_helper
import pw_tool.ui.reg.reg_page
import pw_tool.ui.vault.vault_page


class LoginPage:
    def __init__(self):
        self.__window = ttkthemes.ThemedTk(theme="arc")
        self.__window.geometry(newGeometry=pw_tool.helper.ui_helper.window_size)
        self.__window.title(string="Password Manager")

        pw_tool.helper.ui_helper.create_button_style()
        pw_tool.helper.ui_helper.create_frame_style()

        self.__title_label = tkinter.ttk.Label(master=self.__window, text="Password Tool",
                                               font=pw_tool.helper.ui_helper.font,
                                               background=pw_tool.helper.ui_helper.background_color)

        self.__entry_frame = tkinter.ttk.Frame(master=self.__window, style="TFrame")

        self.__email_label = tkinter.ttk.Label(master=self.__entry_frame, text="Email",
                                               font=pw_tool.helper.ui_helper.font,
                                               background=pw_tool.helper.ui_helper.background_color)

        self.__email_entry = tkinter.ttk.Entry(master=self.__entry_frame, font=pw_tool.helper.ui_helper.font)

        self.__password_label = tkinter.ttk.Label(master=self.__entry_frame, text="Password",
                                                  font=pw_tool.helper.ui_helper.font,
                                                  background=pw_tool.helper.ui_helper.background_color)

        self.__password_entry = tkinter.ttk.Entry(master=self.__entry_frame, show="*",
                                                  font=pw_tool.helper.ui_helper.font)

        self.__button_frame = tkinter.ttk.Frame(master=self.__window, style="TFrame")

        self.__login_button = tkinter.ttk.Button(master=self.__button_frame, text="Login", style="TButton",
                                                 command=self.__verify_login)

        self.__register_button = tkinter.ttk.Button(master=self.__button_frame, text="Register", style="TButton",
                                                    command=self.__show_register_page)

        self.__notification_label = tkinter.ttk.Label(master=self.__window, font=pw_tool.helper.ui_helper.font,
                                                      background=pw_tool.helper.ui_helper.background_color)

        self.__email_entry.focus()

        self.__email_label.grid(row=0, column=0, padx=20, pady=5, sticky="E")
        self.__email_entry.grid(row=0, column=1, padx=20, pady=5, sticky="W")
        self.__password_label.grid(row=1, column=0, padx=20, pady=5, sticky="E")
        self.__password_entry.grid(row=1, column=1, padx=20, pady=5, sticky="W")

        self.__login_button.grid(row=0, column=0, padx=20, pady=5, sticky="E")
        self.__register_button.grid(row=0, column=1, padx=20, pady=5, sticky="W")

        self.__title_label.pack(pady=20)
        self.__entry_frame.pack(pady=30)
        self.__button_frame.pack(pady=10)
        self.__notification_label.pack(pady=50)

        pw_tool.helper.ui_helper.centre_window(window=self.__window)
        self.__window.mainloop()

    def __show_register_page(self):
        pw_tool.helper.ui_helper.clear_fields(window=self.__entry_frame)
        self.__window.withdraw()
        pw_tool.ui.reg.reg_page.RegPage(master=self.__window)

    def __verify_login(self):
        if not self.__email_entry.get() or not self.__password_entry.get():
            self.__notification_label.config(text="Please ensure all fields are filled!")
            return

        try:
            pw_tool.helper.fb_helper.login(email=self.__email_entry.get(), password=self.__password_entry.get())
        except requests.HTTPError as error:
            error_json = error.args[1]
            message = json.loads(error_json)["error"]["message"]
            formatted_message = message.replace("_", " ").replace(" : ",
                                                                  "\n").capitalize()
            self.__notification_label.config(text=formatted_message)
            return

        pw_tool.helper.ui_helper.clear_fields(window=self.__entry_frame)

        self.__notification_label.config(text="Login Successful! Redirecting you...")
        self.__window.after(ms=1000, func=lambda: self.__notification_label.config(text=""))
        self.__window.after(ms=1000, func=self.__create_vault_page)

    def __create_vault_page(self):
        pw_tool.helper.ui_helper.vault_page = pw_tool.ui.vault.vault_page.VaultPage(master=self.__window)
