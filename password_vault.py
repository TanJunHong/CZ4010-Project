import tkinter

import passlib.context

main_window = tkinter.Tk()
main_window.title(string="Password Manager")


def login_screen():
    main_window.geometry("640x480")

    context = passlib.context.CryptContext(
        schemes=["pbkdf2_sha256"],
        default="pbkdf2_sha256",
        pbkdf2_sha256__default_rounds=50000
    )
    password_hash = context.hash("test")

    password_label = tkinter.Label(main_window, text="Enter Master Password")
    password_label.config(anchor=tkinter.CENTER)
    password_label.pack()

    password_entry = tkinter.Entry(main_window, show="*")
    password_entry.pack()
    password_entry.focus()

    another_label = tkinter.Label(main_window)
    another_label.config(anchor=tkinter.CENTER)
    another_label.pack()

    def check_password():
        if context.verify(password_entry.get(), password_hash):
            password_vault()
        else:
            another_label.config(text="Wrong Password")

    submit_button = tkinter.Button(main_window, text="Submit", command=check_password)
    submit_button.pack()


def password_vault():
    for widget in main_window.winfo_children():
        widget.destroy()
    welcome_label = tkinter.Label(main_window, text="Password Vault")
    welcome_label.config(anchor=tkinter.CENTER)
    welcome_label.pack()


login_screen()
main_window.mainloop()
