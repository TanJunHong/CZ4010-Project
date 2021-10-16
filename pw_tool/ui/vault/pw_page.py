import tkinter
import tkinter.ttk

import pw_tool.helper.firebase_helper
import pw_tool.helper.pw_helper
import pw_tool.helper.ui_helper
import pw_tool.ui.vault.add_page
import pw_tool.ui.vault.gen_page


class PWPage:
    def __init__(self, master, website, value):
        self.__master = master
        self.__master.withdraw()

        self.__window = tkinter.Toplevel()
        self.__window.geometry(newGeometry="640x480")
        self.__window.title(string="Password Manager")

        self.__website_label = tkinter.ttk.Label(master=self.__window, text=website, font=("Arial", 25),
                                                 background="SystemButtonFace")
        self.__website_label.pack()

        self.__inner_frame = tkinter.ttk.Frame(master=self.__window, style="TFrame")
        self.__username = tkinter.ttk.Label(master=self.__inner_frame, text="Username:", font=("Arial", 25),
                                            background="SystemButtonFace")
        self.__username_label = tkinter.ttk.Label(master=self.__inner_frame, text=value["username"], font=("Arial", 25),
                                                  background="SystemButtonFace")
        self.__pw = tkinter.ttk.Label(master=self.__inner_frame, text="Password:", font=("Arial", 25),
                                      background="SystemButtonFace")
        self.__pw_label = tkinter.ttk.Label(master=self.__inner_frame, text=value["password"], font=("Arial", 25),
                                            background="SystemButtonFace")

        self.__username.grid(row=0, column=0, padx=20, pady=5, sticky="W")
        self.__username_label.grid(row=0, column=1, padx=20, pady=5, sticky="E")
        self.__pw.grid(row=1, column=0, padx=20, pady=5, sticky="W")
        self.__pw_label.grid(row=1, column=1, padx=20, pady=5, sticky="E")
        self.__inner_frame.pack()

        self.__edit_button = tkinter.ttk.Button(master=self.__window, text="Edit", style="TButton",
                                                command=self.__show_edit_page)
        self.__edit_button.pack()

        self.__window.protocol(func=lambda: pw_tool.helper.ui_helper.back(root=self.__master, me=self.__window),
                               name="WM_DELETE_WINDOW")

        pw_tool.helper.ui_helper.centre_window(window=self.__window)

    def __show_edit_page(self):
        self.__window.withdraw()
