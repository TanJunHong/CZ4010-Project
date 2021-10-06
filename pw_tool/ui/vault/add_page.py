import json
import tkinter.ttk

import Crypto.Cipher.AES
import Crypto.Util.Padding

import pw_tool.helper.firebase_helper
import pw_tool.helper.pw_helper
import pw_tool.helper.ui_helper


class AddPage:
    def __init__(self, master, vault):
        self.__master = master
        self.__vault = vault

        self.__window = tkinter.Toplevel()
        self.__window.geometry(newGeometry="640x480")
        self.__window.title(string="Add Item")
        self.__website_label = tkinter.ttk.Label(master=self.__window, text="Website", font=("Arial", 25))
        self.__website_label.pack()

        self.__website_entry = tkinter.ttk.Entry(master=self.__window, font=("Arial", 25))
        self.__website_entry.pack()
        self.__website_entry.focus()

        self.__username_label = tkinter.ttk.Label(master=self.__window, text="Login Username", font=("Arial", 25))
        self.__username_label.pack()

        self.__username_entry = tkinter.ttk.Entry(master=self.__window, font=("Arial", 25))
        self.__username_entry.pack()
        self.__username_entry.focus()

        self.__password_label = tkinter.ttk.Label(master=self.__window, text="Password", font=("Arial", 25))
        self.__password_label.pack()

        self.__password_entry = tkinter.ttk.Entry(master=self.__window, show="*", font=("Arial", 25))
        self.__password_entry.pack()
        self.__password_entry.focus()

        self.__notification_label = tkinter.ttk.Label(master=self.__window, font=("Arial", 25))
        self.__notification_label.pack()

        self.__add_button = tkinter.ttk.Button(master=self.__window, text="Add To Vault", style="TButton",
                                               command=self.__add_to_vault)
        self.__add_button.pack()

        pw_tool.helper.ui_helper.centre_window(window=self.__window)

        self.__window.protocol(
            func=lambda root=master, window=self.__window: pw_tool.helper.ui_helper.back(root=master, me=self.__window),
            name="WM_DELETE_WINDOW")

    def __add_to_vault(self):
        data = ""
        self.__vault[self.__website_entry.get()] = {"username": self.__username_entry.get(),
                                                    "password": self.__password_entry.get()}
        vault_bytes = json.dumps(obj=self.__vault).encode(encoding="utf-8")
        vault_key_bytes = pw_tool.helper.pw_helper.vault_key.encode(encodings="utf-8")
        cipher = Crypto.Cipher.AES.new(key=vault_key_bytes, mode=Crypto.Cipher.AES.MODE_CBC)
        encrypted_vault = cipher.encrypt(
            Crypto.Util.Padding.pad(data_to_pad=vault_bytes, block_size=Crypto.Cipher.AES.block_size))
        # pw_tool.helper.firebase_helper.database.child("vault").child(pw_tool.helper.firebase_helper.auth_key).push()

        self.__notification_label.config(text="Successfully Added!")
        self.__window.after(1000, lambda: pw_tool.helper.ui_helper.back(root=self.__master, me=self.__window))
