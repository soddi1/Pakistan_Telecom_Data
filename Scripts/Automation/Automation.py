import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import pyautogui
import pyperclip  # To interact with the clipboard
import json

# Replace these with your actual email and password
email = "***"
password = "***"

# Path to the document to upload
document_path = r"C:\Users\Dell\Desktop\A_Project\Flooding\OpenCelliD data\Flooding\PTA-Data-Analysis\PTA-dataset\2018\cmo_qos_survey_2018_030119.pdf"

# The prompt to write in the textarea
prompt_text = "Give JSON for this PDF."

# Initialize Chrome options
options = uc.ChromeOptions()
options.add_argument("--disable-save-password-bubble")
options.add_argument("--password-store=basic")
options.add_argument("--start-maximized")
options.add_experimental_option(
    "prefs",
    {
        "credentials_enable_service": False,
        "profile.password_manager_enabled": False,
    },
)

# Initialize the undetected Chrome driver with options
driver = uc.Chrome(options=options)

try:
    # Navigate to the webpage
    driver.get("https://chatgpt.com/?model=gpt-4")

    # Wait for the page to load completely
    time.sleep(3)

    # Find and click the login button
    login_button = driver.find_element(By.XPATH, "//button[@data-testid='login-button']")
    login_button.click()

    # Wait for the login page to load
    time.sleep(3)

    # Enter the email address and press Enter
    email_input = driver.find_element(By.XPATH, "//input[@type='email']")
    email_input.send_keys(email)
    email_input.send_keys(Keys.ENTER)

    # Wait for the password page to load
    time.sleep(3)

    # Enter the password and press Enter
    password_input = driver.find_element(By.XPATH, "//input[@type='password']")
    password_input.send_keys(password)
    password_input.send_keys(Keys.ENTER)

    # Wait for the login process to complete
    time.sleep(5)

    # Navigate to the desired page after login
    driver.get("https://chatgpt.com/?model=gpt-4")

    # Wait for the page to load
    time.sleep(3)

    # Locate and click the button
    button = driver.find_element(By.XPATH, "//button[@class='flex items-center justify-center h-8 w-8 rounded-full text-token-text-primary focus-visible:outline-black dark:text-white dark:focus-visible:outline-white mb-1 ml-1.5']")
    button.click()

    # Wait for the upload options to appear
    time.sleep(2)

    # Locate and click the "Upload from computer" option
    upload_option = driver.find_element(By.XPATH, "//div[contains(text(), 'Upload from computer')]")
    upload_option.click()

    # Wait for the file dialog to open
    time.sleep(2)

    # Use PyAutoGUI to interact with the file upload dialog
    pyautogui.write(document_path)
    pyautogui.press('enter')

    # Wait for the upload process to complete
    time.sleep(5)

    # Locate the textarea and write the prompt
    textarea = driver.find_element(By.XPATH, "//textarea[@id='prompt-textarea']")
    textarea.send_keys(prompt_text)

    # Submit the prompt by pressing Enter
    textarea.send_keys(Keys.ENTER)

    # Wait for the code to be generated
    time.sleep(100)

    # Locate and click the "Copy code" button
    copy_code_button = driver.find_element(By.XPATH, "//button[@class='flex gap-1 items-center']")
    copy_code_button.click()

    # Wait for the clipboard to update
    time.sleep(100)

    # Retrieve the code from the clipboard
    copied_code = pyperclip.paste()

    # Save the code to a JSON file
    json_data = {"code": copied_code}
    with open("copied_code.json", "w") as json_file:
        json.dump(json_data, json_file, indent=4)

finally:
    # Ensure that the driver is properly closed
    driver.quit()
