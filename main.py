import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import random
import time
import logging
import subprocess
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException,StaleElementReferenceException


from flask import Flask, render_template, request, send_file
import threading
import time
import os
import requests
import capsolver
import json

def get_chromedriver_version():
    try:
        result = subprocess.run(['chromedriver', '--version'], capture_output=True, text=True)
        return result.stdout.strip()
    except Exception as e:
        logging.error(f"Could not get ChromeDriver version: {e}")
        return "Unknown version"
    

def natural_sleep(base, variance=2):
    time.sleep(base + random.uniform(-variance, variance))


def is_recaptcha_present(driver):
    try:
        # First check if the reCAPTCHA iframe exists and is visible
        iframe = driver.find_element(By.CSS_SELECTOR, "iframe[src*='recaptcha']")
        if iframe.is_displayed():
            # reCAPTCHA iframe is present, now check if it's solved
            try:
                token_field = driver.find_element(By.CSS_SELECTOR, "textarea#g-recaptcha-response")
                token = token_field.get_attribute("value").strip()
                if token:
                    return False  # reCAPTCHA solved
            except NoSuchElementException:
                pass
            return True  # reCAPTCHA present and unsolved
    except NoSuchElementException:
        pass

    return False  # No CAPTCHA iframe found => assume absent

def call_capsolver(driver, extension_id="bbdhfoclddncoaomddgkaaphcnddbpdh", enable_auto=True) -> None:
    original_window = driver.current_window_handle
    driver.execute_script("window.open('');")
    driver.switch_to.window(driver.window_handles[-1])

    try:
        driver.get(f"chrome-extension://{extension_id}/popup.html")

        # List of all settings you want to toggle
        settings = [
            "recaptcha_auto_open",
            "recaptcha_auto_solve"
        ]

        for setting in settings:
            expected_class = "off" if enable_auto else "on"
            desired_class = "on" if enable_auto else "off"

            try:
                # Wait for the toggle with expected current class
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, f'div.settings_toggle.{expected_class}[data-settings="{setting}"]'))
                )

                toggles = driver.find_elements(By.CSS_SELECTOR, f'div.settings_toggle.{expected_class}[data-settings="{setting}"]')
                for toggle in toggles:
                    driver.execute_script("arguments[0].click();", toggle)

            except Exception as e:
                pass

    finally:
        driver.close()
        driver.switch_to.window(original_window)

def send_discord_webhook(webhook_url, title, log_results, color=16711680):
    """
    Sends an embedded message to a Discord webhook with log results as fields.
    """
    embed = {
        "title": title,
        "color": color,
        "fields": [{"name": key, "value": str(value), "inline": False} for key, value in log_results.items()]
    }
    
    data = {"embeds": [embed]}
    
    response = requests.post(webhook_url, json=data)
    if response.status_code == 204:
        print("Message sent successfully!")
    else:
        print(f"Failed to send message: {response.status_code}, {response.text}")

# Define ANSI escape codes for colors
class LogColors:
    HEADER = "\033[95m"  # Purple
    OKBLUE = "\033[94m"  # Blue
    OKGREEN = "\033[92m"  # Green
    WARNING = "\033[93m"  # Yellow
    FAIL = "\033[91m"  # Red
    RESET = "\033[0m"    # Reset color

app = Flask(__name__)
log = logging.getLogger('werkzeug')
log.disabled = True
# Path for storing the CAPTCHA image and result
CAPTCHA_IMAGE_PATH = "./static/screenshot.png"
CAPTCHA_RESULT_PATH = "./static/captcha_result.txt"

def runFlask():
    try:
        app.run(host="0.0.0.0", port=5000, debug=False, use_reloader=False)
    except:
        pass

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/captcha")
def serve_captcha():
    return send_file(CAPTCHA_IMAGE_PATH, mimetype="image/png")

@app.route("/submit", methods=["POST"])
def submit():
    user_input = request.form.get("captcha_text")
    if user_input:
        with open(CAPTCHA_RESULT_PATH, "w") as f:
            f.write(user_input)
        
        return "CAPTCHA submitted successfully! The script will now continue."
    return "Invalid input, please try again."


extensionIds = {"nodepay":"lgmpfmgeabnnlemejacfljbmonaomfmm","grass":"ilehaonighjijnmpnagapkhpcdbhclfg","gradient":"caacbgbklghmpodbdafajbgdnegacfmo","dawn":"fpdkjdnhkakefebpekbdhillbhonfjjp",
                "despeed":"ofpfdpleloialedjbfpocglfggbdpiem","teneo":"emcclcoaglgcpoognfiggmhnhgabppkm","grass-node":"lkbnfiajjmbhnfledhphioinpickokdi"}
docker = os.getenv("ISDOCKER")

if not docker:
    from dotenv import load_dotenv
    #For developement environment
    load_dotenv()

