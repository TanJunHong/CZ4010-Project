import tkinter.ttk

import pw_tool.helper.ui_helper
import pw_tool.helper.vault_helper
import pw_tool.ui.gen.clear_dialog


class GenHistPage:
    def __init__(self, master):
        """Initialises password history page
        """
        self.__master = master

        self.__window = tkinter.Toplevel()
        self.__window.geometry(newGeometry="960x720")
        self.__window.title(string="Generated Passwords")

        self.__welcome_label = tkinter.ttk.Label(master=self.__window, text="Last 10 Generated Passwords",
                                                 font=pw_tool.helper.ui_helper.font,
                                                 background=pw_tool.helper.ui_helper.background_color)

        self.__clear_button = tkinter.ttk.Button(master=self.__window, text="Clear All", style="LargeFont.TButton",
                                                 command=self.__show_clear_dialog)

        self.__pw_frame = tkinter.ttk.Frame(master=self.__window, style="TFrame")

        counter = 0
        for value in pw_tool.helper.vault_helper.vault["pw_gen_hist"]:
            label = tkinter.ttk.Label(master=self.__pw_frame, text=value, font=pw_tool.helper.ui_helper.small_font,
                                      background=pw_tool.helper.ui_helper.background_color)

            button = tkinter.ttk.Button(master=self.__pw_frame, text="Copy", style="SmallFont.TButton",
                                        command=lambda val=value: pw_tool.helper.ui_helper.copy_to_clipboard(
                                            password=val))

            label.grid(row=counter, column=0, padx=10, pady=5, sticky="W")
            button.grid(row=counter, column=1, padx=10, pady=5, sticky="E")

            counter += 1

        self.__welcome_label.pack(pady=30)
        self.__clear_button.pack(pady=40)
        self.__pw_frame.pack(pady=20)

        self.__window.protocol(func=lambda: pw_tool.helper.ui_helper.back(root=self.__master, me=self.__window),
                               name="WM_DELETE_WINDOW")

        pw_tool.helper.ui_helper.centre_window(window=self.__window)

    def __show_clear_dialog(self):
        """Redirects to clear dialog
        """
        self.__window.destroy()
        pw_tool.ui.gen.clear_dialog.ClearDialog(master=self.__master)
