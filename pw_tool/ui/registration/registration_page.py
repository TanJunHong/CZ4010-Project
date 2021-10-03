import tkinter
import tkinter.ttk

import passlib.hash

import pw_tool.helper.db_helper
import pw_tool.helper.pw_helper
import pw_tool.helper.ui_helper


class RegistrationPage:
    def __init__(self, master):
        self.__master = master
        self.__window = tkinter.Toplevel()
        self.__window.geometry(newGeometry="640x480")
        self.__window.title(string="Registration Page")

        self.__username_label = tkinter.ttk.Label(master=self.__window, text="Username", font=("Arial", 25),
                                                  background="SystemButtonFace")
        self.__username_label.pack()

        self.__username_entry = tkinter.ttk.Entry(master=self.__window, font=("Arial", 25))
        self.__username_entry.pack()
        self.__username_entry.focus()

        self.__password_label = tkinter.ttk.Label(master=self.__window, text="Enter Password", font=("Arial", 25),
                                                  background="SystemButtonFace")
        self.__password_label.pack()

        self.__password_entry = tkinter.ttk.Entry(master=self.__window, show="*", font=("Arial", 25))
        self.__password_entry.pack()
        self.__password_entry.focus()

        self.confirm_password_label = tkinter.ttk.Label(master=self.__window, text="Confirm password",
                                                        font=("Arial", 25), background="SystemButtonFace")
        self.confirm_password_label.pack()

        self.confirm_password_entry = tkinter.ttk.Entry(master=self.__window, show="*", font=("Arial", 25))
        self.confirm_password_entry.pack()
        self.confirm_password_entry.focus()

        self.__notification_label = tkinter.ttk.Label(master=self.__window, font=("Arial", 25),
                                                      background="SystemButtonFace")
        self.__notification_label.pack()

        self.create_account_button = tkinter.ttk.Button(master=self.__window, text="Create Account", style="TButton",
                                                        command=self.__create_account)
        self.create_account_button.pack()

        pw_tool.helper.ui_helper.centre_window(window=self.__window)

        self.__window.protocol(
            func=lambda root=master, window=self.__window: pw_tool.helper.ui_helper.back(root=master, me=self.__window),
            name="WM_DELETE_WINDOW")

    def __create_account(self):
        if not self.__username_entry.get() or not self.__password_entry.get() or not self.confirm_password_entry.get():
            self.__notification_label.config(text="Please ensure all fields are filled!")
            return

        username_hash = passlib.hash.pbkdf2_sha256.hash(secret=self.__username_entry.get(),
                                                        salt=pw_tool.helper.pw_helper.site_wide_salt).split("$")[-1]

        pw_tool.helper.db_helper.cursor.execute("SELECT 1 FROM user_accounts WHERE username = ? LIMIT 1",
                                                [username_hash])
        if len(pw_tool.helper.db_helper.cursor.fetchall()) > 0:
            self.__notification_label.config(text="Username already exists!")
            return
        if self.__password_entry.get() != self.confirm_password_entry.get():
            self.__notification_label.config(text="Passwords do not match!")
            return

        password_hash = pw_tool.helper.pw_helper.context.hash(self.__password_entry.get())

        pw_tool.helper.ui_helper.clear_fields(self.__window)

        pw_tool.helper.db_helper.cursor.execute("""INSERT INTO user_accounts (username, password) VALUES (?, ?) """,
                                                [username_hash, password_hash])
        pw_tool.helper.db_helper.db.commit()

        self.__notification_label.config(text="Successfully Created!")
        self.__window.after(1000, lambda: pw_tool.helper.ui_helper.back(root=self.__master, me=self.__window))
