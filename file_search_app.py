"""
Application to search the file system using a user-specified search expression.
The expression can either use the asterisk (*) wildcard character, or be a regex (regular expression)
"""
import os
import datetime
import basic_combo_dialog
from file_search import *
import webbrowser


class App(basic_combo_dialog.BasicComboGUI):
    # inherits from BasicComboGUI
    def __init__(self, title="Search File System", date_picker=False):
        basic_combo_dialog.BasicComboGUI.__init__(self, frame_title=title, date_picker=date_picker)
        self.set_combo_box_label("Select named expression or\nenter custom expression\n(Use wildcard '*' or regex)")
        self.set_combo_box_width(45)

        # read named expressions from file_search.config
        fn = os.path.join(os.getcwd(), 'file_search.config')
        self.dict_choice = configsectionmap(fn, 'named expressions')
        self.regex_url = configsectionmap(fn, 'regex url')
        lst_choice = list(self.dict_choice.keys())
        self.lst_combo_values = lst_choice
        self.lst_combo_values.sort()
        self.combo_box['values'] = self.lst_combo_values
        if self.date_picker:
            self.selected_date_start.set('01/01/1900')
            self.selected_date_end.set(datetime.date.today().strftime('%m/%d/%Y'))
        # self.root.bind('<Return>', self.okclick)
        # self.combo_box.current(0)

    def okclick(self):
        # override click event
        if self.date_picker:
            try:
                dt1 = datetime.datetime.strptime(self.selected_date_start.get(), '%m/%d/%Y').strftime('%Y-%m-%d')
                dt2 = datetime.datetime.strptime(self.selected_date_end.get(), '%m/%d/%Y').strftime('%Y-%m-%d')
            except ValueError:
                msgbox.show_error('Value Error', 'Date format is mm/dd/yyyy')
                # raise ValueError('Date format is mm/dd/yyyy')
        else:
            dt1 = None
            dt2 = None

        if self.chk_val.get():
            try:
                search_dir_only(self.dict_choice[self.entered_value.get()], 'search_results')
            except KeyError:
                search_dir_only(self.entered_value.get(), 'search_results')
        else:
            try:
                search_dir_topdown(self.dict_choice[self.entered_value.get()], 'search_results', dt1, dt2)
            except KeyError:
                search_dir_topdown(self.entered_value.get(), 'search_results', dt1, dt2)

    def callback(self, event):
        webbrowser.open_new(self.regex_url['cheatsheet'])

if __name__ == "__main__":
    app = App(date_picker=True)
    app.show_window()
