import tkinter.ttk
from functools import partial

import pw_tool.helper.firebase_helper
import pw_tool.helper.ui_helper


class DeletePage:
    def __init__(self, master):
        self.__master = master

        self.__window = tkinter.Toplevel()
        self.__window.geometry(newGeometry="640x480")
        self.__window.title(string="Delete Item")

        self.__website_label = tkinter.ttk.Label(master=self.__window, text="Website", background="SystemButtonFace")
        self.__website_label.grid(row=2, column=0, padx=80)

        self.__username_label = tkinter.ttk.Label(master=self.__window, text="Username", background="SystemButtonFace")
        self.__username_label.grid(row=2, column=1, padx=80)

        self.__password_label = tkinter.ttk.Label(master=self.__window, text="Password", background="SystemButtonFace")
        self.__password_label.grid(row=2, column=2, padx=80)

        # pw_tool.helper.firebase_helper.cursor.execute("SELECT website, username, password FROM password_vault")
        if True:  # pw_tool.helper.firebase_helper.cursor.fetchall() is not None:
            i = 0
            while True:
                # pw_tool.helper.firebase_helper.cursor.execute("SELECT website, username,password FROM password_vault")
                # array = pw_tool.helper.firebase_helper.cursor.fetchall()
                self.__website_label1 = tkinter.ttk.Label(master=self.__window, text=(array[i][0]), font=("Arial", 12),
                                                          background="SystemButtonFace")
                self.__website_label1.grid(column=0, row=(i + 3))

                self.__username_label2 = tkinter.ttk.Label(master=self.__window, text=(array[i][1]), font=("Arial", 12),
                                                           background="SystemButtonFace")
                self.__username_label2.grid(column=1, row=(i + 3))

                self.__password_label3 = tkinter.ttk.Label(master=self.__window, text=(array[i][2]), font=("Arial", 12),
                                                           background="SystemButtonFace")
                self.__password_label3.grid(column=2, row=(i + 3))

                delete_btn = tkinter.ttk.Button(master=self.__window, text="Delete",
                                                command=partial(self.__delete_from_vault, array[i][0]))
                delete_btn.grid(column=3, row=(i + 3), pady=10)

                i = i + 1
                # pw_tool.helper.firebase_helper.cursor.execute("SELECT website, username, password FROM password_vault")
                # if len(pw_tool.helper.firebase_helper.cursor.fetchall()) <= i:
                break
        pw_tool.helper.ui_helper.centre_window(self.__window)

        self.__window.protocol(
            func=lambda root=master, window=self.__window: pw_tool.helper.ui_helper.back(root=master, me=self.__window),
            name="WM_DELETE_WINDOW")

    def __delete_from_vault(self):
        # pw_tool.helper.firebase_helper.cursor.execute("DELETE FROM password_vault WHERE id =?", input)
        # pw_tool.helper.firebase_helper.db.commit()

        self.__window.after(1000, lambda: pw_tool.helper.ui_helper.back(root=self.__master, me=self.__window))