def setup_logging():
    # Now simplified; run() handles basicConfig for unified setup.
    # Can be removed if no other logging responsibilities.
    pass # Kept for potential future logging setup (e.g., handlers).

def clearMemory(driver):
    """Closes unused tabs to save memory."""
    window_handles = driver.window_handles

    # Keep the first tab open
    driver.switch_to.window(window_handles[0])

    # Close all other tabs
    for handle in window_handles[1:]:
        driver.switch_to.window(handle)
        driver.close()

    # Switch back to the first tab to ensure driver is on a valid window
    driver.switch_to.window(window_handles[0])


def handle_cookie_banner(driver):
    """
    Handle the cookie banner by clicking the "ACCEPT ALL" button if it's present.

    Args:
        driver (webdriver): The WebDriver instance.
    """
    try:
        # Match button by visible text
        cookie_button = driver.find_element(By.XPATH, "//button[contains(translate(., 'abcdefghijklmnopqrstuvwxyz', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'), 'ACCEPT ALL')]")
        
        if cookie_button:
            logging.info('Cookie banner found. Accepting cookies...')
            cookie_button.click()
            time.sleep(random.randint(3, 11))  # simulate human behavior
            logging.info('Cookies accepted.')
    except NoSuchElementException:
        logging.info("No cookie banner found.")
    except Exception as e:
        logging.warning(f"Unexpected error while handling cookie banner: {e}")
def askCapcha():
    
    while not os.path.exists(CAPTCHA_RESULT_PATH):
        time.sleep(1)

    # Read the CAPTCHA result
    with open(CAPTCHA_RESULT_PATH, "r") as f:
        captcha_text = f.read().strip()

    logging.info("CAPTCHA entered.")
    return captcha_text


def add_cooki(driver, cooki):
    driver.execute_script(f"localStorage.setItem('{cooki['key']}', '{cooki['value']}');")


def runTeneo(driver, email=None, password=None, extension_id=None, cookie=None, delay_multiplier=1.0):
    driver.set_window_size(1024, driver.get_window_size()['height'])
    logging.info(f"{LogColors.HEADER}🚀 Navigating to Teneo Website...{LogColors.RESET}")
    driver.get("https://dashboard.teneo.pro")
    
    timeout = max(10, 20 * delay_multiplier)  # Ensure a minimum wait time of 10 seconds
    wait = WebDriverWait(driver, timeout)  # Set a max wait time based on delay multiplier
    natural_sleep(15,variance=7)
    if cookie:
        add_cooki(driver, {"key": "accessToken", "value": cookie})
        add_cooki(driver,{"key":"auth","value":json.dumps({"state":{"accessToken":cookie,"signupToken":None,"passwordResetTimeout":{"email":"","state":None,"timestamp":0,"duration":0}},"version":0})})
        add_cooki(driver,{"key":"sb-node-b-auth-token","value":json.dumps({"access_token":cookie,"token_type":"bearer"})})
        driver.refresh()
        try:
            time.sleep(15)
            wait.until(EC.url_contains("/dashboard"))
            logging.info("Log in sucessfull")
        except:
            logging.error("Nodepay cookie seems to be expired")
            return
        
    if driver.current_url == "https://dashboard.teneo.pro/dashboard":
        logging.info(f"{LogColors.OKBLUE}✅ Inside the dahboard.....{LogColors.RESET}")
        logging.info(f"{LogColors.OKGREEN}🖥️ Accessing extension settings page...{LogColors.RESET}")
        driver.get(f'chrome-extension://{extension_id}/index.html')
        
        try:
            driver.add_cookie({"accessToken":cookie})
            driver.refresh()

            joinButton = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Join now')]")))
            joinButton.click()
            logging.info("Join Now button was clicked......")
            natural_sleep(3*delay_multiplier)
            clearMemory(driver)
            driver.get(f'chrome-extension://{extension_id}/index.html')
        except:
            pass
        natural_sleep(3*delay_multiplier)
        connect_button = driver.find_element(By.XPATH, "/html/body/div/div/div/div[2]/div[1]/div/button[1]")
        logging.info(f"{LogColors.WARNING}🔍 Button says {connect_button.text}{LogColors.RESET}")
        
        while connect_button.text.strip().lower() == "connect node":
            logging.info(f"{LogColors.OKBLUE}🤔 Ooooooooooo....Maybe I should click it.....{LogColors.RESET}")
            connect_button.click()
            logging.info(f"{LogColors.OKGREEN}👌 I just clicked it!!!{LogColors.RESET}")
            time.sleep(random.randint(3,10)*delay_multiplier)
            if "disconnect" in connect_button.text.lower():
                logging.info(f"{LogColors.OKGREEN}Connected Sucessfully{LogColors.RESET}")

        logging.info(f"{LogColors.OKGREEN}💸 Earning...{LogColors.RESET}")
        return
    logging.info(driver.current_url)
    logging.info("Login Failed")
    return
    time.sleep(random.randint(3, 7))
    logging.info(f"{LogColors.HEADER}🔑 Entering credentials...{LogColors.RESET}")
    email_element = driver.find_element(By.XPATH, "/html/body/div/main/div/div/div[2]/div/div/div[1]/input")
    email_element.send_keys(email)
    password_element = driver.find_element(By.XPATH, "/html/body/div/main/div/div/div[2]/div/div/div[2]/div/input")
    password_element.send_keys(password)
    
    logging.info(f"{LogColors.OKBLUE}🖱️ Clicking the login button...{LogColors.RESET}")
    login_button = driver.find_element(By.XPATH, "/html/body/div/main/div/div/div[2]/div/div/button")
    login_button.click()
    logging.info(f"{LogColors.WARNING}⏳ Waiting for response...{LogColors.RESET}")
    
    time.sleep(random.randint(10, 50))
    logging.info(f"{LogColors.OKGREEN}🖥️ Accessing extension settings page...{LogColors.RESET}")
    driver.get(f'chrome-extension://{extension_id}/index.html')
    time.sleep(random.randint(3, 7))
    
    joinButton = driver.find_element(By.XPATH, "/html/body/div/div/div/div[2]/button")
    joinButton.click()
    time.sleep(random.randint(3, 7))
    
    driver.get(f'chrome-extension://{extension_id}/index.html')
    time.sleep(random.randint(3, 7))
    logging.info(f"{LogColors.OKGREEN}💪 Clicking the connect button...{LogColors.RESET}")
    connect_button = driver.find_element(By.XPATH, "/html/body/div/div/div/div[2]/div[1]/div/button[1]")
    
    if connect_button.text.strip().lower() == "connect node":
        logging.info(f"{LogColors.OKBLUE}🤝 Clicking the connect button...{LogColors.RESET}")
        connect_button.click()
    else:
        logging.info(f"{LogColors.FAIL}👀 Button does not say 'Connect'. Skipping click.{LogColors.RESET}")
        logging.info(f"{LogColors.OKGREEN}💸 Earning...{LogColors.RESET}")
    
    time.sleep(random.randint(1, 30))
    return


