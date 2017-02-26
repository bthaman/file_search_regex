try:
    import Tkinter as tk
    import ttk
except ImportError:
    # python 3
    import tkinter as tk
    from tkinter import ttk
import ttkcalendar
import datetime
import tkSimpleDialog
import webbrowser


class CalendarDialog(tkSimpleDialog.Dialog):
    """Dialog box that displays a calendar and returns the selected date"""
    def body(self, master):
        self.calendar = ttkcalendar.Calendar(master)
        self.calendar.pack()

    def apply(self):
        self.result = self.calendar.selection


class BasicComboGUI(ttk.LabelFrame):
    def __init__(self, frame_title, date_picker=False):
        self.root = tk.Tk()
        self.root.wm_title(frame_title)
        ttk.LabelFrame.__init__(self, self.root, text=None)
        self.padding = '6, 6, 12, 12'
        self.grid(column=0, row=0)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.date_picker = date_picker
        self.selected_date_start = tk.StringVar()
        self.selected_date_start.trace('w', self.handle_event)
        self.selected_date_end = tk.StringVar()
        self.selected_date_end.trace('w', self.handle_event)
        self.entered_value = tk.StringVar()
        self.entered_value.trace('w', self.handle_event)
        self.chk_val = tk.IntVar()
        self.chk_val.trace('w', self.handle_event)
        self.lst_combo_values = ['Choice 1', 'Choice 2', 'Choice3']

        # create 'OK' button and bind it to the okclick function using the command param
        self.btn_ok = ttk.Button(self, text='OK', width=7, command=self.okclick)
        # bind the return (enter) key to the okclick event
        # self.root.bind('<Return>', self.okclick)

        # since this is a parent window, call the quit method when the window is closed
        # by clicking the 'x' in the upper right
        self.root.protocol('WM_DELETE_WINDOW', self.quit)

        self.set_combo_box_label('Change me')
        self.combo_box = ttk.Combobox(self, textvariable=self.entered_value, width=12)
        self.hyperlink = ttk.Label(self, text='regex cheatsheet', foreground='blue', cursor='hand2')
        self.hyperlink.bind("<Button-1>", self.callback)
        self.chk_box = ttk.Checkbutton(self, text='Search only directory names',
                                       variable=self.chk_val)

        self.combo_box.grid(column=2, row=1, sticky='E')
        self.hyperlink.grid(column=1, row=2, sticky='N')
        self.chk_box.grid(column=2, row=2, sticky='W')
        self.btn_ok.grid(row=6, columnspan=3)
        self.btn_ok.configure(state='disabled', cursor='')

        self.combo_box['values'] = self.lst_combo_values

        if date_picker:
            self.add_date_controls()

        # put space around the widgets
        for child in self.winfo_children():
            child.grid_configure(padx=5, pady=5)

    def add_date_controls(self):
        self.txt_date = ttk.Entry(self, textvariable=self.selected_date_start, width=15)
        self.btn_choose_date_start = ttk.Button(self, text="Choose start date", command=self.getdatestart, width=18)
        self.btn_choose_date_start.grid(column=1, row=3)
        self.txt_date.grid(column=2, row=3, sticky='W')
        self.txt_date_end = ttk.Entry(self, textvariable=self.selected_date_end, width=15)
        self.btn_choose_date_end = ttk.Button(self, text="Choose end date", command=self.getdateend, width=18)
        self.btn_choose_date_end.grid(column=1, row=4)
        self.txt_date_end.grid(column=2, row=4, sticky='W')

    def getdatestart(self):
        cd = CalendarDialog(self)
        result = cd.result
        if result:
            self.selected_date_start.set(result.strftime("%m/%d/%Y"))

    def getdateend(self):
        cd = CalendarDialog(self)
        result = cd.result
        if result:
            self.selected_date_end.set(result.strftime("%m/%d/%Y"))

    def okclick(self):
        # click event for btn_ok. this should be overridden by any superclass
        # need 'event' as a parameter if binding the Return key, and the event is passed
        try:
            if self.entered_value.get() not in self.lst_combo_values:
                raise ValueError
        except ValueError:
            raise ValueError('value not in list')
        try:
            datetime.datetime.strptime(self.selected_date_start.get(), '%m/%d/%Y')
            print(datetime.datetime.strptime(self.selected_date_start.get(), '%m/%d/%Y').strftime('%Y-%m-%d'))
        except ValueError:
            raise ValueError('Date format is mm/dd/yyyy')
            pass
        print(self.entered_value.get())

    def handle_event(self, *args):
        x = self.selected_date_start.get()
        x2 = self.selected_date_end.get()
        y = self.entered_value.get()

        if self.date_picker and self.chk_val.get():
            self.txt_date.configure(state='disabled')
            self.txt_date_end.configure(state='disabled')
            self.btn_choose_date_start.configure(state='disabled')
            self.btn_choose_date_end.configure(state='disabled')
        elif self.date_picker and not self.chk_val.get():
            self.txt_date.configure(state='normal')
            self.txt_date_end.configure(state='normal')
            self.btn_choose_date_start.configure(state='normal')
            self.btn_choose_date_end.configure(state='normal')

        if self.date_picker:
            if x and x2 and y:
                self.btn_ok.configure(state='normal')
            else:
                self.btn_ok.configure(state='disabled')
        else:
            if y:
                self.btn_ok.configure(state='normal')
            else:
                self.btn_ok.configure(state='disabled')

    def callback(self, event):
        webbrowser.open_new(r'https://www.debuggex.com/cheatsheet/regex/python')

    def get_durations(self):
        return self.lst_combo_values

    def set_combo_box_label(self, labeltext):
        ttk.Label(self, text=labeltext).grid(column=1, row=1, sticky='W')

    def set_combo_box_width(self, cb_width):
        self.combo_box.configure(width=cb_width)

    def show_window(self):
        self.root.mainloop()

    def quit(self):
        # if root.quit isn't called, the window will close, but will leave the python.exe process running
        # if there are any child windows (e.g. file/dir dialog that didn't close with root.quit.
        # calling root.destroy() will not kill the process
        self.root.quit()


if __name__ == "__main__":
    gui = BasicComboGUI(frame_title='Change Me', date_picker=True)
    gui.show_window()
