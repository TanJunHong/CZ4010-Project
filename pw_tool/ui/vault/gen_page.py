import binascii
import math
import secrets
import statistics
import tkinter.ttk

import statsmodels.sandbox.stats.runs

import pw_tool.helper.ui_helper
import pw_tool.ui.vault.gen_history


def _change_clipboard(string, tk):
    # change clipboard to given string
    tk.clipboard_clear()
    tk.clipboard_append(string=string)
    tk.update()


class GenPage:
    def __init__(self, master):
        self.__master = master
        self.__master.withdraw()

        self.__window = tkinter.Toplevel()
        self.__window.geometry(newGeometry=pw_tool.helper.ui_helper.window_size)
        self.__window.title(string="Password Generator")

        self.__welcome_label = tkinter.ttk.Label(master=self.__window, text="Password Generator",
                                                 font=pw_tool.helper.ui_helper.font,
                                                 background=pw_tool.helper.ui_helper.background_color)

        self.__gen_frame = tkinter.ttk.Frame(master=self.__window, style="TFrame")

        # Get length of password to generate
        self.__plength_label = tkinter.ttk.Label(master=self.__gen_frame,
                                                 text="Length of password:\n(Minimum length = 12)",
                                                 font=("Arial", 12),
                                                 background=pw_tool.helper.ui_helper.background_color)

        self.__plength_entry = tkinter.ttk.Entry(master=self.__gen_frame, font=("Arial", 12))

        self.__var_upper = tkinter.IntVar()
        self.__var_lower = tkinter.IntVar()
        self.__var_numeric = tkinter.IntVar()
        self.__var_symbol = tkinter.IntVar()

        # Get type of characters to include in password
        self.__ptype_label = tkinter.ttk.Label(master=self.__gen_frame, text="Type of characters:", font=("Arial", 12),
                                               background=pw_tool.helper.ui_helper.background_color)

        self.__ptype1_cbox = tkinter.ttk.Checkbutton(master=self.__gen_frame, text="Upper Case A-Z",
                                                     variable=self.__var_upper)

        self.__ptype2_cbox = tkinter.ttk.Checkbutton(master=self.__gen_frame, text="Lower Case a-z",
                                                     variable=self.__var_lower)

        self.__ptype3_cbox = tkinter.ttk.Checkbutton(master=self.__gen_frame, text="Numeric 0-9",
                                                     variable=self.__var_numeric)

        self.__ptype4_cbox = tkinter.ttk.Checkbutton(master=self.__gen_frame, text="!@#$%^&*",
                                                     variable=self.__var_symbol)

        # Display Generated Password
        self.__gpassword_label = tkinter.ttk.Label(master=self.__gen_frame, text="Generated Password:",
                                                   font=("Arial", 12),
                                                   background=pw_tool.helper.ui_helper.background_color)
        self.__gpassword_label["state"] = tkinter.DISABLED

        self.__pw_label = tkinter.ttk.Label(master=self.__gen_frame, font=("Arial", 12),
                                            background=pw_tool.helper.ui_helper.background_color)

        self.__error_frame = tkinter.ttk.Frame(master=self.__window, style="TFrame")

        # Error message if no input
        self.__error_label = tkinter.ttk.Label(master=self.__error_frame, font=("Arial", 12),
                                               background=pw_tool.helper.ui_helper.background_color)

        self.__button_frame = tkinter.ttk.Frame(master=self.__window, style="TFrame")

        # Generate password
        self.__generate_button = tkinter.ttk.Button(master=self.__button_frame, text="Generate", style="TButton",
                                                    command=self.__pgenerator)

        # copy generated password to clipboard
        self.__copy_button = tkinter.ttk.Button(master=self.__button_frame, text="Copy Password", style="TButton",
                                                command=self.__pcopy)
        self.__copy_button["state"] = tkinter.DISABLED

        self.__button2_frame = tkinter.ttk.Frame(master=self.__window, style="TFrame")

        # view previously generated password
        self.__pgenhistory_button = tkinter.ttk.Button(master=self.__button2_frame,
                                                       text="Previously Generated Password",
                                                       style="TButton", command=self.__show_genhist_page)

        # copied notification
        self.__noti_frame = tkinter.ttk.Frame(master=self.__window, style="TFrame")
        self.__copynoti_label = tkinter.ttk.Label(master=self.__noti_frame, font=("Arial", 12),
                                                  background=pw_tool.helper.ui_helper.background_color)

        self.__plength_label.focus()

        self.__plength_label.grid(row=0, column=0, padx=20, pady=5, sticky="W")
        self.__plength_entry.grid(row=0, column=1, padx=20, pady=5, sticky="E")
        self.__ptype_label.grid(row=1, column=0, padx=20, pady=5, sticky="W")
        self.__ptype1_cbox.grid(row=1, column=1, padx=20, pady=5, sticky="W")
        self.__ptype2_cbox.grid(row=1, column=2, padx=20, pady=5, sticky="W")
        self.__ptype3_cbox.grid(row=2, column=1, padx=20, pady=5, sticky="W")
        self.__ptype4_cbox.grid(row=2, column=2, padx=20, pady=5, sticky="W")
        self.__gpassword_label.grid(row=3, column=0, padx=20, pady=5, sticky="W")
        self.__pw_label.grid(row=3, column=1, padx=20, pady=5, sticky="W")

        self.__error_label.grid(row=0, column=1, padx=20, pady=5, sticky="E")

        self.__generate_button.grid(row=0, column=0, padx=20, pady=5, sticky="E")
        self.__copy_button.grid(row=0, column=1, padx=20, pady=5, sticky="W")

        self.__pgenhistory_button.grid(row=0, column=1, padx=20, pady=5, sticky="E")

        self.__copynoti_label.grid(row=0, column=1, padx=20, pady=5, sticky="E")

        self.__welcome_label.pack(pady=25)
        self.__gen_frame.pack(pady=5)
        self.__error_frame.pack(pady=5)
        self.__button_frame.pack(pady=5)
        self.__button2_frame.pack(pady=5)
        self.__noti_frame.pack(pady=5)

        self.__window.protocol(
            func=lambda root=master, window=self.__window: pw_tool.helper.ui_helper.back(root=master, me=self.__window),
            name="WM_DELETE_WINDOW")
        pw_tool.helper.ui_helper.centre_window(window=self.__window)

    def __pgenerator(self):
        # destroy previously displayed password
        self.__pw_label.after(1000, self.__pw_label.destroy())

        # define all possible characters
        uppercase_list = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S',
                          'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
        lowercase_list = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's',
                          't', 'u', 'v', 'w', 'x', 'y', 'z']
        numeric_list = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        symbol_list = ['!', '"', '#', '$', '%', '&', '\'', '(', ')', '*', '+', ',', '-', '.', '/', ':', ';', '<', '=',
                       '>', '?', '@', '[', '\\', ']', '^', '_', '`', '{', '|', '}', '~']

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
                self.__gpassword_label["state"] = tkinter.DISABLED
                self.__window.after(0, lambda: self.__pw_label.config(text=""))
                self.__copy_button["state"] = tkinter.DISABLED
                return
            else:
                if not upper and not lower and not num and not sym:
                    self.__error_label.config(text="Please choose the type of characters!")
                    self.__gpassword_label["state"] = tkinter.DISABLED
                    self.__window.after(0, lambda: self.__pw_label.config(text=""))
                    self.__copy_button["state"] = tkinter.DISABLED
                    return
                else:
                    self.__window.after(0, lambda: self.__error_label.config(text=""))
                    self.__gpassword_label["state"] = tkinter.NORMAL
                    self.__copy_button["state"] = tkinter.NORMAL
                    break

        # adding list of selected characters to combined list
        if upper == 1:
            characters += uppercase_list
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

        # to ensure that there is at least 1 of the selected type of variable
        self.__password = rand_upper + rand_lower + rand_num + rand_sym

        # generate initial password by selecting random characters
        for x in range(int(length) - character_counter):
            value = secrets_generator.randint(0, len(characters) - 1)
            self.__password += characters[value]

        print(self.__password)

        # permute password using feistel rounds
        # generate key using random bits
        def random_key(p):
            key1 = ""
            p = int(p)
            for j in range(p):
                temp = secrets_generator.randint(0, 1)
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
        def bin_to_dec(binary):
            string = int(binary, 2)
            return string

        # get the index of each character
        pw_index = []
        for x in self.__password:
            index = characters.index(x)
            pw_index.append(index)
        print(pw_index)

        # convert decimal index to 8 bit binary
        pw_bin = [format(y, '08b') for y in pw_index]
        pw_bin = "".join(pw_bin)
        print(pw_bin)

        n = int(len(pw_bin) // 2)
        l1 = pw_bin[0:n]
        r1 = pw_bin[n::]
        m = len(r1)

        # generate key k1, k2 for the first and second round
        k1 = random_key(m)
        k2 = random_key(m)
        k3 = random_key(m)
        k4 = random_key(m)
        k5 = random_key(m)

        # first round of feistel
        f1 = xor(r1, k1)
        r2 = xor(f1, l1)
        l2 = l1

        # second round of feistel
        f2 = xor(r2, k2)
        r3 = xor(f2, l2)
        l3 = r2

        # third round of feistel
        f3 = xor(r3, k3)
        r4 = xor(f3, l3)
        l4 = r3

        # fourth round of feistel
        f4 = xor(r4, k4)
        r5 = xor(f4, l4)
        l5 = r4

        # fifth round of feistel
        f5 = xor(r5, k5)
        r6 = xor(f5, l5)
        l6 = r5

        # "cipher"text
        bin_data = l6 + r6
        str_data = ' '
        decimal_list = []
        for i in range(0, len(bin_data), 7):
            temp_data = bin_data[i:i + 7]
            decimal_data = bin_to_dec(temp_data)
            decimal_data %= len(characters)
            decimal_list.append(decimal_data)
            print(decimal_data)
            str_data = str_data + characters[decimal_data]

        print(str_data)
        print(decimal_list)

        self.__password = str_data[0:int(length) + 1]
        print(self.__password)

        # display generated password
        self.__pw_label = tkinter.ttk.Label(master=self.__gen_frame, font=("Arial", 12),
                                            background=pw_tool.helper.ui_helper.background_color)
        self.__pw_label.configure(text=self.__password)
        self.__pw_label.grid(row=3, column=1, padx=20, pady=5, sticky="W")

        def runsTest(l, l_median):

            runs, n1, n2 = 0, 0, 0

            # Checking for start of new run
            for k in range(len(l)):

                # no. of runs
                if (l[k] >= l_median > l[k - 1]) or \
                        (l[k] < l_median <= l[k - 1]):
                    runs += 1

                    # no. of positive values
                if (l[k]) >= l_median:
                    n1 += 1

                    # no. of negative values
                else:
                    n2 += 1

            runs_exp = ((2 * n1 * n2) / (n1 + n2)) + 1
            stan_dev = math.sqrt((2 * n1 * n2 * (2 * n1 * n2 - n1 - n2)) / \
                                 (((n1 + n2) ** 2) * (n1 + n2 - 1)))

            z = (runs - runs_exp) / stan_dev

            return z

        l_median = statistics.median(decimal_list)
        z_value = abs(runsTest(decimal_list, l_median))

        print('Z-statistic= ', z_value)

        x = statsmodels.sandbox.stats.runs.runstest_1samp(decimal_list, correction=False)
        print(x)

    def __pcopy(self):
        tk = tkinter.Tk()
        tk.withdraw()
        _change_clipboard(string=self.__password, tk=tk)
        tk.after(ms=10000, func=lambda: _change_clipboard(string="", tk=tk))
        tk.after(ms=10500, func=tk.destroy)
        self.__copynoti_label.config(text="Copied to clipboard!")
        self.__window.after(10000, lambda: self.__copynoti_label.config(text=""))
        print(self.__password + " uwu")

    def __show_genhist_page(self):
        self.__window.withdraw()
        pw_tool.ui.vault.gen_history.GenHistPage(master=self.__window)