def runDawn(driver, email, password, extension_id, delay_multiplier=1.0):
    driver.get(f"chrome-extension://{extension_id}/pages/dashboard.html")
    timeout = max(10, 20 * delay_multiplier)  # Ensure a minimum wait time of 10 seconds
    wait = WebDriverWait(driver, timeout)  # Set a max wait time based on delay multiplier
    logging.info(f"{LogColors.HEADER}🚀 Navigating to Dawn website...{LogColors.RESET}")
    natural_sleep(15,variance=7)
    try:
        alert = wait.until(EC.alert_is_present())
        alert_text = alert.text.lower()
        alert.accept()
        if "expired" not in alert_text:
            wait.until(EC.alert_is_present()).accept()
    except:
        logging.info(f"{LogColors.OKBLUE}✅ Already Logged in, Skipping...{LogColors.RESET}")
        refresh_button = wait.until(EC.element_to_be_clickable((By.ID, "refreshpoint")))
        refresh_button.click()
        
        element = wait.until(EC.visibility_of_element_located((By.ID, "dawnbalance")))
        logging.info(f"{LogColors.OKGREEN}💰 Your Dawn Balance is {element.text}{LogColors.RESET}")

        element = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "connecttext")))
        if element.text.lower() == "connected":
            logging.info(f"{LogColors.OKGREEN}🔗 Dawn is connected{LogColors.RESET}")
            logging.info(f"{LogColors.HEADER}💸 Earning started...{LogColors.RESET}")
        return

    driver.get(f"chrome-extension://{extension_id}/pages/signin.html")
    
    emailElement = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@id='email']")))
    emailElement.send_keys(email)
    
    passElement = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@id='password']")))
    passElement.send_keys(password)

    capElement = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='puzzelAns']")))
    capchaImg = wait.until(EC.visibility_of_element_located((By.XPATH, "//*[@id='puzzleImage']")))

    flask_thread = threading.Thread(target=runFlask, daemon=True)
    flask_thread.start()

    logging.info(f"{LogColors.WARNING}⚠️ Solve the CAPTCHA at http://localhost:5000{LogColors.RESET}")

    solved = False
    while not solved:
        try:
            os.remove(CAPTCHA_IMAGE_PATH)
            os.remove(CAPTCHA_RESULT_PATH)
        except FileNotFoundError:
            pass
        
        capchaImg.screenshot(CAPTCHA_IMAGE_PATH)
        capElement.click()
        capElement.clear()
        capElement.send_keys(askCapcha())

        login_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='loginButton']")))
        login_button.click()
        
        try:
            wait.until(EC.url_changes(driver.current_url))
            solved = True
            logging.info(f"{LogColors.OKGREEN}✅ CAPTCHA Solved Successfully!{LogColors.RESET}")
        except:
            logging.info(f"{LogColors.FAIL}❌ Incorrect CAPTCHA, retrying...{LogColors.RESET}")

    logging.info(f"{LogColors.HEADER}💸 Earning started.{LogColors.RESET}")


