import base64
import json
import tkinter
import tkinter.ttk

import Crypto.Cipher.AES
import requests

import pw_tool.helper.firebase_helper
import pw_tool.helper.ui_helper
import pw_tool.helper.vault_helper
import pw_tool.ui.vault.add_page
import pw_tool.ui.vault.gen_page
import pw_tool.ui.vault.pw_page


class VaultPage:
    def __init__(self, master):
        self.__master = master
        self.__master.withdraw()

        self.__buttons = {}
        self.__labels = {}

        self.__window = tkinter.Toplevel()
        self.__window.geometry(newGeometry="640x480")
        self.__window.title(string="Password Manager")
        self.__welcome_label = tkinter.ttk.Label(master=self.__window, text="Password Vault", font=("Arial", 25),
                                                 background="SystemButtonFace")
        self.__welcome_label.pack()

        try:
            data = pw_tool.helper.firebase_helper.database.child("vault").child(
                pw_tool.helper.firebase_helper.auth_key.split("$")[-1].replace(".", "")).get()
            if data.val() is not None:
                result = json.loads(s=data.val())
                initialization_vector = base64.b64decode(s=result["iv"])
                ciphertext = base64.b64decode(s=result["ct"])
                cipher = Crypto.Cipher.AES.new(key=bytes(pw_tool.helper.vault_helper.vault_key),
                                               mode=Crypto.Cipher.AES.MODE_CBC, iv=initialization_vector)
                vault_bytes = Crypto.Util.Padding.unpad(padded_data=cipher.decrypt(ciphertext=ciphertext),
                                                        block_size=Crypto.Cipher.AES.block_size)

                pw_tool.helper.vault_helper.vault = json.loads(s=vault_bytes.decode(encoding="utf-8"))

        except requests.HTTPError as error:
            error_json = error.args[1]
            message = json.loads(error_json)["error"]
            print(message)

        self.__inner_frame = tkinter.ttk.Frame(master=self.__window, style="TFrame")

        counter = 0
        for website, value in pw_tool.helper.vault_helper.vault.items():
            self.__labels[website] = tkinter.ttk.Label(master=self.__inner_frame, text=website, font=("Arial", 25),
                                                       background="SystemButtonFace")
            self.__buttons[website] = tkinter.ttk.Button(master=self.__inner_frame, text="Show", style="TButton",
                                                         command=lambda web=website, val=value: self.__show_pw_page(
                                                             website=web, value=val))

            self.__labels[website].grid(row=counter, column=0, padx=10, pady=5, sticky="W")
            self.__buttons[website].grid(row=counter, column=1, padx=10, pady=5, sticky="E")

            counter += 1

        self.__inner_frame.pack()

        self.__add_button = tkinter.ttk.Button(master=self.__window, text="+", style="TButton",
                                               command=self.__show_add_page)
        self.__add_button.pack()

        self.__pgenerator_button = tkinter.ttk.Button(master=self.__window, text="Password Generator", style="TButton",
                                                      command=self.__show_gen_page)
        self.__pgenerator_button.pack()

        self.__window.protocol(func=lambda: pw_tool.helper.ui_helper.back(root=self.__master, me=self.__window),
                               name="WM_DELETE_WINDOW")

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
