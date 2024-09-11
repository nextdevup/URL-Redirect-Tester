import csv
import pandas as pd
import requests
import tkinter as tk
import tkinter.ttk as ttk
import urllib3

from tkinter import messagebox
from common.extensions import is_empty_string
from common.gui_components import InputRow
from common.io_helper import get_file, get_location_for_save
from common.response_helper import get_domain, get_domain_from_url, get_fixed_url, get_redirect_from_response, ignore_http_to_https_redirects, is_valid_url, make_request
from common.settings_helper import get_max_redirects, get_max_urls

#Ignore warning regarding skipping cert validation
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

window = tk.Tk()
window.title("URL Redirect Tester")
window.resizable(height=False, width=False)

def generate_reports():
    domain = get_domain(domain_row.get_selection_value())
    column_input = column_row.get_selection_value()
    path_input = select_file_row.get_selection_value()

    if worksheet_row.get_selection_value() is None:
        messagebox.showerror("Missing Sheet Selection", "Please select a sheet from the spreadsheet first.")
        return
    
    print(worksheet_row.get_selection_value())
    sheet_input = str(worksheet_row.get_selection_value()).strip()

    if column_input.isdigit():
        url_file = pd.read_excel(path_input, sheet_name=sheet_input, header=None)
        column_name = int(column_input or 0)
    else:
        url_file = pd.read_excel(path_input, sheet_name=sheet_input)
        column_name = str(column_input).strip()

    url_file = url_file.dropna()
    
    paths = url_file[column_name].to_list()

    file_rows = []
    total_redirects = 0

    for path in paths[:get_max_urls()]:
        should_continue = True
        url = get_fixed_url(path, domain)
        urls = []
        urls.append(url)

        while should_continue:
            resp = make_request(url)

            if resp.is_redirect or resp.is_permanent_redirect or resp.status_code in {301, 302, 303, 307, 308}:
                if is_empty_string(domain):
                    domain = get_domain_from_url(url)

                url = get_redirect_from_response(resp, domain)

                if not is_valid_url(url):
                    should_continue = False
                elif url in urls:
                    url = f'Possible Infinite Redirect -- Ending Loop -- {url}'
                    should_continue = False
                elif len(urls) > get_max_redirects():
                    url = f'Max Redirects Reached -- {url}'
                    should_continue = False
            elif ('Strict-Transport-Security' in resp.headers or resp.headers.get('Non-Authoritative-Reason') == 'HSTS') and not ignore_http_to_https_redirects():
                # Check for HSTS headers because request may not indicate the redirect here but 
                # the browser would force the redirect to https
                url = url.replace('http://', 'https://')
            else:
                url = f'No Redirect -- Status Code: {resp.status_code}'
                should_continue = False

            urls.append(url)

        if len(urls) >= total_redirects:
            total_redirects = len(urls)

        # Pass urls as an array or else it will split each character into a column
        file_rows.extend([urls])

    header_row = ['input_url']

    for i in range(1, total_redirects):
        header_row.append(f'redirect_{i}')

    file_rows.insert(0, header_row)

    with open(select_output_location.get_selection_value(), "w", newline='') as results_file:
        csv_writer = csv.writer(results_file)
        print(file_rows)
        csv_writer.writerows(file_rows)



lbl_top = ttk.Label(text="URL Redirect Tester")

btn_submit = ttk.Button(
    text="Generate Report",
    width=25,
    command=generate_reports
)

window.columnconfigure([0, 1, 2], weight=1)
window.rowconfigure([0, 1, 2], weight=0, minsize=25)

lbl_top.grid(row=0, column=0, padx=5, pady=5)

select_file_row = InputRow(window, 1, "Select File:", get_file, popup_options=None)
domain_row = InputRow(window, 2, "Enter Domain (if not in URLs):", btn_method=None, popup_options=None)
worksheet_row = InputRow(window, 3, "Select Worksheet:", btn_method=None, popup_options=select_file_row.get_excel_sheet_names)
column_row = InputRow(window, 4, "Select Column:", btn_method=None, popup_options=select_file_row.get_column_names)
select_output_location = InputRow(window, 5, "Save Results To:", get_location_for_save, popup_options=None)
btn_submit.grid(row=6, column=0, padx=5, pady=5)

window.mainloop()