def runGrass(driver, email, password, extension_id, delay_multiplier=1):
    MAX_GRASS_RETRIES = 5  # Maximum number of retry attempts for the main loop
    retry_count = 0        # Initialize retry counter

    while True:  # Main retry loop for Grass connection
        try:
            logging.info(f"🚀 Starting Grass automation...")
            
            logging.info(f"🌍 Navigating to Grass dashboard...")
            clearMemory(driver)
            driver.get("https://app.grass.io/dashboard")
            natural_sleep(15*delay_multiplier,variance=3)

            if driver.current_url == "https://app.grass.io/dashboard":
                logging.info(f"✅ Already logged in. Skipping login process.")
                WebDriverWait(driver, random.randint(10, 50) * delay_multiplier).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
                
                logging.info(f"🔧 Accessing extension settings...")
                driver.get(f'chrome-extension://{extension_id}/index.html')
                WebDriverWait(driver, random.randint(3, 7) * delay_multiplier).until(EC.presence_of_element_located((By.XPATH, "//button")))
                
                logging.info(f"🚀 Activating extension...")
                timeout = 0
                while True:
                    status_elements = driver.find_elements(By.XPATH, "//p[@class='chakra-text css-uzsxi7']")
                    if not status_elements: 
                        logging.warning("Grass status element not found. Assuming not connected and will retry or fail.")
                        if timeout > 60 * delay_multiplier:
                            # Raise an exception if the status element is not found after the timeout
                            raise Exception("Grass status element not found after timeout.")
                        time.sleep(1)
                        timeout +=1
                        driver.refresh() # Attempt to refresh the extension page
                        natural_sleep(5)
                        continue # Retry finding the element

                    status_text = status_elements[0].text.lower()
                    if "connected" in status_text:
                        break # Exit the status check loop
                    if timeout > 60 * delay_multiplier:
                        logging.error("Grass Failed to connect after timeout")
                        # Raise an exception if connection fails after the timeout
                        raise Exception("Grass failed to connect after timeout")
                    time.sleep(1)
                    logging.info("waiting for grass to connect")
                    timeout += 1
                
                logging.info(f"🎉 Successfully logged in! Grass is running...")
                # handle_cookie_banner(driver) # Likely not needed here, on the extension page
                logging.info(f"💰 Earning in progress...")
                break  
            
            logging.info(f"🔄 Redirecting to login page...")
            driver.get("https://app.grass.io/")
            natural_sleep(7,3)
            handle_cookie_banner(driver)
            
            logging.info(f"🔑 Entering login credentials...")

            username = driver.find_element(By.NAME, "email")
            username.send_keys(email)

            button = driver.find_element(By.XPATH, "//button[contains(text(), 'CONTINUE')]")
            button.click()
            natural_sleep(5*delay_multiplier)
            
            tries = 0 
            capsolver_active = False
            while is_recaptcha_present(driver):
                if tries > 3:
                    logging.error("Failed to Solve CAPTCHA after multiple attempts")
                    # Raise an exception if CAPTCHA solving fails multiple times
                    raise Exception("Failed to Solve CAPTCHA after multiple attempts")
                logging.info("Captcha found trying to auto solve")
                if not capsolver_active:
                    call_capsolver(driver)
                    capsolver_active = True
                natural_sleep(60) 
                tries += 1 
            
            call_capsolver(driver,enable_auto=False) 
            natural_sleep(random.uniform(2,5)) 

            use_password_button = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, "//p[translate(., 'abcdefghijklmnopqrstuvwxyz', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ')='USE PASSWORD INSTEAD']"))
            )
            use_password_button.click()
            logging.info("Clicked on Use Password Instead......")
            natural_sleep(random.uniform(2,5))
            
            passwd_field = driver.find_element(By.NAME, "password")
            passwd_field.send_keys(password)
            
            signin_button = driver.find_element(By.XPATH, "//button[contains(translate(., 'abcdefghijklmnopqrstuvwxyz', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'), 'SIGN IN')]")
            signin_button.click()
            logging.info(f"➡️ Clicking login button...")
            
            logging.info(f"⏳ Waiting for login response...")
            WebDriverWait(driver, random.randint(10, 50) * delay_multiplier).until(EC.url_contains("dashboard"))

            logging.info(f"⏳ Log in successful.......")
            logging.info(f"🔧 Accessing extension settings...")
            driver.get(f'chrome-extension://{extension_id}/index.html')
            WebDriverWait(driver, random.randint(3, 7) * delay_multiplier).until(EC.presence_of_element_located((By.XPATH, "//button")))
            
            logging.info(f"🚀 Activating extension...")
            timeout = 0
            while True:
                status_elements_after_login = driver.find_elements(By.XPATH, "//p[@class='chakra-text css-uzsxi7'] | //p[contains(text(),'Grass is Connected')] | //p[contains(text(),'Connected')]")
                
                if not status_elements_after_login:
                    logging.warning("Grass status element not found after login. Will retry or fail.")
                    if timeout > 60 * delay_multiplier:
                        # Raise an exception if status element is not found after login and timeout
                        raise Exception("Grass status element not found after login and timeout.")
                    time.sleep(1)
                    timeout +=1
                    driver.refresh() # Refresh the extension page
                    natural_sleep(5)
                    continue # Retry finding the element

                status_text_after_login = status_elements_after_login[0].text.lower()
                logging.info(f"Grass status after login attempt: {status_text_after_login}")
                if "connected" in status_text_after_login:
                    break # Exit the post-login status check loop
                if timeout > 60 * delay_multiplier:
                    logging.error("Grass Failed to show connected status after login")
                    # Raise an exception if connected status is not shown after login and timeout
                    raise Exception("Grass failed to show connected status after login and timeout")
                time.sleep(1)
                logging.info("waiting for grass to show connected status after login")
                timeout += 1
            
            logging.info(f"🎉 Successfully logged in and extension confirmed! Grass is running...")
            # handle_cookie_banner(driver) # Likely not needed here, on the extension page
            logging.info(f"💰 Earning in progress...\n\n\n")
            break  

        except BaseException as be:  # Catching BaseException for wider capture during debugging
            print(f"[DEBUG] runGrass caught an exception: {type(be).__name__}") # Raw print for immediate debug output
            # Modified error log below to be more user-friendly and hide verbose stack trace from 'be'
            logging.error(f"😥 Grass encountered a {type(be).__name__}. Will attempt to retry.") 
            
            retry_count += 1 # Increment retry counter
            if retry_count >= MAX_GRASS_RETRIES:
                logging.error(f"Max retries ({MAX_GRASS_RETRIES}) reached for Grass. Skipping this app.")
                return # Exit the function, stopping retries for Grass

            logging.info(f"Retrying Grass connection in 300 seconds... (Attempt {retry_count}/{MAX_GRASS_RETRIES})")
            try:
                if driver: # Ensure driver object exists
                    clearMemory(driver) # Attempt to clear tabs
                    driver.get('about:blank') # Navigate to a blank page to reset state
            except Exception as ce:
                logging.error(f"Error during cleanup before retry: {ce}")
            time.sleep(300) # Wait 300 seconds before the next attempt

