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

        # to delete the passwords
        self.__clear_button = tkinter.ttk.Button(master=self.__window, text="Clear All", style="TButton",
                                                  command=self.__show_clear_dialog)
        self.__welcome_label.pack(pady=30)
        self.__clear_button.pack(pady=40)

    def __show_clear_dialog(self):
        self.__window.destroy()
        pw_tool.ui.vault.clear_dialog.ClearDialog(master=self.__master, website=self.__website)

