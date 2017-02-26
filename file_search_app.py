"""
Application to search the file system using a user-specified search expression.
The expression can either use the asterisk (*) wildcard character, or be a regex (regular expression)
"""
import datetime
import basic_combo_dialog
import msgbox
from file_search import *


class App(basic_combo_dialog.BasicComboGUI):
    # inherits from BasicComboGUI
    def __init__(self, title="Search File System", date_picker=False):
        basic_combo_dialog.BasicComboGUI.__init__(self, frame_title=title, date_picker=date_picker)
        self.set_combo_box_label("Select named expression or\nenter custom expression\n(Use wildcard '*' or regex)")
        self.set_combo_box_width(45)
        self.dict_choice = {'Word (doc, docx)': '.+\.docx?$',
                            'Excel (xls, xlsx, xlsb, xlsm)': '.+\.xls(x|b|m)?',
                            'Audio (mp3, wav, au, m4p, etc.)': '.+\.(m4p|cdda|mp3|wma|mp4a|au|ra|flac|cda|wav|m4a)$',
                            'PDF files': '.+\.pdf$',
                            'Visio (vsd, vss, vst, vsx, vdx, vtx)': '.+\.(vs(d|s|t|x)|v(d|t)x)$',
                            'Images (png, gif, jpg, bmp, tif, svg)': '.+\.(png|gif|jpg|bmp|tif|svgx?)$',
                            'Word/Excel/PDF files': '.+\.(xls(x|m|b)?|docx?|pdf)$',
                            'Video (avi, wmv, mpg, mp4, etc.)': '.+\.(avi|wmv|qt|mov|mp(4|e?g|v)|m4p|flv|rm|webm)$',
                            'Numeric file names': '^[0-9_\-\.]+\.(xls(x|m|b)?|docx?|pdf|shp|dbf|shx|xml|'
                                                  'txt|csv|bmp|sql|gif|png|jpg|tif|py|x?html?|vb|cp*)$'}
        lst_choice = list(self.dict_choice.keys())
        self.lst_combo_values = lst_choice
        # self.lst_combo_values = ['.*\.docx',
        #                          '^[0-9_-]+\..*',
        #                          '.*\.xls',
        #                          '.*\.pdf',
        #                          '.*(gw|(ground|grnd).*(water|wtr)).*\.(pdf|xls|doc)',
        #                          '.*\.(png|jpg|gif|bmp)$']
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


if __name__ == "__main__":
    app = App(date_picker=True)
    app.show_window()
