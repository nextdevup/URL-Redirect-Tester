
# URL Redirect Tester

Python application that accepts an Excel file of URLs and outputs any redirects that occurred.




## Dependencies
To run this application you will need to have Python installed.

## Executing Program

1. The application currently has to be run using a terminal in the root folder and calling the command below

    ```python main.py```
2. Use the select file option to choose an Excel Worksheet (currently, only .xlsx files are allowed).
3. For the Enter Domain field, this is the domain that will be used if your excel file contains paths only.
4. You will have options to select the sheet and column that contains the URLs you wish to test.
5. Choose where to save the results (will save as a .csv file)

## Settings

Please review the settings.INI file if you'd like to change the application defaults, such as, the max number of URLs to test and what User Agent to use.

