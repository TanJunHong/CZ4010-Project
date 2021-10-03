import tkinter
import tkinter.ttk

import pw_tool.helper.db_helper
import pw_tool.helper.ui_helper
import pw_tool.ui.vault.add_page
import pw_tool.ui.vault.delete_page
import pw_tool.ui.vault.gen_page


class VaultPage:
    def __init__(self, master):
        self.__master = master
        self.__master.withdraw()

        self.__window = tkinter.Toplevel()
        self.__window.geometry(newGeometry="640x480")
        self.__window.title(string="Password Manager")
        self.__welcome_label = tkinter.ttk.Label(master=self.__window, text="Password Vault")
        self.__welcome_label.pack()

        self.__add_button = tkinter.ttk.Button(master=self.__window, text="Add Vault", style="TButton",
                                               command=self.__show_add_page)
        self.__add_button.pack()

        self.__delete_button = tkinter.ttk.Button(master=self.__window, text="Delete Vault", style="TButton",
                                                  command=self.__show_delete_page)
        self.__delete_button.pack()

        self.__pgenerator_button = tkinter.ttk.Button(master=self.__window, text="Password Generator", style="TButton",
                                                      command=self.__show_gen_page)
        self.__pgenerator_button.pack()

        self.__window.protocol(func=lambda: pw_tool.helper.ui_helper.back(root=self.__master, me=self.__window),
                               name="WM_DELETE_WINDOW")

        pw_tool.helper.ui_helper.centre_window(window=self.__window)

    def __show_delete_page(self):
        self.__window.withdraw()
        pw_tool.ui.vault.delete_page.DeletePage(master=self.__window)

    def __show_add_page(self):
        self.__window.withdraw()
        pw_tool.ui.vault.add_page.AddPage(master=self.__window)

    def __show_gen_page(self):
        self.__window.withdraw()
        pw_tool.ui.vault.gen_page.GenPage(master=self.__window)
