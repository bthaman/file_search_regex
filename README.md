# regex_file_search
Python application to search the file system using either a wildcard character (*), an ad hoc regular expression, or a named regular expression. The user can enter an expression directly through the pulldown, or select from pre-defined named expressions (e.g., Word files (.doc, .docx)) stored in a config file. The interface contains a hyperlink to https://pythex.org/ if the user needs a refresher on regular expressions. Default is all file modified dates, but the user can also filter by dates. 

The results of the search are written to an MS Excel file, and the file is automatically opened after results are written. Results include directory, filename, file extension, filesize, and last modified date. The directory and filename are written as hyperlinks.

### Prerequisites
The files included in this repo were only tested in Python 3.6.1. 
The only package not in the standard library is pandas (0.20.1).

The minimum version of pandas can be installed using pip. For example:
```
pip install pandas>=0.20.1
```
## Built With

* [Python 3.6.1 |Anaconda 4.4.0 (32-bit)](https://www.anaconda.com/) - The Python interpreter used

## Running the Application
The application is launched by executing *file_search_app.py*.
* **Using an ad hoc regex expression**
![sample image](https://raw.githubusercontent.com/bthaman/file_search_regex/master/images/search_file_system.jpg)

* **Using a named expression read from file_search.config**
![sample image](https://raw.githubusercontent.com/bthaman/file_search_regex/master/images/search_file_system2.jpg)

* **Using the date picker**
![sample image](https://raw.githubusercontent.com/bthaman/file_search_regex/master/images/date_picker.jpg)

### Output
![sample image](https://raw.githubusercontent.com/bthaman/file_search_regex/master/images/file_search_output.jpg)

## Author

* **Bill Thaman** - *Initial work* - [bthaman/file_search_regex](https://github.com/bthaman/file_search_regex)