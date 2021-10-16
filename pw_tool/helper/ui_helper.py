import tkinter
import tkinter.ttk


def centre_window(window):
    """Centres main window given 'window'
    Function centre_window(window) centres the given 'window' by taking into account main window geometry and screen
    geometry. winfo_screenwidth(), winfo_screenheight(), winfo_width(), winfo_height() are used. The main window is
    hidden using withdraw() then displayed again using deiconify().
    """

    # Hide window
    window.withdraw()

    # Update
    window.update_idletasks()

    # Calculations to centre the window
    x = (window.winfo_screenwidth() - max(window.winfo_width(), window.winfo_reqwidth())) / 2
    y = (window.winfo_screenheight() - max(window.winfo_height(), window.winfo_reqheight())) / 2
    window.geometry(newGeometry="+%d+%d" % (x, y))

    # Show window
    window.deiconify()


def back(root, me):
    """Goes Back to main page, given 'root' and 'me'.
    Function back(root,me) takes in 'root' and 'me', destroys 'me' and shows 'root'
    """

    me.destroy()
    root.deiconify()


def create_button_style():
    style = tkinter.ttk.Style()
    style.configure(style="TButton", font=("Arial", 25))


def create_frame_style():
    style = tkinter.ttk.Style()
    style.configure(style="TFrame", background="SystemButtonFace")

def clear_fields(window):
    for widget in window.winfo_children():
        if type(widget) == tkinter.ttk.Entry:
            widget.delete(first=0, last=tkinter.END)
