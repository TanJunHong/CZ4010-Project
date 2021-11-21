import binascii
import math
import secrets
import statistics
import string
import tkinter.ttk

import statsmodels.sandbox.stats.runs

import pw_tool.helper.ui_helper
import pw_tool.helper.vault_helper
import pw_tool.ui.gen.gen_history

uppercase_list = list(string.ascii_uppercase)
lowercase_list = list(string.ascii_lowercase)
numeric_list = list(string.digits)
symbol_list = list(string.punctuation)


class GenPage:
    def __init__(self, master):
        """Initialises password generator page
        """
        self.__master = master

        self.__window = tkinter.Toplevel()
        self.__window.geometry(newGeometry=pw_tool.helper.ui_helper.window_size)
        self.__window.title(string="Password Generator")

        self.__welcome_label = tkinter.ttk.Label(master=self.__window, text="Password Generator",
                                                 font=pw_tool.helper.ui_helper.font,
                                                 background=pw_tool.helper.ui_helper.background_color)

        self.__gen_frame = tkinter.ttk.Frame(master=self.__window, style="TFrame")

        # Get length of password to generate
        self.__pw_len_label = tkinter.ttk.Label(master=self.__gen_frame,
                                                text="Length of password:\n(Minimum length = 12)",
                                                font=pw_tool.helper.ui_helper.small_font,
                                                background=pw_tool.helper.ui_helper.background_color)

        self.__pw_len_entry = tkinter.ttk.Entry(master=self.__gen_frame, font=pw_tool.helper.ui_helper.small_font,
                                                validate="key", validatecommand=(
                                                    self.__gen_frame.register(func=self.digit_validation), "%S"))

        self.__type_label = tkinter.ttk.Label(master=self.__gen_frame, text="Type of characters:",
                                              font=pw_tool.helper.ui_helper.small_font,
                                              background=pw_tool.helper.ui_helper.background_color)

        self.__upper_checkbox = tkinter.ttk.Checkbutton(master=self.__gen_frame, text="Upper Case A-Z",
                                                        style="TCheckbutton")

        self.__lower_checkbox = tkinter.ttk.Checkbutton(master=self.__gen_frame, text="Lower Case a-z",
                                                        style="TCheckbutton")

        self.__numeric_checkbox = tkinter.ttk.Checkbutton(master=self.__gen_frame, text="Numeric 0-9",
                                                          style="TCheckbutton")

        self.__symbol_checkbox = tkinter.ttk.Checkbutton(master=self.__gen_frame, text="!@#$%^&*", style="TCheckbutton")

        # Display Generated Password
        self.__gen_pw_label = tkinter.ttk.Label(master=self.__gen_frame, text="Generated Password:",
                                                font=pw_tool.helper.ui_helper.small_font,
                                                background=pw_tool.helper.ui_helper.background_color)
        self.__gen_pw_label["state"] = tkinter.DISABLED

        self.__pw_label = tkinter.ttk.Label(master=self.__gen_frame, font=pw_tool.helper.ui_helper.small_font,
                                            background=pw_tool.helper.ui_helper.background_color)

        self.__error_frame = tkinter.ttk.Frame(master=self.__window, style="TFrame")

        # Error message if no input
        self.__error_label = tkinter.ttk.Label(master=self.__error_frame, font=pw_tool.helper.ui_helper.small_font,
                                               background=pw_tool.helper.ui_helper.background_color)

        self.__button_frame = tkinter.ttk.Frame(master=self.__window, style="TFrame")

        # Generate password
        self.__generate_button = tkinter.ttk.Button(master=self.__button_frame, text="Generate",
                                                    style="LargeFont.TButton",
                                                    command=self.__pw_generator)

        # copy generated password to clipboard
        self.__copy_button = tkinter.ttk.Button(master=self.__button_frame, text="Copy Password",
                                                style="LargeFont.TButton",
                                                command=lambda: pw_tool.helper.ui_helper.copy_to_clipboard(
                                                    password=self.__password))
        self.__copy_button["state"] = tkinter.DISABLED

        self.__history_frame = tkinter.ttk.Frame(master=self.__window, style="TFrame")

        # view previously generated password
        self.__history_button = tkinter.ttk.Button(master=self.__history_frame, text="Previously Generated Password",
                                                   style="LargeFont.TButton", command=self.__show_hist_page)

        # copied notification
        self.__notif_frame = tkinter.ttk.Frame(master=self.__window, style="TFrame")
        self.__copy_notif_label = tkinter.ttk.Label(master=self.__notif_frame, font=pw_tool.helper.ui_helper.small_font,
                                                    background=pw_tool.helper.ui_helper.background_color)

        self.__pw_len_label.focus()

        self.__pw_len_label.grid(row=0, column=0, padx=20, pady=5, sticky="W")
        self.__pw_len_entry.grid(row=0, column=1, padx=20, pady=5, sticky="W")
        self.__type_label.grid(row=1, column=0, padx=20, pady=5, sticky="W")
        self.__upper_checkbox.grid(row=1, column=1, padx=20, pady=5, sticky="W")
        self.__lower_checkbox.grid(row=1, column=2, padx=20, pady=5, sticky="W")
        self.__numeric_checkbox.grid(row=2, column=1, padx=20, pady=5, sticky="W")
        self.__symbol_checkbox.grid(row=2, column=2, padx=20, pady=5, sticky="W")
        self.__gen_pw_label.grid(row=3, column=0, padx=20, pady=5, sticky="W")
        self.__pw_label.grid(row=3, column=1, columnspan=50, padx=20, pady=5, sticky="W")

        self.__error_label.grid(row=0, column=1, padx=20, pady=5, sticky="E")

        self.__generate_button.grid(row=0, column=0, padx=20, pady=5, sticky="E")
        self.__copy_button.grid(row=0, column=1, padx=20, pady=5, sticky="W")

        self.__history_button.grid(row=0, column=1, padx=20, pady=5, sticky="E")

        self.__copy_notif_label.grid(row=0, column=1, padx=20, pady=5, sticky="E")

        self.__welcome_label.pack(pady=25)
        self.__gen_frame.pack(pady=5)
        self.__error_frame.pack(pady=5)
        self.__button_frame.pack(pady=5)
        self.__history_frame.pack(pady=5)
        self.__notif_frame.pack(pady=5)

        self.__window.protocol(func=lambda: pw_tool.helper.ui_helper.back(root=self.__master, me=self.__window),
                               name="WM_DELETE_WINDOW")

        pw_tool.helper.ui_helper.centre_window(window=self.__window)

    def __pw_generator(self):
        # destroy previously displayed password

        # character list used to combine all the selected characters
        characters = []

        # used to select one character from each list to fulfill selected character requirement
        rand_upper = rand_lower = rand_num = rand_sym = ""
        character_counter = 0

        # used to combine all random characters to create password
        length = self.__pw_len_entry.get()
        upper = self.__upper_checkbox.instate(['selected'])
        lower = self.__lower_checkbox.instate(['selected'])
        num = self.__numeric_checkbox.instate(['selected'])
        sym = self.__symbol_checkbox.instate(['selected'])
        secrets_generator = secrets.SystemRandom()

        if not length or int(length) < 12:
            self.__error_label.configure(text="Please ensure password length is filled/valid!")
            self.__gen_pw_label["state"] = tkinter.DISABLED
            self.__pw_label.configure(text="")
            self.__copy_button["state"] = tkinter.DISABLED
            return

        if not upper and not lower and not num and not sym:
            self.__error_label.configure(text="Please choose the type of characters!")
            self.__gen_pw_label["state"] = tkinter.DISABLED
            self.__pw_label.configure(text="")
            self.__copy_button["state"] = tkinter.DISABLED
            return

        self.__error_label.configure(text="")
        self.__gen_pw_label["state"] = tkinter.NORMAL
        self.__copy_button["state"] = tkinter.NORMAL

        # adding list of selected characters to combined list
        if upper:
            characters += uppercase_list
            rand_upper = secrets_generator.choice(seq=uppercase_list)
            character_counter += 1

        if lower:
            characters += lowercase_list
            rand_lower = secrets_generator.choice(seq=lowercase_list)
            character_counter += 1

        if num:
            characters += numeric_list
            rand_num = secrets_generator.choice(seq=numeric_list)
            character_counter += 1

        if sym:
            characters += symbol_list
            rand_sym = secrets_generator.choice(seq=symbol_list)
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
            return int(binary, 2)

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

        pw_tool.helper.vault_helper.add_gen_pw(password=self.__password)

        # display generated password
        self.__pw_label.configure(text=self.__password)

        def run_test(l, l_median):

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
            stan_dev = math.sqrt((2 * n1 * n2 * (2 * n1 * n2 - n1 - n2)) / (((n1 + n2) ** 2) * (n1 + n2 - 1)))

            z = (runs - runs_exp) / stan_dev

            return z

        l_median = statistics.median(decimal_list)
        z_value = abs(run_test(decimal_list, l_median))

        print('Z-statistic= ', z_value)

        x = statsmodels.sandbox.stats.runs.runstest_1samp(decimal_list, correction=False)
        print(x)

    def digit_validation(self, char):
        """Validates input, making sure it contains only digits
        Rings bell if invalid input.
        """
        if char in numeric_list:
            return True

        self.__gen_frame.bell()
        return False

    def __show_hist_page(self):
        """Redirects to history page
        """
        self.__window.withdraw()
        pw_tool.ui.gen.gen_history.GenHistPage(master=self.__window)
