import secrets
import tkinter.ttk
from tkinter import *
import binascii

import pw_tool.helper.ui_helper


class GenPage:
    def __init__(self, master):
        self.__master = master

        self.__window = tkinter.Toplevel()
        self.__window.geometry(newGeometry="640x480")
        self.__window.title(string="Password Generator")

        # Get length of password to generate
        self.__plength_label = tkinter.ttk.Label(master=self.__window,
                                                 text="Length of password:\n(Minimum length = 12)", font=("Arial", 12))
        self.__plength_label.grid(row=0, column=0, padx=10)

        self.__plength_entry = tkinter.ttk.Entry(master=self.__window, font=("Arial", 12))
        self.__plength_entry.grid(row=0, column=1)

        self.__var_upper = IntVar()
        self.__var_lower = IntVar()
        self.__var_numeric = IntVar()
        self.__var_symbol = IntVar()

        # Get type of characters to include in password
        self.__ptype_label = tkinter.ttk.Label(master=self.__window, text="Type of characters:", font=("Arial", 12))
        self.__ptype_label.grid(row=1, column=0, padx=10)

        self.__ptype1_cbox = tkinter.ttk.Checkbutton(master=self.__window, text="Upper Case A-Z",
                                                     variable=self.__var_upper)
        self.__ptype1_cbox.grid(row=1, column=1)

        self.__ptype2_cbox = tkinter.ttk.Checkbutton(master=self.__window, text="Lower Case a-z",
                                                     variable=self.__var_lower)
        self.__ptype2_cbox.grid(row=1, column=2)

        self.__ptype3_cbox = tkinter.ttk.Checkbutton(master=self.__window, text="Numeric 0-9",
                                                     variable=self.__var_numeric)
        self.__ptype3_cbox.grid(row=2, column=1)

        self.__ptype4_cbox = tkinter.ttk.Checkbutton(master=self.__window, text="!@#$%^&*", variable=self.__var_symbol)
        self.__ptype4_cbox.grid(row=2, column=2)

        # Error message if no input
        self.__error_label = tkinter.ttk.Label(master=self.__window, font=("Arial", 12), background="SystemButtonFace")
        self.__error_label.grid(row=3, column=1)

        # Generate password
        self.__generate_button = tkinter.ttk.Button(master=self.__window, text="Generate", style="TButton",
                                                    command=self.__pgenerator)
        self.__generate_button.grid(row=4, column=1)

        # Display Generated Password
        self.__gpassword_label = tkinter.ttk.Label(master=self.__window, text="Generated Password:", font=("Arial", 12))
        self.__gpassword_label["state"] = DISABLED
        self.__gpassword_label.grid(row=5, column=0, padx=10)

        # copy generated password to clipboard
        self.__copy_button = tkinter.ttk.Button(master=self.__window, text="Copy Password", style="TButton",
                                                command=self.__pcopy)
        self.__copy_button["state"] = DISABLED
        self.__copy_button.grid(row=7, column=1)

        pw_tool.helper.ui_helper.centre_window(window=self.__window)

        self.__window.protocol(
            func=lambda root=master, window=self.__window: pw_tool.helper.ui_helper.back(root=master, me=self.__window),
            name="WM_DELETE_WINDOW")

    def __pgenerator(self):
        # define all possible characters
        uppercase_list = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S',
                          'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
        lowercase_list = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's',
                          't', 'u', 'v', 'w', 'x', 'y', 'z']
        numeric_list = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        symbol_list = ['!', '"', '#', '$', '%', '&', '\'', '(', ')', '*', '+', ',', '-', '.', '/', ':', ';', '<', '=',
                       '>', '?', '@', '[', '\\' ']', '^', '_', '`', '{', '|', '}', '~']

        # character list used to combine all the selected characters
        characters = []

        # used to select one character from each list to fulfill selected character requirement
        rand_upper = ""
        rand_lower = ""
        rand_num = ""
        rand_sym = ""
        character_counter = 0

        # used to combine all random characters to create password
        self.__password = ""

        length = self.__plength_entry.get()
        upper = self.__var_upper.get()
        lower = self.__var_lower.get()
        num = self.__var_numeric.get()
        sym = self.__var_symbol.get()
        secrets_generator = secrets.SystemRandom()

        i = 0
        while i == 0:
            if not length or int(length) <= 11:
                self.__error_label.config(text="Please ensure password length is filled/valid!")
                self.__gpassword_label["state"] = DISABLED
                self.__window.after(0, lambda: self.__password_label.config(text=""))
                self.__copy_button["state"] = DISABLED
                return
            else:
                if not upper and not lower and not num and not sym:
                    self.__error_label.config(text="Please choose the type of characters!")
                    self.__gpassword_label["state"] = DISABLED
                    self.__window.after(0, lambda: self.__password_label.config(text=""))
                    self.__copy_button["state"] = DISABLED
                    return
                else:
                    self.__window.after(0, lambda: self.__error_label.config(text=""))
                    self.__gpassword_label["state"] = NORMAL
                    self.__copy_button["state"] = NORMAL
                    break

        # adding list of selected characters to combined list
        if upper == 1:
            characters += uppercase_list
            # value = secrets_generator.randint(0, len(uppercase_list)-1)
            # rand_upper = uppercase_list[value]
            rand_upper = secrets_generator.choice(uppercase_list)
            character_counter += 1

        if lower == 1:
            characters += lowercase_list
            rand_lower = secrets_generator.choice(lowercase_list)
            character_counter += 1

        if num == 1:
            characters += numeric_list
            rand_num = secrets_generator.choice(numeric_list)
            character_counter += 1

        if sym == 1:
            characters += symbol_list
            rand_sym = secrets_generator.choice(symbol_list)
            character_counter += 1

        self.__password = rand_upper + rand_lower + rand_num + rand_sym
        print(self.__password)
        print(character_counter)

        # generate initial password by selecting random characters
        for x in range(int(length) - character_counter):
            value = secrets_generator.randint(0, len(characters)-1)
            self.__password += characters[value]

        print(self.__password)

        # permute password using feistel rounds
        # generate key using random bits
        def random_key(p):
            key1 = ""
            p = int(p)
            for j in range(p):
                temp = secrets_generator.randint(0,1)
                temp = str(temp)
                key1 += temp
            return key1

        # func for bit XOR
        def xor(a, b):
            temp = ""
            for j in range(n):
                if a[j] == b[j]:
                    temp += "0"
                else:
                    temp += "1"
            return temp

        # change binary to decimal
        def BinToDec(binary):
            string = int(binary, 2)
            return string

        # convert self.__password to ASCII
        pw_ASCII = [ord(x) for x in self.__password]
        print(pw_ASCII)

        # convert ASCII to 8 bit binary
        pw_Bin = [format(y,'08b') for y in pw_ASCII]
        pw_Bin = "".join(pw_Bin)
        print(pw_Bin)

        n = int(len(pw_Bin)//2)
        L1 = pw_Bin[0:n]
        R1 = pw_Bin[n::]
        m = len(R1)
        print(L1)
        print(R1)

        # generate key K1, K2 for the first and second round
        K1 = random_key(m)
        K2 = random_key(m)
        print(K1)
        print(K2)

        # first round of feistel
        f1 = xor(R1, K1)
        R2 = xor(f1, L1)
        L2 = L1
        print(L2)
        print(R2)

        # second round of feistel
        f2 = xor(R2, K2)
        R3 = xor(f2, L2)
        L3 = R2
        print(L3)
        print(R3)

        # "cipher"text
        bin_data = L3 + R3
        str_data = ' '
        for i in range(0, len(bin_data), 7):
            temp_data = bin_data[i:i+7]
            decimal_data = BinToDec(temp_data)
            str_data = str_data + chr(decimal_data)

        self.__password = str_data
        print(self.__password)

        # Decryption
        L4 = L3
        R4 = R3

        f3 = xor(L4, K2)
        L5 = xor(R4, f3)
        R5 = L4

        f4 = xor(L5, K1)
        L6 = xor(R5, f4)
        R6 = L5
        PT1 = L6 + R6

        PT1 = int(PT1, 2)
        RPT = binascii.unhexlify('%x' % PT1)
        self.__decrypt = RPT
        print("Retrieved Plain Text is: ", self.__decrypt)

        # display generated password
        self.__password_label = tkinter.ttk.Label(master=self.__window, text=self.__password, font=("Arial", 12))
        self.__password_label.grid(row=5, column=1, padx=10)

        # password = "".join(password_list[])

    def __pcopy(self):
        print("wuwu")