def runNodepay(driver, cookie=None, email=None, passwd=None, api_key=None, delay_multiplier=1):
    driver.set_window_size(1024, driver.get_window_size()['height'])
    driver.get("https://app.nodepay.ai/dashboard")
    time.sleep(random.randint(9,16))
    
    if cookie and driver.current_url != "https://app.nodepay.ai/dashboard":
        add_cooki(driver, {"key": "np_token", "value": cookie})
        add_cooki(driver, {"key": "np_webapp_token", "value": cookie})
        driver.refresh()
        driver.get("https://app.nodepay.ai/dashboard")
        time.sleep(random.randint(9,16))
        WebDriverWait(driver, random.randint(8, 13) * delay_multiplier).until(EC.url_contains("dashboard"))
        
        if driver.current_url != "https://app.nodepay.ai/dashboard":
            logging.error("Nodepay cookie seems to be expired")
            driver.save_screenshot("nodepay_login_failed.png")
            return
    
    if driver.current_url != "https://app.nodepay.ai/dashboard":
        with open("./static/cloud.js", "r", encoding="utf-8") as f:
            inject_js_content = f.read()
        driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {"source": inject_js_content})
        driver.refresh()
        
        site_key = "0x4AAAAAAAx1CyDNL8zOEPe7"
        task_id = capsolver.create_turnstile_task(api_key, site_key, "https://app.nodepay.ai/login")
        
        input_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//input[@id='basic_user']"))
        )
        input_element.send_keys(email)
        
        password_element = driver.find_element(By.XPATH, "//input[@id='basic_password']")
        password_element.send_keys(passwd)
        
        solved_token = None
        while not solved_token:
            solved_token = capsolver.get_turnstile_response(task_id, api_key)
            WebDriverWait(driver, 1 * delay_multiplier).until(lambda d: solved_token is not None)
        
        driver.execute_script("""
            const captchaInput = document.querySelector('[name="cf-turnstile-response"]');
            if (captchaInput) {
                captchaInput.value = arguments[0];
                captchaInput.dispatchEvent(new Event("input", { bubbles: true }));
                captchaInput.dispatchEvent(new Event("change", { bubbles: true }));
            }
            if (window.turnstile && typeof window.tsCallback === "function") {
                window.tsCallback(arguments[0]);
            }
        """, solved_token)
        
        button_element = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[span[text()='Access My Account']]")
        ))
        button_element.click()
        
        WebDriverWait(driver, random.randint(3, 7) * 30 * delay_multiplier).until(
            EC.url_contains("dashboard")
        )
    
    logging.info("Log In successful")
    extension_id = extensionIds['nodepay']
    driver.get(f'chrome-extension://{extension_id}/index.html')
    WebDriverWait(driver, random.randint(8, 13) * delay_multiplier).until(
        EC.presence_of_element_located((By.XPATH, "//span[contains(@class, 'font-bold') and contains(@class, 'text-green')]")
    ))
    
    connected = driver.find_element(By.XPATH, "//span[contains(@class, 'font-bold') and contains(@class, 'text-green')]")
    if connected.text.strip().lower() == "connected":
        logging.info("The extension is connected :D")
    
    price_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//span[contains(@class, 'text-16px') and contains(@class, 'font-bold') and contains(@class, 'mr-1') and contains(@class, 'truncate')]")
    ))
    price_text = price_element.text.strip()
    
    logging.info(f"Your nodepay season earnings is {price_text}")
    return


