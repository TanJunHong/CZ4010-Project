import tkinter
import tkinter.ttk

import pw_tool.helper.firebase_helper
import pw_tool.helper.ui_helper
import pw_tool.helper.vault_helper
import pw_tool.ui.vault.add_page
import pw_tool.ui.vault.gen_page


class EditPage:
    def __init__(self, master, website, value):
        self.__master = master
        self.__master.withdraw()

        self.__website = website
        self.__value = value

        self.__window = tkinter.Toplevel()
        self.__window.geometry(newGeometry="640x480")
        self.__window.title(string="Password Manager")

        self.__website_label = tkinter.ttk.Label(master=self.__window, text=self.__website, font=("Arial", 25),
                                                 background=pw_tool.helper.ui_helper.background_color)
        self.__website_label.pack()

        self.__inner_frame = tkinter.ttk.Frame(master=self.__window, style="TFrame")
        self.__username_label = tkinter.ttk.Label(master=self.__inner_frame, text="Username:", font=("Arial", 25),
                                                  background=pw_tool.helper.ui_helper.background_color)
        self.__username_entry = tkinter.ttk.Entry(master=self.__inner_frame, font=("Arial", 25))
        self.__username_entry.insert(index=0, string=self.__value["username"])
        self.__password_label = tkinter.ttk.Label(master=self.__inner_frame, text="Password:", font=("Arial", 25),
                                                  background=pw_tool.helper.ui_helper.background_color)
        self.__password_entry = tkinter.ttk.Entry(master=self.__inner_frame, font=("Arial", 25))
        self.__password_entry.insert(index=0, string=self.__value["password"])

        self.__username_label.grid(row=0, column=0, padx=20, pady=5, sticky="W")
        self.__username_entry.grid(row=0, column=1, padx=20, pady=5, sticky="E")
        self.__password_label.grid(row=1, column=0, padx=20, pady=5, sticky="W")
        self.__password_entry.grid(row=1, column=1, padx=20, pady=5, sticky="E")
        self.__inner_frame.pack()

        self.__edit_button = tkinter.ttk.Button(master=self.__window, text="Update", style="TButton",
                                                command=self.__update_vault)
        self.__edit_button.pack()

        self.__notification_label = tkinter.ttk.Label(master=self.__window, font=("Arial", 25),
                                                      background=pw_tool.helper.ui_helper.background_color)
        self.__notification_label.pack()

        self.__window.protocol(func=lambda: pw_tool.helper.ui_helper.back(root=self.__master, me=self.__window),
                               name="WM_DELETE_WINDOW")

        pw_tool.helper.ui_helper.centre_window(window=self.__window)

    def __update_vault(self):
        pw_tool.helper.vault_helper.update_vault(website=self.__website,
                                                 username=self.__username_entry.get(),
                                                 password=self.__password_entry.get())

        self.__notification_label.config(text="Successfully Updated!")
        self.__window.after(ms=1000, func=lambda: pw_tool.helper.ui_helper.back(root=self.__master, me=self.__window))
