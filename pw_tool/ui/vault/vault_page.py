import tkinter.ttk

import pw_tool.helper.ui_helper
import pw_tool.helper.vault_helper
import pw_tool.ui.gen.gen_page
import pw_tool.ui.vault.add_page
import pw_tool.ui.vault.change_pw_page
import pw_tool.ui.vault.pw_page


class VaultPage:
    def __init__(self, master):
        """Initialises vault page
        """
        self.__master = master

        self.__window = tkinter.Toplevel()
        self.__window.geometry(newGeometry="640x720")
        self.__window.title(string="Password Manager")
        self.__welcome_label = tkinter.ttk.Label(master=self.__window, text="Password Vault",
                                                 font=pw_tool.helper.ui_helper.font,
                                                 background=pw_tool.helper.ui_helper.background_color)

        pw_tool.helper.vault_helper.download_vault()

        self.__website_frame = tkinter.ttk.Frame(master=self.__window, style="TFrame")

        self.__button_frame = tkinter.ttk.Frame(master=self.__window, style="TFrame")

        self.__add_button = tkinter.ttk.Button(master=self.__button_frame, text="+", style="LargeFont.TButton",
                                               command=self.__show_add_page)

        self.__pw_gen_button = tkinter.ttk.Button(master=self.__button_frame, text="Password Generator",
                                                  style="LargeFont.TButton", command=self.__show_gen_page)

        self.__change_master_pw_button = tkinter.ttk.Button(master=self.__button_frame, text="Change Master Password",
                                                            style="LargeFont.TButton",
                                                            command=self.__change_master_password)

        self.__notification_label = tkinter.ttk.Label(master=self.__window, font=pw_tool.helper.ui_helper.font,
                                                      background=pw_tool.helper.ui_helper.background_color,
                                                      foreground="red")

        self.refresh_page()

        self.__add_button.grid(row=0, column=0, padx=10, pady=5, sticky="W")
        self.__pw_gen_button.grid(row=0, column=1, padx=10, pady=5, sticky="E")
        self.__change_master_pw_button.grid(row=1, column=0, columnspan=2, padx=10, pady=5)

        self.__welcome_label.pack(pady=30)
        self.__website_frame.pack(pady=20)
        self.__button_frame.pack(pady=40)
        self.__notification_label.pack(pady=50)

        self.__window.protocol(func=self.__logout, name="WM_DELETE_WINDOW")

        pw_tool.helper.ui_helper.centre_window(window=self.__window)

    def __show_add_page(self):
        """Redirects to add page
        """
        self.__window.withdraw()
        pw_tool.ui.vault.add_page.AddPage(master=self.__window)

    def __show_gen_page(self):
        """Redirects to generator page
        """
        self.__window.withdraw()
        pw_tool.ui.gen.gen_page.GenPage(master=self.__window)

    def __show_pw_page(self, website, value):
        """Redirects to password page
        """
        self.__window.withdraw()
        pw_tool.ui.vault.pw_page.PWPage(master=self.__window, website=website, value=value)

    def __change_master_password(self):
        """Redirects to change master password page
        """
        self.__window.withdraw()
        pw_tool.ui.vault.change_pw_page.ChangePWPage(master=self.__window)

    def refresh_page(self):
        """Refreshes page
        """
        pw_tool.helper.ui_helper.destroy_children(window=self.__website_frame)

        if pw_tool.helper.vault_helper.vault is False:
            self.__notification_label.configure(text="TAMPERED VAULT! LOGGING OUT...")
            self.__window.after(ms=5000, func=self.__logout)
            return

        counter = 0
        for website, value in pw_tool.helper.vault_helper.vault["vault"].items():
            label = tkinter.ttk.Label(master=self.__website_frame, text=website, font=pw_tool.helper.ui_helper.font,
                                      background=pw_tool.helper.ui_helper.background_color)

            button = tkinter.ttk.Button(master=self.__website_frame, text="Show", style="LargeFont.TButton",
                                        command=lambda web=website, val=value: self.__show_pw_page(website=web,
                                                                                                   value=val))

            label.grid(row=counter, column=0, padx=10, pady=5, sticky="W")
            button.grid(row=counter, column=1, padx=10, pady=5, sticky="E")

            counter += 1

    def __logout(self):
        """Logs out
        It will purge client's variables.
        """
        pw_tool.helper.vault_helper.destroy_variables()
        pw_tool.helper.ui_helper.back(root=self.__master, me=self.__window)
