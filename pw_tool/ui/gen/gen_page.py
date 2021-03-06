import tkinter.ttk

import pw_tool.helper.ui_helper
import pw_tool.helper.vault_helper
import pw_tool.ui.gen.gen_history


class GenPage:
    def __init__(self, master, pw_entry=None):
        """Initialises password generator page
        """
        self.__master = master

        self.__password = ""
        self.__pw_entry = pw_entry

        self.__window = tkinter.Toplevel()
        self.__window.geometry(newGeometry="960x480")
        self.__window.title(string="Password Generator")

        self.__welcome_label = tkinter.ttk.Label(master=self.__window, text="Password Generator",
                                                 font=pw_tool.helper.ui_helper.font,
                                                 background=pw_tool.helper.ui_helper.background_color)

        self.__gen_frame = tkinter.ttk.Frame(master=self.__window, style="TFrame")

        self.__pw_len_label = tkinter.ttk.Label(master=self.__gen_frame,
                                                text="Length of password:\n(Minimum length = 12)",
                                                font=pw_tool.helper.ui_helper.small_font,
                                                background=pw_tool.helper.ui_helper.background_color)

        self.__pw_len_entry = tkinter.ttk.Entry(master=self.__gen_frame, font=pw_tool.helper.ui_helper.small_font,
                                                validate="key", validatecommand=(self.__gen_frame.register(
                                                                    func=self.__validate_digit), "%S"))

        self.__type_label = tkinter.ttk.Label(master=self.__gen_frame, text="Type of characters:",
                                              font=pw_tool.helper.ui_helper.small_font,
                                              background=pw_tool.helper.ui_helper.background_color)

        self.__upper_checkbox = tkinter.ttk.Checkbutton(master=self.__gen_frame, text="Upper Case A-Z",
                                                        style="TCheckbutton")

        self.__lower_checkbox = tkinter.ttk.Checkbutton(master=self.__gen_frame, text="Lower Case a-z",
                                                        style="TCheckbutton")

        self.__numeric_checkbox = tkinter.ttk.Checkbutton(master=self.__gen_frame, text="Numeric 0-9",
                                                          style="TCheckbutton")

        self.__symbol_checkbox = tkinter.ttk.Checkbutton(master=self.__gen_frame, text="!@#$%^&*", style="TCheckbutton")

        self.__gen_pw_label = tkinter.ttk.Label(master=self.__gen_frame, text="Generated Password:",
                                                state=tkinter.DISABLED, font=pw_tool.helper.ui_helper.small_font,
                                                background=pw_tool.helper.ui_helper.background_color)

        self.__pw_label = tkinter.ttk.Label(master=self.__gen_frame, font=pw_tool.helper.ui_helper.small_font,
                                            background=pw_tool.helper.ui_helper.background_color)

        self.__error_frame = tkinter.ttk.Frame(master=self.__window, style="TFrame")

        self.__error_label = tkinter.ttk.Label(master=self.__error_frame, font=pw_tool.helper.ui_helper.small_font,
                                               background=pw_tool.helper.ui_helper.background_color)

        self.__button_frame = tkinter.ttk.Frame(master=self.__window, style="TFrame")

        self.__generate_button = tkinter.ttk.Button(master=self.__button_frame, text="Generate",
                                                    style="LargeFont.TButton", command=self.__generate_pw)

        self.__copy_button = tkinter.ttk.Button(master=self.__button_frame, text="Copy Password",
                                                state=tkinter.DISABLED, style="LargeFont.TButton",
                                                command=lambda: pw_tool.helper.ui_helper.copy_to_clipboard(
                                                    password=self.__password))

        self.__dynamic_frame = tkinter.ttk.Frame(master=self.__window, style="TFrame")

        self.__dynamic_button = tkinter.ttk.Button(master=self.__dynamic_frame, text="Previously Generated Password",
                                                   style="LargeFont.TButton", command=self.__show_hist_page) \
            if pw_entry is None else tkinter.ttk.Button(master=self.__dynamic_frame, text="Use Password",
                                                        style="LargeFont.TButton", command=self.__show_master_page)

        self.__notif_frame = tkinter.ttk.Frame(master=self.__window, style="TFrame")
        self.__copy_notif_label = tkinter.ttk.Label(master=self.__notif_frame, font=pw_tool.helper.ui_helper.small_font,
                                                    background=pw_tool.helper.ui_helper.background_color)

        self.__pw_len_label.focus()

        self.__pw_len_label.grid(row=0, column=0, padx=20, pady=5, sticky="W")
        self.__pw_len_entry.grid(row=0, column=1, padx=20, pady=5, sticky="W")
        self.__type_label.grid(row=1, column=0, padx=20, pady=5, sticky="W")
        self.__upper_checkbox.grid(row=1, column=1, padx=20, pady=5, sticky="W")
        self.__lower_checkbox.grid(row=1, column=2, padx=20, pady=5, sticky="W")
        self.__numeric_checkbox.grid(row=2, column=1, padx=20, pady=5, sticky="W")
        self.__symbol_checkbox.grid(row=2, column=2, padx=20, pady=5, sticky="W")
        self.__gen_pw_label.grid(row=3, column=0, padx=20, pady=5, sticky="W")
        self.__pw_label.grid(row=3, column=1, columnspan=50, padx=20, pady=5, sticky="W")

        self.__error_label.grid(row=0, column=1, padx=20, pady=5, sticky="E")

        self.__generate_button.grid(row=0, column=0, padx=20, pady=5, sticky="E")
        self.__copy_button.grid(row=0, column=1, padx=20, pady=5, sticky="W")

        self.__dynamic_button.grid(row=0, column=1, padx=20, pady=5, sticky="E")

        self.__copy_notif_label.grid(row=0, column=1, padx=20, pady=5, sticky="E")

        self.__welcome_label.pack(pady=25)
        self.__gen_frame.pack(pady=5)
        self.__error_frame.pack(pady=5)
        self.__button_frame.pack(pady=5)
        self.__dynamic_frame.pack(pady=5)
        self.__notif_frame.pack(pady=5)

        self.__window.protocol(func=lambda: pw_tool.helper.ui_helper.back(root=self.__master, me=self.__window),
                               name="WM_DELETE_WINDOW")

        pw_tool.helper.ui_helper.centre_window(window=self.__window)

    def __generate_pw(self):
        """Generates password, stores in vault and displays it
        """
        length = int(self.__pw_len_entry.get()) if self.__pw_len_entry.get() else 0

        if length < 12 or length > 64:
            self.__error_label.configure(text="Please ensure password length is filled/valid! (12-64)")
            self.__pw_label.configure(text="")
            self.__gen_pw_label.configure(state=tkinter.DISABLED)
            self.__copy_button.configure(state=tkinter.DISABLED)
            return

        config = {"upper":   self.__upper_checkbox.instate(statespec=["selected"]),
                  "lower":   self.__lower_checkbox.instate(statespec=["selected"]),
                  "numeric": self.__numeric_checkbox.instate(statespec=["selected"]),
                  "symbol":  self.__symbol_checkbox.instate(statespec=["selected"])}

        if not any(value for value in config.values()):
            self.__error_label.configure(text="Please choose the type of characters!")
            self.__pw_label.configure(text="")
            self.__gen_pw_label.configure(state=tkinter.DISABLED)
            self.__copy_button.configure(state=tkinter.DISABLED)
            return

        self.__error_label.configure(text="")
        self.__gen_pw_label.configure(state=tkinter.NORMAL)
        self.__copy_button.configure(state=tkinter.NORMAL)

        self.__password = pw_tool.helper.vault_helper.generate_pw(length=length, config=config)

        pw_tool.helper.vault_helper.add_gen_pw(password=self.__password)

        self.__pw_label.configure(text=self.__password)

    def __validate_digit(self, char):
        """Validates input, making sure it contains only digits
        Rings bell if invalid input.
        """
        if char in pw_tool.helper.vault_helper.numeric_list:
            return True

        self.__gen_frame.bell()
        return False

    def __show_hist_page(self):
        """Redirects to history page
        """
        self.__window.withdraw()
        pw_tool.ui.gen.gen_history.GenHistPage(master=self.__window)

    def __show_master_page(self):
        """Fills password and redirects back to master page
        """
        self.__pw_entry.delete(first=0, last=tkinter.END)
        self.__pw_entry.insert(index=0, string=self.__password)
        pw_tool.helper.ui_helper.back(root=self.__master, me=self.__window)
