import json
import tkinter.ttk

import requests

import pw_tool.helper.fb_helper
import pw_tool.helper.ui_helper


class RegPage:
    def __init__(self, master):
        """Initialises registration page
        """
        self.__master = master
        self.__window = tkinter.Toplevel()
        self.__window.geometry(newGeometry="720x480")
        self.__window.title(string="Registration Page")

        self.__title_label = tkinter.ttk.Label(master=self.__window, text="Registration",
                                               font=pw_tool.helper.ui_helper.font,
                                               background=pw_tool.helper.ui_helper.background_color)

        self.__entry_frame = tkinter.ttk.Frame(master=self.__window, style="TFrame")

        self.__email_label = tkinter.ttk.Label(master=self.__entry_frame, text="Email",
                                               font=pw_tool.helper.ui_helper.font,
                                               background=pw_tool.helper.ui_helper.background_color)

        self.__email_entry = tkinter.ttk.Entry(master=self.__entry_frame, font=pw_tool.helper.ui_helper.font)

        self.__pw_label = tkinter.ttk.Label(master=self.__entry_frame, text="Password",
                                            font=pw_tool.helper.ui_helper.font,
                                            background=pw_tool.helper.ui_helper.background_color)

        self.__pw_entry = tkinter.ttk.Entry(master=self.__entry_frame, show="*", font=pw_tool.helper.ui_helper.font)

        self.__confirm_pw_label = tkinter.ttk.Label(master=self.__entry_frame, text="Confirm Password",
                                                    font=pw_tool.helper.ui_helper.font,
                                                    background=pw_tool.helper.ui_helper.background_color)

        self.__confirm_pw_entry = tkinter.ttk.Entry(master=self.__entry_frame, show="*",
                                                    font=pw_tool.helper.ui_helper.font)

        self.__create_account_button = tkinter.ttk.Button(master=self.__window, text="Create Account",
                                                          style="LargeFont.TButton", command=self.__create_account)

        self.__notification_label = tkinter.ttk.Label(master=self.__window, font=pw_tool.helper.ui_helper.font,
                                                      background=pw_tool.helper.ui_helper.background_color)

        self.__email_entry.focus()

        self.__email_label.grid(row=0, column=0, padx=20, pady=5, sticky="E")
        self.__email_entry.grid(row=0, column=1, padx=20, pady=5, sticky="W")
        self.__pw_label.grid(row=1, column=0, padx=20, pady=5, sticky="E")
        self.__pw_entry.grid(row=1, column=1, padx=20, pady=5, sticky="W")
        self.__confirm_pw_label.grid(row=2, column=0, padx=20, pady=5, sticky="E")
        self.__confirm_pw_entry.grid(row=2, column=1, padx=20, pady=5, sticky="W")

        self.__title_label.pack(pady=20)
        self.__entry_frame.pack(pady=30)
        self.__create_account_button.pack(pady=5)
        self.__notification_label.pack(pady=5)

        pw_tool.helper.ui_helper.centre_window(window=self.__window)

        self.__window.protocol(func=lambda: pw_tool.helper.ui_helper.back(root=master, me=self.__window),
                               name="WM_DELETE_WINDOW")

    def __create_account(self):
        """Creates account
        If successful, redirects back to login page.
        """
        if not self.__email_entry.get() or not self.__pw_entry.get() or not self.__confirm_pw_entry.get():
            self.__notification_label.configure(text="Please ensure all fields are filled!")
            return

        if self.__pw_entry.get() != self.__confirm_pw_entry.get():
            self.__notification_label.configure(text="Passwords do not match!")
            return

        if len(self.__pw_entry.get()) < 12:
            self.__notification_label.configure(text="Please use at least 12 characters!")
            return

        try:
            pw_tool.helper.fb_helper.register(email=self.__email_entry.get(), password=self.__pw_entry.get())
        except requests.HTTPError as error:
            error_json = error.args[1]
            message = json.loads(s=error_json)["error"]["message"]
            formatted_message = message.replace("_", " ").replace(" : ", "\n").capitalize()
            self.__notification_label.configure(text=formatted_message)
            return

        pw_tool.helper.ui_helper.clear_fields(window=self.__entry_frame)

        self.__notification_label.configure(text="Successfully Created!")
        self.__window.after(ms=1000, func=lambda: pw_tool.helper.ui_helper.back(root=self.__master, me=self.__window))
