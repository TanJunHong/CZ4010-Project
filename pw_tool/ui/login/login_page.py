import tkinter.ttk

import passlib.hash
import ttkthemes

import pw_tool.helper.db_helper
import pw_tool.helper.pw_helper
import pw_tool.helper.ui_helper
import pw_tool.ui.registration.registration_page
import pw_tool.ui.vault.vault_page


class LoginPage:
    def __init__(self):
        self.__window = ttkthemes.ThemedTk(theme="arc")
        self.__window.geometry(newGeometry="640x480")
        self.__window.title(string="Password Manager")

        pw_tool.helper.ui_helper.create_style()

        self.__username_label = tkinter.ttk.Label(master=self.__window, text="Username", font=("Arial", 25),
                                                  background="SystemButtonFace")
        self.__username_label.pack()

        self.__username_entry = tkinter.ttk.Entry(master=self.__window, font=("Arial", 25))
        self.__username_entry.pack()
        self.__username_entry.focus()

        self.__password_label = tkinter.ttk.Label(master=self.__window, text="Enter Master Password",
                                                  font=("Arial", 25), background="SystemButtonFace")
        self.__password_label.pack()

        self.__password_entry = tkinter.ttk.Entry(master=self.__window, show="*", font=("Arial", 25))
        self.__password_entry.pack()
        self.__password_entry.focus()

        self.__notification_label = tkinter.ttk.Label(master=self.__window, font=("Arial", 25),
                                                      background="SystemButtonFace")
        self.__notification_label.pack()

        self.__login_button = tkinter.ttk.Button(master=self.__window, text="Login", style="TButton",
                                                 command=self.__verify_login)
        self.__login_button.pack()

        self.__register_button = tkinter.ttk.Button(master=self.__window, text="Register", style="TButton",
                                                    command=self.__show_register_page)
        self.__register_button.pack()

        pw_tool.helper.ui_helper.centre_window(window=self.__window)
        self.__window.mainloop()

    def __show_register_page(self):
        pw_tool.helper.ui_helper.clear_fields(window=self.__window)
        self.__window.withdraw()
        pw_tool.ui.registration.registration_page.RegistrationPage(master=self.__window)

    def __verify_login(self):
        if not self.__username_entry.get() or not self.__password_entry.get():
            self.__notification_label.config(text="Please ensure all fields are filled!")
            return

        username_hash = passlib.hash.pbkdf2_sha256.hash(secret=self.__username_entry.get(),
                                                        salt=pw_tool.helper.pw_helper.site_wide_salt).split("$")[-1]

        pw_tool.helper.db_helper.cursor.execute("SELECT password FROM user_accounts WHERE username = ?",
                                                [username_hash])
        password_hash = pw_tool.helper.db_helper.cursor.fetchone()

        if not password_hash or not pw_tool.helper.pw_helper.context.verify(self.__password_entry.get(),
                                                                            password_hash[0]):
            self.__notification_label.config(text="Wrong Username or Password!")
            return

        pw_tool.helper.ui_helper.clear_fields(self.__window)

        self.__notification_label.config(text="Login Successful! Redirecting you...")
        self.__window.after(1000, lambda: self.__notification_label.config(text=""))
        self.__window.after(1000, lambda: pw_tool.ui.vault.vault_page.VaultPage(master=self.__window))
