import json
import tkinter.ttk

import requests

import pw_tool.helper.fb_helper
import pw_tool.helper.ui_helper


class ChangePWPage:
    def __init__(self, master):
        self.__master = master
        self.__master.withdraw()

        self.__window = tkinter.Toplevel()
        self.__window.geometry(newGeometry="720x640")
        self.__window.title(string="Password Manager")

        self.__welcome_label = tkinter.ttk.Label(master=self.__window, text="Change Password",
                                                 font=pw_tool.helper.ui_helper.font,
                                                 background=pw_tool.helper.ui_helper.background_color)

        self.__entry_frame = tkinter.ttk.Frame(master=self.__window, style="TFrame")

        self.__old_pw_label = tkinter.ttk.Label(master=self.__entry_frame, text="Old Password:",
                                                font=pw_tool.helper.ui_helper.font,
                                                background=pw_tool.helper.ui_helper.background_color)

        self.__old_pw_entry = tkinter.ttk.Entry(master=self.__entry_frame, font=pw_tool.helper.ui_helper.font, show="*")

        self.__new_pw_label = tkinter.ttk.Label(master=self.__entry_frame, text="New Password:",
                                                font=pw_tool.helper.ui_helper.font,
                                                background=pw_tool.helper.ui_helper.background_color)

        self.__new_pw_entry = tkinter.ttk.Entry(master=self.__entry_frame, font=pw_tool.helper.ui_helper.font,
                                                show="*")

        self.__confirm_pw_label = tkinter.ttk.Label(master=self.__entry_frame, text="Confirm Password:",
                                                    font=pw_tool.helper.ui_helper.font,
                                                    background=pw_tool.helper.ui_helper.background_color)

        self.__confirm_pw_entry = tkinter.ttk.Entry(master=self.__entry_frame, font=pw_tool.helper.ui_helper.font,
                                                    show="*")

        self.__update_button = tkinter.ttk.Button(master=self.__window, text="Update", style="TButton",
                                                  command=self.__change_password)

        self.__notification_label = tkinter.ttk.Label(master=self.__window, font=pw_tool.helper.ui_helper.font,
                                                      background=pw_tool.helper.ui_helper.background_color)

        self.__old_pw_entry.focus()

        self.__old_pw_label.grid(row=0, column=0, padx=20, pady=5, sticky="W")
        self.__old_pw_entry.grid(row=0, column=1, padx=20, pady=5, sticky="E")
        self.__new_pw_label.grid(row=1, column=0, padx=20, pady=5, sticky="W")
        self.__new_pw_entry.grid(row=1, column=1, padx=20, pady=5, sticky="E")
        self.__confirm_pw_label.grid(row=2, column=0, padx=20, pady=5, sticky="W")
        self.__confirm_pw_entry.grid(row=2, column=1, padx=20, pady=5, sticky="E")

        self.__welcome_label.pack(pady=50)
        self.__entry_frame.pack(pady=5)
        self.__update_button.pack(pady=50)
        self.__notification_label.pack(pady=5)

        self.__window.protocol(func=lambda: pw_tool.helper.ui_helper.back(root=self.__master, me=self.__window),
                               name="WM_DELETE_WINDOW")

        pw_tool.helper.ui_helper.centre_window(window=self.__window)

    def __change_password(self):
        if not self.__old_pw_entry.get() or not self.__new_pw_entry.get() or not self.__confirm_pw_entry.get():
            self.__notification_label.config(text="Please ensure all fields are filled!")
            return

        if not pw_tool.helper.fb_helper.validate_old_password(old_password=self.__old_pw_entry.get()):
            self.__notification_label.config(text="Incorrect password!")
            return

        if self.__new_pw_entry.get() != self.__confirm_pw_entry.get():
            self.__notification_label.config(text="Passwords don't match!")
            return

        try:
            pw_tool.helper.fb_helper.change_password(password=self.__new_pw_entry.get())
        except requests.HTTPError as error:
            error_json = error.args[1]
            message = json.loads(s=error_json)["error"]["message"]
            formatted_message = message.replace("_", " ").replace(" : ",
                                                                  "\n").capitalize()
            self.__notification_label.config(text=formatted_message)
            return

        pw_tool.helper.ui_helper.clear_fields(window=self.__entry_frame)

        self.__notification_label.config(text="Successfully Updated!")
        self.__window.after(ms=1000, func=lambda: pw_tool.helper.ui_helper.back(root=self.__master, me=self.__window))
