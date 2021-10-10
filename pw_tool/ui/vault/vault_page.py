import base64
import json
import tkinter
import tkinter.ttk

import Crypto.Cipher.AES
import requests

import pw_tool.helper.firebase_helper
import pw_tool.helper.pw_helper
import pw_tool.helper.ui_helper
import pw_tool.ui.vault.add_page
import pw_tool.ui.vault.delete_page
import pw_tool.ui.vault.gen_page


class VaultPage:
    def __init__(self, master):
        self.__master = master
        self.__master.withdraw()

        self.__window = tkinter.Toplevel()
        self.__window.geometry(newGeometry="640x480")
        self.__window.title(string="Password Manager")
        self.__welcome_label = tkinter.ttk.Label(master=self.__window, text="Password Vault")
        self.__welcome_label.pack()

        try:
            encrypted_vault = pw_tool.helper.firebase_helper.database.child("vault").child(
                pw_tool.helper.firebase_helper.auth_key.split("$")[-1].replace(".", "")).get()
            if encrypted_vault.val() is not None:
                for vault in encrypted_vault.each():
                    result = json.loads(s=vault.val())
                    initialization_vector = base64.b64decode(s=result["iv"])
                    ciphertext = base64.b64decode(s=result["ct"])
                    cipher = Crypto.Cipher.AES.new(key=bytes(pw_tool.helper.pw_helper.vault_key),
                                                   mode=Crypto.Cipher.AES.MODE_CBC, iv=initialization_vector)
                    vault_bytes = Crypto.Util.Padding.unpad(padded_data=cipher.decrypt(ciphertext=ciphertext),
                                                            block_size=Crypto.Cipher.AES.block_size)

                    self.__vault = json.loads(s=vault_bytes.decode(encoding="utf-8"))
            else:
                self.__vault = {}

        except requests.HTTPError as error:
            error_json = error.args[1]
            message = json.loads(error_json)["error"]
            print(message)
            self.__vault = {}

        self.__add_button = tkinter.ttk.Button(master=self.__window, text="Add Vault", style="TButton",
                                               command=self.__show_add_page)
        self.__add_button.pack()

        self.__delete_button = tkinter.ttk.Button(master=self.__window, text="Delete Vault", style="TButton",
                                                  command=self.__show_delete_page)
        self.__delete_button.pack()

        self.__pgenerator_button = tkinter.ttk.Button(master=self.__window, text="Password Generator", style="TButton",
                                                      command=self.__show_gen_page)
        self.__pgenerator_button.pack()

        self.__window.protocol(func=lambda: pw_tool.helper.ui_helper.back(root=self.__master, me=self.__window),
                               name="WM_DELETE_WINDOW")

        pw_tool.helper.ui_helper.centre_window(window=self.__window)

    def __show_delete_page(self):
        self.__window.withdraw()
        pw_tool.ui.vault.delete_page.DeletePage(master=self.__window)

    def __show_add_page(self):
        self.__window.withdraw()
        pw_tool.ui.vault.add_page.AddPage(master=self.__window, vault=self.__vault)

    def __show_gen_page(self):
        self.__window.withdraw()
        pw_tool.ui.vault.gen_page.GenPage(master=self.__window)
