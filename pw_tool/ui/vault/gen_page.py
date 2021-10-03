import tkinter.ttk
from tkinter import IntVar
import pw_tool.helper.ui_helper


class GenPage:
    def __init__(self, master):
        self.__master = master

        self.__window = tkinter.Toplevel()
        self.__window.geometry(newGeometry="640x480")
        self.__window.title(string="Password Generator")

        # Get length of password to generate
        self.__plength_label = tkinter.ttk.Label(master=self.__window, text="Length of password:", font=("Arial", 12))
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

        self.__ptype1_cbox = tkinter.ttk.Checkbutton(master=self.__window, text="Upper Case A-Z", variable=self.__var_upper)
        self.__ptype1_cbox.grid(row=1, column=1)

        self.__ptype2_cbox = tkinter.ttk.Checkbutton(master=self.__window, text="Lower Case a-z", variable=self.__var_lower)
        self.__ptype2_cbox.grid(row=1, column=2)

        self.__ptype3_cbox = tkinter.ttk.Checkbutton(master=self.__window, text="Numeric 0-9", variable=self.__var_numeric)
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

        pw_tool.helper.ui_helper.centre_window(window=self.__window)

        self.__window.protocol(
            func=lambda root=master, window=self.__window: pw_tool.helper.ui_helper.back(root=master, me=self.__window),
            name="WM_DELETE_WINDOW")

    def __pgenerator(self):
        lowercase_list = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's',
                          't', 'u', 'v', 'w', 'x', 'y', 'z']
        uppercase_list = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S',
                          'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
        numeric_list = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        symbol_list = ['!', '@', '#', '$', '%', '^', '&', '*']

        characters = []
        length = self.__plength_entry.get()
        upper = self.__var_upper.get()
        lower = self.__var_lower.get()
        num = self.__var_numeric.get()
        sym = self.__var_symbol.get()

        i = 0
        while i == 0:
            if not length or int(length) <= 0:
                self.__error_label.config(text="Please ensure all fields are filled!")
                return
            else:
                if not upper and not lower and not num and not sym:
                    self.__error_label.config(text="Please ensure all fields are filled!")
                    return
                else:
                    self.__window.after(0, lambda: self.__error_label.config(text=""))
                    break

        if upper == 1:
            characters += uppercase_list
        if lower == 1:
            characters += lowercase_list
        if num == 1:
            characters += numeric_list
        if sym == 1:
            characters += symbol_list

        self.__password_label = tkinter.ttk.Label(master=self.__window, text="Generated Password:", font=("Arial", 12))
        self.__password_label.grid(row=5, column=0, padx=10)

        # copy generated password to clipboard
        self.__copy_button = tkinter.ttk.Button(master=self.__window, text="Copy Password", style="TButton",
                                                command=self.__pcopy)
        self.__copy_button.grid(row=7, column=1)

        print(characters)
        print(length)
        print(len)
        print(type(len))

    def __pcopy(self):
        print("wuwu")
