try:
    import Tkinter as tk
    import tkMessageBox as tkmb
except ImportError:
    import tkinter as tk
    from tkinter import messagebox as tkmb


def show_error(title, message):
    root = tk.Tk()
    root.withdraw()
    tkmb.showerror(title=title, message=message)


def show_message(title, message):
    root = tk.Tk()
    root.withdraw()
    tkmb.showinfo(title=title, message=message)

if __name__ == '__main__':
    show_error('mytitle', 'mymessage')
    show_message('mytitle', 'mymessage')
