import tkinter.ttk

import pw_tool.helper.ui_helper


class GenPage:
    def __init__(self, master):
        self.__master = master

        self.__window = tkinter.Toplevel()
        self.__window.geometry(newGeometry="640x480")
        self.__window.title(string="Password Generator")

        # Get length of password to generate
        plength_label = tkinter.ttk.Label(master=self.__window, text="Length of password:", font=("Arial", 12))
        plength_label.grid(row=0, column=0, padx=10)

        plength_entry = tkinter.ttk.Entry(master=self.__window, font=("Arial", 12))
        plength_entry.grid(row=0, column=1)

        # Get type of characters to include in password
        ptype_label = tkinter.ttk.Label(master=self.__window, text="Type of characters:", font=("Arial", 12))
        ptype_label.grid(row=1, column=0, padx=10)

        ptype1_cbox = tkinter.ttk.Checkbutton(master=self.__window, text="Upper Case A-Z")
        ptype1_cbox.grid(row=1, column=1)

        ptype2_cbox = tkinter.ttk.Checkbutton(master=self.__window, text="Lower Case a-z")
        ptype2_cbox.grid(row=1, column=2)

        ptype3_cbox = tkinter.ttk.Checkbutton(master=self.__window, text="Numeric 0-9")
        ptype3_cbox.grid(row=2, column=1)

        ptype4_cbox = tkinter.ttk.Checkbutton(master=self.__window, text="!@#$%^&*")
        ptype4_cbox.grid(row=2, column=2)

        # Generate password
        generate_button = tkinter.ttk.Button(master=self.__window, text="Generate", style="TButton",
                                             command=self.__pgenerator)
        generate_button.grid(row=3, column=1)

        pw_tool.helper.ui_helper.centre_window(window=self.__window)

        self.__window.protocol(
            func=lambda root=master, window=self.__window: pw_tool.helper.ui_helper.back(root=master, me=self.__window),
            name="WM_DELETE_WINDOW")

    def __pgenerator(self):
        print("bIJ")
