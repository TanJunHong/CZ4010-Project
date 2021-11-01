import tkinter.ttk

import pw_tool.helper.ui_helper
import pw_tool.helper.vault_helper


class AddPage:
    def __init__(self, master):
        self.__master = master

        self.__window = tkinter.Toplevel()
        self.__window.geometry(newGeometry=pw_tool.helper.ui_helper.window_size)
        self.__window.title(string="Add Item")

        self.__title_label = tkinter.ttk.Label(master=self.__window, text="Add Item",
                                               font=pw_tool.helper.ui_helper.font,
                                               background=pw_tool.helper.ui_helper.background_color)

        self.__entry_frame = tkinter.ttk.Frame(master=self.__window, style="TFrame")

        self.__website_label = tkinter.ttk.Label(master=self.__entry_frame, text="Website",
                                                 font=pw_tool.helper.ui_helper.font,
                                                 background=pw_tool.helper.ui_helper.background_color)

        self.__website_entry = tkinter.ttk.Entry(master=self.__entry_frame, font=pw_tool.helper.ui_helper.font)

        self.__username_label = tkinter.ttk.Label(master=self.__entry_frame, text="Username",
                                                  font=pw_tool.helper.ui_helper.font,
                                                  background=pw_tool.helper.ui_helper.background_color)

        self.__username_entry = tkinter.ttk.Entry(master=self.__entry_frame, font=pw_tool.helper.ui_helper.font)

        self.__password_label = tkinter.ttk.Label(master=self.__entry_frame, text="Password",
                                                  font=pw_tool.helper.ui_helper.font,
                                                  background=pw_tool.helper.ui_helper.background_color)

        self.__password_entry = tkinter.ttk.Entry(master=self.__entry_frame, show="*",
                                                  font=pw_tool.helper.ui_helper.font)

        self.__notification_label = tkinter.ttk.Label(master=self.__window, font=pw_tool.helper.ui_helper.font,
                                                      background=pw_tool.helper.ui_helper.background_color)

        self.__add_button = tkinter.ttk.Button(master=self.__window, text="Add To Vault", style="TButton",
                                               command=self.__add_to_vault)

        self.__website_entry.focus()

        self.__website_label.grid(row=0, column=0, padx=20, pady=5, sticky="E")
        self.__website_entry.grid(row=0, column=1, padx=20, pady=5, sticky="W")
        self.__username_label.grid(row=1, column=0, padx=20, pady=5, sticky="E")
        self.__username_entry.grid(row=1, column=1, padx=20, pady=5, sticky="W")
        self.__password_label.grid(row=2, column=0, padx=20, pady=5, sticky="E")
        self.__password_entry.grid(row=2, column=1, padx=20, pady=5, sticky="W")

        self.__title_label.pack(pady=20)
        self.__entry_frame.pack(pady=30)
        self.__notification_label.pack(pady=5)
        self.__add_button.pack(pady=5)

        pw_tool.helper.ui_helper.centre_window(window=self.__window)

        self.__window.protocol(
            func=lambda root=master, window=self.__window: pw_tool.helper.ui_helper.back(root=master, me=self.__window),
            name="WM_DELETE_WINDOW")

    def __add_to_vault(self):
        if not self.__website_entry.get() or not self.__username_entry.get() or not self.__password_entry.get():
            self.__notification_label.config(text="Please ensure all fields are filled!")
            return

        pw_tool.helper.vault_helper.update_vault(website=self.__website_entry.get(),
                                                 username=self.__username_entry.get(),
                                                 password=self.__password_entry.get())

        pw_tool.helper.ui_helper.clear_fields(window=self.__entry_frame)

        self.__notification_label.config(text="Successfully Added!")
        self.__window.after(ms=1000, func=lambda: pw_tool.helper.ui_helper.back(root=self.__master, me=self.__window))
