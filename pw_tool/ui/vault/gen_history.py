import tkinter.ttk

import pw_tool.helper.ui_helper
import pw_tool.helper.vault_helper
import pw_tool.ui.vault.add_page
import pw_tool.ui.vault.change_pw_page
import pw_tool.ui.vault.gen_page
import pw_tool.ui.vault.pw_page


class GenHistPage:
    def __init__(self, master):

        self.__master = master
        self.__master.withdraw()

        self.__labels = {}
        self.__buttons = {}

        self.__window = tkinter.Toplevel()
        self.__window.geometry(newGeometry=pw_tool.helper.ui_helper.window_size)
        self.__window.title(string="Generated Passwords")
        self.__welcome_label = tkinter.ttk.Label(master=self.__window, text="Previously Generated Passwords",
                                                 font=pw_tool.helper.ui_helper.font,
                                                 background=pw_tool.helper.ui_helper.background_color)
        pw_tool.helper.vault_helper.download_vault()