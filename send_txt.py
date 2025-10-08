from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from dotenv import load_dotenv
from pathlib import Path
import pandas as pd
import time
import sys
import os

load_dotenv()

# filenames from .env (fall back to previous defaults)
excel_file = os.getenv("EXCEL_FILE", "excel.xlsm")
sheet_name = os.getenv("SHEET_NAME", "phone_numbers")
first_row_name = os.getenv("FIRST_ROW_NAME", "Numbers")
message_file = os.getenv("MESSAGE_FILE", "message.txt")
log_file = os.getenv("LOG_FILE", "failed_numbers.log")
chrome_driver_dir = os.getenv("CHROME_DRIVER_DIR", r"C:\webdriver\chromedriver.exe")
chrome_profile_dir = os.getenv("CHROME_PROFILE_DIR", r"C:\selenium\chrome-profile")
chrome_profile_name = os.getenv("CHROME_PROFILE_NAME", "Default")

# Ensure paths are safe
excel_file = Path(excel_file)
message_file = Path(message_file)
log_file = Path(log_file)
chrome_driver_dir = Path(chrome_driver_dir)

# Load the Excel file
data = pd.read_excel(excel_file, sheet_name=sheet_name)

try:
    with open(message_file, 'r', encoding='utf-8') as file:
        message = file.read()
except FileNotFoundError:
    print(f"❌ Error: The '{message_file}' file was not found.")
    sys.exit(1)

# Chrome options (use saved WhatsApp session)
options = Options()
options.add_argument(f"user-data-dir={chrome_profile_dir}")
options.add_argument(f"profile-directory={chrome_profile_name}")

service = Service(str(chrome_driver_dir))
driver = webdriver.Chrome(service=service, options=options)
driver.get("https://web.whatsapp.com/")
wait = WebDriverWait(driver, 60)
time.sleep(10)

# Prepare error logging
failed_numbers = []

# Clear old log file
with open(log_file, "w", encoding="utf-8") as f:
    f.write("Failed WhatsApp Numbers Log\n")
    f.write("="*40 + "\n\n")

# Iterate through the Excel data
for index, row in data.iterrows():
    phone_number = str(row[first_row_name]).strip()
    try:
        new_chat = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@title='New chat']")))
        new_chat.click()

        search_field = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@aria-label='Search name or number']")))
        search_field.clear()
        search_field.send_keys(phone_number)
        print(f"Processing: {phone_number}")
        time.sleep(1)
        search_field.send_keys(Keys.ENTER)

        time.sleep(1)

        text_field = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[starts-with(@aria-label, 'Type to')]")))
        text_field.clear()

        # Split the message by newlines and send each part with Shift+Enter
        for line in message.splitlines():
            text_field.send_keys(line)
            text_field.send_keys(Keys.SHIFT + Keys.ENTER)

        time.sleep(1)
        text_field.send_keys(Keys.ENTER)

        time.sleep(1)

    except Exception as e:
        error_msg = f"Failed for {phone_number}: {e}"
        print(error_msg)
        failed_numbers.append(phone_number)

        # Append to log file immediately
        with open(log_file, "a", encoding="utf-8") as f:
            f.write(error_msg + "\n")

# Close the browser
time.sleep(2)
driver.quit()

# Display failed numbers at the end
if failed_numbers:
    print("\n❌ The following numbers failed:")
    for num in failed_numbers:
        print(num)
    print(f"\n(Also logged to {log_file})")
else:
    print("\n✅ All numbers processed successfully!")
