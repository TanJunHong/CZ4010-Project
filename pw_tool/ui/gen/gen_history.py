import tkinter.ttk

import pw_tool.helper.ui_helper
import pw_tool.helper.vault_helper
import pw_tool.ui.gen.clear_dialog


class GenHistPage:
    def __init__(self, master):
        """Initialises password history page
        """
        self.__master = master
        self.__master.withdraw()

        self.__labels = []

        self.__window = tkinter.Toplevel()
        self.__window.geometry(newGeometry=pw_tool.helper.ui_helper.window_size)
        self.__window.title(string="Generated Passwords")

        self.__welcome_label = tkinter.ttk.Label(master=self.__window, text="Previously Generated Passwords",
                                                 font=pw_tool.helper.ui_helper.font,
                                                 background=pw_tool.helper.ui_helper.background_color)

        self.__pw_frame = tkinter.ttk.Frame(master=self.__window, style="TFrame")

        counter = 0
        for value in pw_tool.helper.vault_helper.vault["pw_gen_hist"]:
            label = tkinter.ttk.Label(master=self.__pw_frame, text=value, font=pw_tool.helper.ui_helper.font,
                                      background=pw_tool.helper.ui_helper.background_color)

            label.grid(row=counter, column=0, padx=10, pady=5)

            self.__labels.append(label)

            counter += 1

        self.__clear_button = tkinter.ttk.Button(master=self.__window, text="Clear All", style="TButton",
                                                 command=self.__show_clear_dialog)

        self.__welcome_label.pack(pady=30)
        self.__clear_button.pack(pady=40)

        self.__window.protocol(func=lambda: pw_tool.helper.ui_helper.back(root=self.__master, me=self.__window),
                               name="WM_DELETE_WINDOW")

        pw_tool.helper.ui_helper.centre_window(window=self.__window)

    def __show_clear_dialog(self):
        """Redirects to clear dialog
        """
        self.__window.destroy()
        pw_tool.ui.gen.clear_dialog.ClearDialog(master=self.__master)
