import tkinter
import tkinter.ttk

import pw_tool.helper.firebase_helper
import pw_tool.helper.ui_helper
import pw_tool.helper.vault_helper
import pw_tool.ui.vault.add_page
import pw_tool.ui.vault.delete_dialog
import pw_tool.ui.vault.edit_page
import pw_tool.ui.vault.gen_page


class PWPage:
    def __init__(self, master, website, value):
        self.__master = master
        self.__master.withdraw()

        self.__website = website
        self.__value = value

        self.__window = tkinter.Toplevel()
        self.__window.geometry(newGeometry="640x480")
        self.__window.title(string="Password Manager")

        self.__welcome_label = tkinter.ttk.Label(master=self.__window, text="Be careful of prying eyes",
                                                 font=pw_tool.helper.ui_helper.font,
                                                 background=pw_tool.helper.ui_helper.background_color)
        self.__welcome_label.pack(pady=30)

        self.__website_label = tkinter.ttk.Label(master=self.__window, text=self.__website,
                                                 font=pw_tool.helper.ui_helper.font,
                                                 background=pw_tool.helper.ui_helper.background_color)
        self.__website_label.pack(pady=5)

        self.__label_frame = tkinter.ttk.Frame(master=self.__window, style="TFrame")
        self.__username_label = tkinter.ttk.Label(master=self.__label_frame, text="Username:",
                                                  font=pw_tool.helper.ui_helper.font,
                                                  background=pw_tool.helper.ui_helper.background_color)
        self.__actual_username_label = tkinter.ttk.Label(master=self.__label_frame, text=self.__value["username"],
                                                         font=pw_tool.helper.ui_helper.font,
                                                         background=pw_tool.helper.ui_helper.background_color)
        self.__password_label = tkinter.ttk.Label(master=self.__label_frame, text="Password:",
                                                  font=pw_tool.helper.ui_helper.font,
                                                  background=pw_tool.helper.ui_helper.background_color)
        self.__actual_password_label = tkinter.ttk.Label(master=self.__label_frame, text=self.__value["password"],
                                                         font=pw_tool.helper.ui_helper.font,
                                                         background=pw_tool.helper.ui_helper.background_color)

        self.__username_label.grid(row=0, column=0, padx=20, pady=5, sticky="E")
        self.__actual_username_label.grid(row=0, column=1, padx=20, pady=5, sticky="E")
        self.__password_label.grid(row=1, column=0, padx=20, pady=5, sticky="E")
        self.__actual_password_label.grid(row=1, column=1, padx=20, pady=5, sticky="E")
        self.__label_frame.pack(pady=5)

        self.__button_frame = tkinter.ttk.Frame(master=self.__window, style="TFrame")

        self.__edit_button = tkinter.ttk.Button(master=self.__button_frame, text="Edit", style="TButton",
                                                command=self.__show_edit_page)

        self.__delete_button = tkinter.ttk.Button(master=self.__button_frame, text="Delete", style="TButton",
                                                  command=self.__show_delete_dialog)

        self.__edit_button.grid(row=0, column=0, padx=20, pady=5, sticky="E")
        self.__delete_button.grid(row=0, column=1, padx=20, pady=5, sticky="W")

        self.__button_frame.pack(pady=30)

        self.__window.protocol(func=lambda: pw_tool.helper.ui_helper.back(root=self.__master, me=self.__window),
                               name="WM_DELETE_WINDOW")

        pw_tool.helper.ui_helper.centre_window(window=self.__window)

    def __show_edit_page(self):
        self.__window.destroy()
        pw_tool.ui.vault.edit_page.EditPage(master=self.__master, website=self.__website, value=self.__value)

    def __show_delete_dialog(self):
        self.__window.destroy()
        pw_tool.ui.vault.delete_dialog.DeleteDialog(master=self.__master, website=self.__website)
