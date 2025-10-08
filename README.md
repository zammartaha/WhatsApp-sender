#### WhatsApp Sender — Quick Setup (Windows)

1. ##### Install Python

Download and install Python: https://www.python.org/downloads/

During setup, check “Add Python to PATH.”

2. ##### Install required libraries

Double-click install\_libs.bat, or run:

pip install selenium python-dotenv pandas openpyxl xlrd

3. ##### Set up ChromeDriver \& WhatsApp session

Find your exact Chrome version: open Chrome → chrome://settings/help.

Download the matching ChromeDriver from:
https://googlechromelabs.github.io/chrome-for-testing/

For Windows, choose “chromedriver win64.”

Move chromedriver.exe to:

C:\\webdriver\\



Press Win + R, then run:

chrome.exe --user-data-dir="C:\\selenium\\chrome-profile" --profile-directory="Default"



Go to https://web.whatsapp.com/
and log in.

Close Chrome.



##### Default filenames (you can use these out of the box)

Excel file: excel.xlsx

Sheet name: Sheet1

First column header: Numbers

Message file: message.txt

Log file: failed\_numbers.log



If you want to customize any of these, create a .env file (in the same folder as send\_txt.py) and edit the values.



Example .env

=============================

WhatsApp Automation Settings

=============================

\#Path to your Excel file with phone numbers

EXCEL\_FILE=excel.xlsx

\#Name of the sheet in the Excel workbook

SHEET\_NAME=Sheet1

\#Column header of the first column containing phone numbers

FIRST\_ROW\_NAME=Numbers

\#Text file containing the message to send

MESSAGE\_FILE=message.txt

\#Path to save the log file for failed numbers

LOG\_FILE=failed\_numbers.log

\#Path to your Chrome WebDriver executable

CHROME\_DRIVER\_DIR=C:\\webdriver\\chromedriver.exe

\#Directory of your saved Chrome user profile (used for WhatsApp Web session)

CHROME\_PROFILE\_DIR=C:\\selenium\\chrome-profile

\#Name of your Chrome profile (Default, Profile 1, etc.)

CHROME\_PROFILE\_NAME=Default



4. ##### Run the script

Put your message inside message.txt.

Either double-click run.bat or run:

python send\_txt.py



###### Tips \& common issues

File not found? Make sure paths in .env exist (use your actual Windows username/path).

Excel read error? Confirm the sheet name (SHEET\_NAME) and header (FIRST\_ROW\_NAME) match your file.

WhatsApp search not found? Ensure you’re logged in (step 3) and the DOM hasn’t changed.

Chrome version mismatch? Re-download ChromeDriver that matches your Chrome version exactly.



**Good luck!**
Questions / issues: github.com/zammartaha

