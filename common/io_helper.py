import pandas as pd
import tkinter.filedialog

def get_file(set_value_method):
    file_types = (
        ('Excel Worksheet', '*.xlsx'),
        ('All files', '*.*')
    )

    file_path = tkinter.filedialog.askopenfilename(
        filetypes=file_types,
        initialdir='/',
        title='Open a file'
    )

    set_value_method(str(file_path).strip())

def get_location_for_save(set_value_method):
    file_types = [('CSV', '*.csv')]

    file_path = tkinter.filedialog.asksaveasfilename(
        confirmoverwrite=True,
        defaultextension=file_types,
        filetypes=file_types,
        initialdir='/',
        initialfile='Results',
        title='Select Save Location'
    )

    set_value_method(str(file_path).strip())