def runGradientNode(driver, email, password, delay_multiplier=1):
    """
    Automates the login and navigation process for Gradient Node.

    Args:
        driver: Selenium WebDriver instance.
        email: User's email address.
        password: User's password.
        delay_multiplier: Multiplier for random sleep intervals and timeout duration.
    """
    timeout = max(10, 20 * delay_multiplier)  # Ensure a minimum wait time of 10 seconds
    wait = WebDriverWait(driver, timeout)  # Set a max wait time based on delay multiplier

    def earning_status():
        pass

    logging.info(f"🚀 Starting Gradient Node automation...")
    logging.info(f"🌍 Visiting Gradient Network dashboard...")
    clearMemory(driver)

    driver.get("https://app.gradient.network/dashboard")
    natural_sleep(random.randint(9, 15) * delay_multiplier)

    if driver.current_url == "https://app.gradient.network/dashboard":
        logging.info(f"✅ Already logged in. Skipping login process.")
        logging.info(f"🔧 Accessing extension settings...")
        driver.get("chrome-extension://caacbgbklghmpodbdafajbgdnegacfmo/popup.html")
        natural_sleep(2)
        logging.info(f"💰 Earning in progress...")
        return

    logging.info(f"🔄 Redirecting to login page...")
    driver.get("https://app.gradient.network/")
    wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))

    logging.info(f"🔑 Entering email...")
    email_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 
        'input.ant-input.css-2ronba.ant-input-outlined.rounded-full.h-9.px-4.text-sm[type="text"][placeholder="Enter Email"]')))
    email_input.send_keys(email)
    natural_sleep(2)

    logging.info(f"🔒 Entering password...")
    password_input = wait.until(EC.presence_of_element_located((By.XPATH, 
        '//input[@placeholder="Enter Password"]')))
    password_input.send_keys(password)
    natural_sleep(2)

    logging.info(f"➡️ Clicking login button...")
    button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 
        'button.custom-flying-button.bg-black.text-white')))
    button.click()
    natural_sleep(3)

    logging.info(f"🔀 Waiting for login to complete...")
    wait.until(EC.url_contains("dashboard"))

    logging.info(f"🔀 Switching back to main window...")
    window_handles = driver.window_handles
    driver.switch_to.window(window_handles[0])

    logging.info(f"🔧 Accessing extension settings...")
    driver.get("chrome-extension://caacbgbklghmpodbdafajbgdnegacfmo/popup.html")
    natural_sleep(2)
    logging.info(f"💰 Earning in progress...")
    logging.info(f"🎉 Successfully logged in! Gradient Node is running...")
    logging.info(f"💰 Earning in progress...")

