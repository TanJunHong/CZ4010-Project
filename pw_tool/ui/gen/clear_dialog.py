import tkinter.ttk

import pw_tool.helper.ui_helper
import pw_tool.helper.vault_helper


class ClearDialog:
    def __init__(self, master):
        """Initialises clear dialog
        """
        self.__master = master

        self.__window = tkinter.Toplevel()
        self.__window.geometry(newGeometry="640x350")
        self.__window.title(string="Clear History Confirmation")

        self.__title_label = tkinter.ttk.Label(master=self.__window, text="Clear All Confirmation",
                                               font=pw_tool.helper.ui_helper.font,
                                               background=pw_tool.helper.ui_helper.background_color)

        self.__prompt_label = tkinter.ttk.Label(master=self.__window, text="Are you sure you want to clear?",
                                                font=pw_tool.helper.ui_helper.font,
                                                background=pw_tool.helper.ui_helper.background_color)

        self.__inner_frame = tkinter.ttk.Frame(master=self.__window, style="TFrame")

        self.__ok_button = tkinter.ttk.Button(master=self.__inner_frame, text="OK", style="LargeFont.TButton",
                                              command=self.__clear_from_vault)

        self.__cancel_button = tkinter.ttk.Button(master=self.__inner_frame, text="Cancel", style="LargeFont.TButton",
                                                  command=lambda: pw_tool.helper.ui_helper.back(root=self.__master,
                                                                                                me=self.__window))

        self.__notification_label = tkinter.ttk.Label(master=self.__window, font=pw_tool.helper.ui_helper.font,
                                                      background=pw_tool.helper.ui_helper.background_color)

        self.__cancel_button.focus()

        self.__ok_button.grid(row=0, column=0, padx=20, pady=5, sticky="W")
        self.__cancel_button.grid(row=0, column=1, padx=20, pady=5, sticky="E")

        self.__title_label.pack(pady=20)
        self.__prompt_label.pack(pady=30)
        self.__inner_frame.pack(pady=5)
        self.__notification_label.pack(pady=5)

        self.__window.protocol(func=lambda: pw_tool.helper.ui_helper.back(root=self.__master, me=self.__window),
                               name="WM_DELETE_WINDOW")

        pw_tool.helper.ui_helper.centre_window(window=self.__window)

    def __clear_from_vault(self):
        """Clears from vault
        Redirects to generator page afterwards.
        """
        pw_tool.helper.vault_helper.clear_gen_history()

        self.__notification_label.configure(text="Successfully Cleared!")
        self.__window.after(ms=1000, func=lambda: pw_tool.helper.ui_helper.back(root=self.__master, me=self.__window))
