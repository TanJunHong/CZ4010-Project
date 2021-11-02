import tkinter.ttk

import pw_tool.helper.ui_helper
import pw_tool.helper.vault_helper


class EditPage:
    def __init__(self, master, website, value):
        """Initialises edit page
        """
        self.__master = master
        self.__master.withdraw()

        self.__website = website
        self.__value = value

        self.__window = tkinter.Toplevel()
        self.__window.geometry(newGeometry=pw_tool.helper.ui_helper.window_size)
        self.__window.title(string="Password Manager")

        self.__website_label = tkinter.ttk.Label(master=self.__window, text=self.__website,
                                                 font=pw_tool.helper.ui_helper.font,
                                                 background=pw_tool.helper.ui_helper.background_color)

        self.__entry_frame = tkinter.ttk.Frame(master=self.__window, style="TFrame")

        self.__username_label = tkinter.ttk.Label(master=self.__entry_frame, text="Username:",
                                                  font=pw_tool.helper.ui_helper.font,
                                                  background=pw_tool.helper.ui_helper.background_color)

        self.__username_entry = tkinter.ttk.Entry(master=self.__entry_frame, font=pw_tool.helper.ui_helper.font)
        self.__username_entry.insert(index=0, string=self.__value["username"])

        self.__pw_label = tkinter.ttk.Label(master=self.__entry_frame, text="Password:",
                                            font=pw_tool.helper.ui_helper.font,
                                            background=pw_tool.helper.ui_helper.background_color)

        self.__pw_entry = tkinter.ttk.Entry(master=self.__entry_frame, font=pw_tool.helper.ui_helper.font, show="*")
        self.__pw_entry.insert(index=0, string=self.__value["password"])

        self.__edit_button = tkinter.ttk.Button(master=self.__window, text="Update", style="TButton",
                                                command=self.__update_vault)

        self.__notification_label = tkinter.ttk.Label(master=self.__window, font=pw_tool.helper.ui_helper.font,
                                                      background=pw_tool.helper.ui_helper.background_color)

        self.__username_entry.focus()

        self.__username_label.grid(row=0, column=0, padx=20, pady=5, sticky="W")
        self.__username_entry.grid(row=0, column=1, padx=20, pady=5, sticky="E")
        self.__pw_label.grid(row=1, column=0, padx=20, pady=5, sticky="W")
        self.__pw_entry.grid(row=1, column=1, padx=20, pady=5, sticky="E")

        self.__website_label.pack(pady=50)
        self.__entry_frame.pack(pady=5)
        self.__edit_button.pack(pady=50)
        self.__notification_label.pack(pady=5)

        self.__window.protocol(func=lambda: pw_tool.helper.ui_helper.back(root=self.__master, me=self.__window),
                               name="WM_DELETE_WINDOW")

        pw_tool.helper.ui_helper.centre_window(window=self.__window)

    def __update_vault(self):
        """Updates vault
        Redirects back to vault page when successful.
        """
        if not self.__username_entry.get() or not self.__pw_entry.get():
            self.__notification_label.config(text="Please ensure all fields are filled!")
            return

        if self.__username_entry.get() == self.__value["username"] and self.__pw_entry.get() == self.__value[
            "password"]:
            self.__notification_label.config(text="Please change the fields!")
            return

        if not pw_tool.helper.vault_helper.update_vault(website=self.__website, username=self.__username_entry.get(),
                                                        password=self.__pw_entry.get(), old_value=self.__value):
            self.__notification_label.config(text="Old password not allowed!")
            return

        pw_tool.helper.ui_helper.clear_fields(window=self.__entry_frame)

        self.__notification_label.config(text="Successfully Updated!")
        self.__window.after(ms=1000, func=lambda: pw_tool.helper.ui_helper.back(root=self.__master, me=self.__window))