def download_extension(extension_id, driver=None,repo_path="./crx-dl/crx-dl.py"):
    """
    Downloads a Chrome extension using the crxdl script.
    Args:
        extension_id (str): The ID of the Chrome extension to download.
        repo_path (str): Path to the crxdl executable script.
    Returns:
        None
    """
    # Assumes 'docker' is a global var (e.g., docker = os.getenv("ISDOCKER"))
    if docker == 'true': 
        try:
            # Log CRX download start.
            logging.info(f"Downloading CRX for ID: {extension_id} using {repo_path}...")
            result = subprocess.run(["python3",repo_path, extension_id], check=True, text=True, capture_output=True)
            
            # Log output from crx-dl.py script.
            logging.info(f"Download script output for {extension_id}: {result.stdout.strip()}") 
            if result.stderr:
                # Log stderr if download script produced any.
                logging.warning(f"Download script stderr for {extension_id}: {result.stderr.strip()}")
        except subprocess.CalledProcessError as e:
            # Catches crx-dl.py script errors (non-zero exit code).
            logging.error(f"Failed to download extension {extension_id}. Subprocess error: {e.stderr}")
        except FileNotFoundError:
            # Catches error if crx-dl.py script not found.
            logging.error(f"Failed to download extension {extension_id}: crx-dl.py script not found at {repo_path}.")
    else:
        # Non-Docker: Manual download (unchanged).
        url = f"https://chromewebstore.google.com/detail/{extension_id}"
        print(f"Opening: {url}")

        # Open the extension's page
        driver.get(url)

        # Wait for the page to load
        time.sleep(5)

        #Since I am lazy to automate this add the extension manually XOXO
        input("Add the extension and press enter")
        return


