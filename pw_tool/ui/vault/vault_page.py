import base64
import tkinter
import tkinter.ttk

import pw_tool.helper.fb_helper
import pw_tool.helper.ui_helper
import pw_tool.helper.vault_helper
import pw_tool.ui.vault.add_page
import pw_tool.ui.vault.change_pw_page
import pw_tool.ui.vault.gen_page
import pw_tool.ui.vault.pw_page


class VaultPage:
    def __init__(self, master):
        self.__master = master
        self.__master.withdraw()

        self.__labels = {}
        self.__buttons = {}

        self.__window = tkinter.Toplevel()
        self.__window.geometry(newGeometry=pw_tool.helper.ui_helper.window_size)
        self.__window.title(string="Password Manager")
        self.__welcome_label = tkinter.ttk.Label(master=self.__window, text="Password Vault",
                                                 font=pw_tool.helper.ui_helper.font,
                                                 background=pw_tool.helper.ui_helper.background_color)

        pw_tool.helper.vault_helper.load_vault()

        self.__website_frame = tkinter.ttk.Frame(master=self.__window, style="TFrame")

        self.__button_frame = tkinter.ttk.Frame(master=self.__window, style="TFrame")

        self.__add_button = tkinter.ttk.Button(master=self.__button_frame, text="+", style="TButton",
                                               command=self.__show_add_page)

        self.__pgenerator_button = tkinter.ttk.Button(master=self.__button_frame, text="Password Generator",
                                                      style="TButton", command=self.__show_gen_page)

        self.refresh_page()

        self.__add_button.grid(row=0, column=0, padx=10, pady=5, sticky="W")
        self.__pgenerator_button.grid(row=0, column=1, padx=10, pady=5, sticky="E")

        self.__welcome_label.pack(pady=30)
        self.__website_frame.pack(pady=20)
        self.__button_frame.pack(pady=40)

        self.__window.protocol(func=self.__logout, name="WM_DELETE_WINDOW")

        pw_tool.helper.ui_helper.centre_window(window=self.__window)

    def __show_add_page(self):
        self.__window.withdraw()
        pw_tool.ui.vault.add_page.AddPage(master=self.__window)

    def __show_gen_page(self):
        self.__window.withdraw()
        pw_tool.ui.vault.gen_page.GenPage(master=self.__window)

    def __show_pw_page(self, website, value):
        self.__window.withdraw()
        pw_tool.ui.vault.pw_page.PWPage(master=self.__window, website=website, value=value)
        pass

    def refresh_page(self):
        pw_tool.helper.ui_helper.destroy_children(window=self.__website_frame)

        self.__labels = {}
        self.__buttons = {}

        counter = 0
        for website, value in pw_tool.helper.vault_helper.vault.items():
            self.__labels[website] = tkinter.ttk.Label(master=self.__website_frame, text=website,
                                                       font=pw_tool.helper.ui_helper.font,
                                                       background=pw_tool.helper.ui_helper.background_color)

            self.__buttons[website] = tkinter.ttk.Button(master=self.__website_frame, text="Show", style="TButton",
                                                         command=lambda web=website, val=value: self.__show_pw_page(
                                                             website=web, value=val))

            self.__labels[website].grid(row=counter, column=0, padx=10, pady=5, sticky="W")
            self.__buttons[website].grid(row=counter, column=1, padx=10, pady=5, sticky="E")

            counter += 1

    def __logout(self):
        pw_tool.helper.vault_helper.destroy_variables()
        pw_tool.helper.ui_helper.back(root=self.__master, me=self.__window)
