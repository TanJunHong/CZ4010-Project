import tkinter.ttk

vault_page = None
background_color = "SystemButtonFace"
font = ("Arial", 25)
window_size = "640x480"


def centre_window(window):
    """Centres main window given 'window'
    Function centre_window(window) centres the given 'window' by taking into account main window geometry and screen
    geometry. winfo_screenwidth(), winfo_screenheight(), winfo_width(), winfo_height() are used. The main window is
    hidden using withdraw() then displayed again using deiconify().
    """
    window.withdraw()

    window.update_idletasks()

    x = (window.winfo_screenwidth() - max(window.winfo_width(), window.winfo_reqwidth())) / 2
    y = (window.winfo_screenheight() - max(window.winfo_height(), window.winfo_reqheight())) / 2
    window.geometry(newGeometry="+%d+%d" % (x, y))
    window.deiconify()


def back(root, me):
    """Goes Back to main page, given 'root' and 'me'
    Function back(root,me) takes in 'root' and 'me', destroys 'me' and shows 'root'
    """
    me.destroy()
    root.deiconify()


def create_button_style():
    """Creates button style
    """
    style = tkinter.ttk.Style()
    style.configure(style="TButton", font=font)


def create_frame_style():
    """Creates frame style
    """
    style = tkinter.ttk.Style()
    style.configure(style="TFrame", background=background_color)


def clear_fields(window):
    """Clears fields of window
    Finds all entry fields of window and clear it of values.
    """
    for widget in window.winfo_children():
        if type(widget) == tkinter.ttk.Entry:
            widget.delete(first=0, last=tkinter.END)


def destroy_children(window):
    """Destroys children of window
    """
    for widgets in window.winfo_children():
        widgets.destroy()