def run():
   
    # Centralized logging: called once at script start.
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    # setup_logging() call no longer needed for basicConfig.
    # Call if it has other non-basicConfig logging tasks.

    logging.info('Starting the script (run function)...')

    branding = f'''{LogColors.OKBLUE}
                $$$$$$$\                      $$\                               $$\       
                $$  __$$\                     $$ |                              $$ |      
                $$ |  $$ | $$$$$$\   $$$$$$$\ $$ |  $$\ $$\  $$\  $$\  $$$$$$\  $$$$$$$\  
                $$ |  $$ |$$  __$$\ $$  _____|$$ | $$  |$$ | $$ | $$ |$$  __$$\ $$  __$$\ 
                $$ |  $$ |$$ /  $$ |$$ /      $$$$$$  / $$ | $$ | $$ |$$$$$$$$ |$$ |  $$ |
                $$ |  $$ |$$ |  $$ |$$ |      $$  _$$<  $$ | $$ | $$ |$$   ____|$$ |  $$ |
                $$$$$$$  |\$$$$$$  |\$$$$$$$\ $$ | \$$\ \$$$$$\$$$$  |\$$$$$$$\ $$$$$$$  |
                \_______/  \______/  \_______|\__|  \__| \_____\____/  \_______|\_______/ {LogColors.RESET}'''
    
    logging.info(branding)


    user_data_dir = os.path.join(os.getcwd(), "chrome_user_data")
    os.makedirs(user_data_dir, exist_ok=True)

    #Delete the singleton locked file
    found = False
    for filename in os.listdir(user_data_dir):
        if filename.strip().lower() == "singletonlock": #strip and lower
            actual_path = os.path.join(user_data_dir, filename)
            os.remove(actual_path)
            logging.info(f"Removed {filename} file.")
            found = True
            break

    if not found:
        logging.info("SingletonLock file not found")

    chrome_options = Options()

    #Prevent Images from loading to save resources 
    chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])
    prefs = {"profile.managed_default_content_settings.images":2}
    chrome_options.add_experimental_option("prefs", prefs)
    
    #Set profile 
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument(f"user-data-dir={user_data_dir}")
    chrome_options.add_argument("--profile-directory=Default")

    # Read variables from the OS env
    # Fetch universal credentials if available
    all_email = os.getenv('ALL_EMAIL')
    all_pass = os.getenv('ALL_PASS')

    # Fetch individual credentials, falling back to all_email/all_pass if not set
    grass_email = os.getenv('GRASS_USER') or os.getenv('GRASS_EMAIL', all_email)
    grass_password = os.getenv('GRASS_PASS', all_pass)

    gradient_email = os.getenv('GRADIENT_EMAIL', all_email)
    gradient_password = os.getenv('GRADIENT_PASS', all_pass)

    dawn_email = os.getenv('DAWN_EMAIL', all_email)
    dawn_password = os.getenv('DAWN_PASS', all_pass)

    teneo_cooki = os.getenv('TENEO_COOKI') or os.getenv("TENEO_COOKIE")

    teneo_email = os.getenv('TENEO_EMAIL', all_email)
    teneo_password = os.getenv('TENEO_PASS', all_pass)

    np_cooki = os.getenv('NP_COOKI') or os.getenv("NP_COOKIE") or os.getenv("NODEPAY_COOKIE")

    np_email = os.getenv("NODEPAY_EMAIL",all_email)
    np_password = os.getenv("NODEPAY_PASSWORD",all_pass)

    twoCapApiKey = os.getenv("API_KEY")
    webhook_url = os.getenv("DISCORD_WEBHOOK") or os.getenv("WEBHOOK")

    delay_multiplier = int((os.getenv("DELAY")) or 1)

    if docker == 'true':

        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--headless=new')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36")

        chromedriver_version = get_chromedriver_version()
        logging.info(f'Using {chromedriver_version}')

        logging.info("Installing rektCaptcha")
        download_extension("bbdhfoclddncoaomddgkaaphcnddbpdh")
        chrome_options.add_extension("bbdhfoclddncoaomddgkaaphcnddbpdh.crx")
        # Check if credentials are provided
        if  grass_email and  grass_password:
            logging.info('Installing Grass')
            download_extension(extensionIds["grass"])
            id = extensionIds["grass"]
            chrome_options.add_extension(f"./{id}.crx")

        if  gradient_email and  gradient_password:
            logging.info('Installing Gradient')
            download_extension(extensionIds['gradient'])
            id = extensionIds["gradient"]
            chrome_options.add_extension(f"./{id}.crx")

        if dawn_email and dawn_password:
            logging.info("Installing Dawn Internet....")
            download_extension(extensionIds['dawn'])
            id = extensionIds['dawn']
            chrome_options.add_extension(f"./{id}.crx")
        if teneo_email and teneo_password:
            logging.info("Installing Teneo Community Node....")
            download_extension(extensionIds['teneo'])
            id = extensionIds['teneo']
            chrome_options.add_extension(f"./{id}.crx")
        if np_cooki:
            logging.info("Installing Nodepay Node....")
            download_extension(extensionIds['nodepay'])
            id = extensionIds['nodepay']
            chrome_options.add_extension(f"./{id}.crx")

        driver = webdriver.Chrome(options=chrome_options)

    else:
        driver = webdriver.Chrome(options=chrome_options)

        if  grass_email and  grass_password:
            logging.info('Installing Grass')
            download_extension(extensionIds["grass"],driver)
        if  gradient_email and  gradient_password:
            logging.info('Installing Gradient')
            download_extension(extensionIds['gradient'],driver)

        if (np_cooki) or (twoCapApiKey and np_email and np_password):
            logging.info("Installing nodepay")
            download_extension(extensionIds['nodepay'],driver)
        if (teneo_email and teneo_password and twoCapApiKey) or teneo_cooki:

            logging.info("Installing teneo Community Node....")
            download_extension(extensionIds['teneo'],driver)

        if  dawn_email and  dawn_password:
            logging.info('Installing Dawn')
            download_extension(extensionIds['dawn'],driver)

    # Enable CDP
    driver.execute_cdp_cmd("Network.enable", {})

    # Block CSS requests
    driver.execute_cdp_cmd("Network.setBlockedURLs", {"urls": ["*.css", "*.png", "*.svg"]})

    call_capsolver(driver,enable_auto=False)

    results = {}

    def safe_execute(app_key, func, *args, **kwargs):
        try:
            results[app_key] = func(*args, **kwargs)
        except Exception as e:
            logging.error(f'Error in {app_key}: {e}')
            results[app_key] = f'Error: {e}'

    try:
        logging.info(f"Delay Multiplier is {delay_multiplier}")
        if gradient_email and gradient_password:
            safe_execute("gradient", runGradientNode, driver, gradient_email, gradient_password,delay_multiplier)
        clearMemory(driver)
        if grass_email and grass_password:
            safe_execute("grass", runGrass, driver, grass_email, grass_password, extensionIds['grass'],delay_multiplier)
        clearMemory(driver)

        if np_cooki:
            safe_execute("nodepay", runNodepay, driver, cookie=np_cooki,delay_multiplier=delay_multiplier)
        elif np_email and np_password and twoCapApiKey:
            safe_execute("nodepay", runNodepay, driver, passwd=np_password, email=np_email, api_key=twoCapApiKey)
        clearMemory(driver)
    
        if teneo_cooki:
            safe_execute("teneo", runTeneo, driver, extension_id=extensionIds['teneo'],cookie=teneo_cooki,delay_multiplier=delay_multiplier)
        elif teneo_email and teneo_password:
            safe_execute("teneo", runTeneo, driver, teneo_email, teneo_password, extensionIds['teneo'],delay_multiplier=delay_multiplier)
        clearMemory(driver)

        if dawn_email and dawn_password:
            safe_execute("dawn", runDawn, driver, dawn_email, dawn_password, extensionIds['dawn'],delay_multiplier=delay_multiplier)
        clearMemory(driver)

        # Loading a simple webpage to save resources
        try:
            driver.get("https://example.com")
        except Exception as e:
            logging.error(f'Error loading example.com: {e}')

        if webhook_url:
            send_discord_webhook(webhook_url,"DockwebStatus",results)

    except Exception as e:
        logging.error(f'A critical error occurred: {e}')

    while True:
        try:
            time.sleep(3600)
        except KeyboardInterrupt:
            logging.info('Stopping the script...')
            driver.quit()
            break

if __name__ == "__main__":
    run()
