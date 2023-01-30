"""
Application to search the file system using a user-specified search expression.
The expression can either use the asterisk (*) wildcard character, or be a regex (regular expression)
"""
import os
import datetime
import basic_combo_dialog
from file_search import *
import webbrowser
import utility_functions as uf
import uuid
import logger_handler


class App(basic_combo_dialog.BasicComboGUI):
    # inherits from BasicComboGUI
    def __init__(self, title="Search File System", date_picker=False):
        self.logger_debug = logger_handler.setup_logger(name='logger_debug', log_file=os.path.join(os.getcwd(),'debug.log'))
        self.logger_exception = logger_handler.setup_logger(name='logger_exception', log_file=os.path.join(os.getcwd(),'error.log'))
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
        try:
            # used search_results.xlsx previously for the file name. now using uuid.
            # check to see if search_results.xlsx is already open
            open_excel_files = uf.get_opened_files(['xlsx', 'xlsm'])
            if 'search_results.xlsx' in [os.path.split(el)[1] for el in open_excel_files]:
                raise PermissionError('search_results.xlsx already open.\n\n'
                                      'Please close or rename file and try again.')
            # get uuid for file name
            file_name = str(uuid.uuid4())
            self.logger_debug.info(file_name)
            if self.date_picker:
                try:
                    dt1 = datetime.datetime.strptime(self.selected_date_start.get(), '%m/%d/%Y').strftime('%Y-%m-%d')
                    dt2 = datetime.datetime.strptime(self.selected_date_end.get(), '%m/%d/%Y').strftime('%Y-%m-%d')
                except ValueError:
                    msgbox.show_error('Value Error', 'Date format is mm/dd/yyyy')
                    raise Exception('')
            else:
                dt1 = None
                dt2 = None

            if self.chk_val.get():
                try:
                    search_dir_only(self.dict_choice[self.entered_value.get()], filename=file_name)
                except KeyError:
                    search_dir_only(self.entered_value.get(), filename=file_name)
            else:
                try:
                    search_dir_topdown(self.dict_choice[self.entered_value.get()], file_name, dt1, dt2)
                except KeyError:
                    search_dir_topdown(self.entered_value.get(), file_name, dt1, dt2)
                except Exception as e:
                    self.logger_exception('error in search_dir_topdown')
        except PermissionError as e:
            msgbox.show_error('Can\'t do what you\'re trying to do...', e)
        except Exception as e:
            self.logger_exception.exception('error in click event')
            if len(e.args[0]) > 0:
                msgbox.show_error('Error', e)

    def callback(self, event):
        webbrowser.open_new(self.regex_url['cheatsheet'])

if __name__ == "__main__":
    app = App(date_picker=True)
    app.show_window()
