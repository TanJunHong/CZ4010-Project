import tkinter.ttk

import pw_tool.helper.ui_helper
import pw_tool.helper.vault_helper

class GenHistPage:
    def __init__(self, master):

        self.__master = master
        self.__master.withdraw()

        self.__window = tkinter.Toplevel()
        self.__window.geometry(newGeometry=pw_tool.helper.ui_helper.window_size)
        self.__window.title(string="Generated Passwords")

        self.__welcome_label = tkinter.ttk.Label(master=self.__window, text="Previously Generated Passwords",
                                                 font=pw_tool.helper.ui_helper.font,
                                                 background=pw_tool.helper.ui_helper.background_color)

        pw_tool.helper.vault_helper.download_vault()

        # to display passwords
        self.__password_frame = tkinter.ttk.Frame(master=self.__window, style="TFrame")
        # to delete the passwords
        self.__button_frame = tkinter.ttk.Frame(master=self.__window, style="TFrame")

        self.__welcome_label.pack(pady=30)
        self.__password_frame.pack(pady=20)
        self.__button_frame.pack(pady=40)