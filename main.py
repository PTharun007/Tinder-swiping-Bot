from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException, NoSuchElementException
from selenium.webdriver.chrome.options import Options
from dotenv import load_dotenv
import os
import random
from time import sleep

# Load environment variables
load_dotenv()
FB_EMAIL = os.getenv("FB_EMAIL")
FB_PASSWORD = os.getenv("FB_PASSWORD")

# Chrome options
options = Options()
options.add_argument("--start-maximized")
# options.add_argument("--headless")  # Uncomment to run in headless mode

# Initialize driver
driver = webdriver.Chrome(options=options)
wait = WebDriverWait(driver, 15)

# Step 1: Open Tinder
driver.get("https://tinder.com")

# Step 2: Accept Cookies (if prompted)
try:
    cookie_btn = wait.until(EC.element_to_be_clickable((By.XPATH, '//button[contains(text(), "I accept")]')))
    cookie_btn.click()
except TimeoutException:
    pass

# Step 3: Click "Create Account"
try:
    create_account = wait.until(EC.element_to_be_clickable((By.XPATH, '//div[text()="Create account"]')))
    create_account.click()
except TimeoutException:
    print("❌ 'Create account' button not found.")
    driver.quit()
    exit()

# Step 4: Click "Log in with Facebook"
try:
    fb_login_btn = wait.until(EC.element_to_be_clickable((By.XPATH, '//div[text()="Log in with Facebook"]/ancestor::button')))
    fb_login_btn.click()
except TimeoutException:
    print("❌ Facebook login button not found.")
    driver.quit()
    exit()

# Step 5: Switch to Facebook popup window
sleep(5)
main_window = driver.current_window_handle
for window in driver.window_handles:
    if window != main_window:
        driver.switch_to.window(window)
        break

# Step 6: Enter Facebook credentials and login
try:
    email_input = wait.until(EC.presence_of_element_located((By.ID, "email")))
    password_input = wait.until(EC.presence_of_element_located((By.ID, "pass")))
    login_button = wait.until(EC.element_to_be_clickable((By.NAME, "login")))

    email_input.send_keys(FB_EMAIL)
    password_input.send_keys(FB_PASSWORD)
    login_button.click()
    print("✅ Facebook credentials submitted.")
except TimeoutException:
    print("❌ Facebook login form not found.")
    driver.quit()
    exit()

# Step 7: Switch back to Tinder main window
sleep(5)
driver.switch_to.window(main_window)

# Step 8: Handle location access prompt
try:
    allow_btn = wait.until(EC.element_to_be_clickable((By.XPATH, '//button[contains(., "Allow")]')))
    allow_btn.click()
    print("✅ Location access allowed.")
    sleep(3)
except TimeoutException:
    print("⚠️ Location prompt not found. Continuing...")

# Step 9: Handle notification popup
try:
    miss_out_btn = wait.until(EC.element_to_be_clickable((By.XPATH, '//button[@data-testid="decline"]')))
    miss_out_btn.click()
    print("✅ Notification popup dismissed.")
    sleep(2)
except TimeoutException:
    print("⚠️ Notification prompt not found. Continuing...")

# Step 10: Wait for main swipe screen
try:
    wait.until(EC.presence_of_element_located((By.XPATH, '//div[contains(@class, "recsCardboard__cards")]')))
    wait.until(EC.element_to_be_clickable((By.XPATH, '//button[@aria-label="Like"]')))
    print("🎉 Successfully logged in and ready to swipe.")
except TimeoutException:
    print("❌ Failed to confirm Tinder login.")
    driver.save_screenshot("tinder_login_fail.png")
    print("📸 Screenshot saved as tinder_login_fail.png")
    driver.quit()
    exit()

# Step 11: Start swiping loop
swipe_count = 0
MAX_SWIPES = 100

print("🔥 Starting to swipe profiles...")

while swipe_count < MAX_SWIPES:
    try:
        action = random.choice(["like", "nope"])
        if action == "like":
            like_btn = wait.until(EC.element_to_be_clickable((By.XPATH, '//button[@aria-label="Like"]')))
            like_btn.click()
            print("💚 Liked a profile")
        else:
            nope_btn = wait.until(EC.element_to_be_clickable((By.XPATH, '//button[@aria-label="Nope"]')))
            nope_btn.click()
            print("❌ Passed on a profile")

        swipe_count += 1
        print(f"👉 Total Swipes: {swipe_count}")
        sleep(random.uniform(1.5, 3.5))

    except TimeoutException:
        print("⚠️ No more profiles or button not found.")
        break
    except ElementClickInterceptedException:
        print("⚠️ Popup blocked action, trying to close it...")
        try:
            close_btn = driver.find_element(By.XPATH, '//button[@aria-label="Back to Tinder"]')
            close_btn.click()
            print("✅ Closed popup.")
        except NoSuchElementException:
            print("⚠️ No close button found. Skipping...")
        continue

print(f"🎯 Finished swiping. Total actions: {swipe_count}")
driver.quit()