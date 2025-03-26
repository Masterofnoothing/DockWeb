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
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


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



# function to handle cookie banner: If a cookie banner is present press the button containing the accept text
def handle_cookie_banner(driver):
    """
    Handle the cookie banner by clicking the "Accept" button if it's present.

    Args:
        driver (webdriver): The WebDriver instance.
    """
    try:
        cookie_banner = driver.find_element(By.XPATH, "//button[contains(text(), 'ACCEPT')]")
        if cookie_banner:
            logging.info('Cookie banner found. Accepting cookies...')
            cookie_banner.click()
            time.sleep(random.randint(3, 11))
            logging.info('Cookies accepted.')
    except Exception:
        pass
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
    
    wait = WebDriverWait(driver, 15 * delay_multiplier)
    
    if cookie:
        add_cooki(driver, {"key": "accessToken", "value": cookie})
        add_cooki(driver,{"key":"auth","value":json.dumps({"state":{"accessToken":cookie,"signupToken":None,"passwordResetTimeout":{"email":"","state":None,"timestamp":0,"duration":0}},"version":0})})
        driver.refresh()
        try:
            time.sleep(15)
            wait.until(EC.url_contains("/dashboard"))
        except:
            logging.error("Nodepay cookie seems to be expired")
            return
        
    if driver.current_url == "https://dashboard.teneo.pro/dashboard":
        logging.info(f"{LogColors.OKBLUE}✅ Already logged in, skipping login{LogColors.RESET}")
        logging.info(f"{LogColors.OKGREEN}🖥️ Accessing extension settings page...{LogColors.RESET}")
        driver.get(f'chrome-extension://{extension_id}/index.html')
        
        try:
            joinButton = wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div/div/div/div[2]/button")))
            joinButton.click()
            driver.get(f'chrome-extension://{extension_id}/index.html')
        except:
            pass

        connect_button = wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div/div/div/div[2]/div[1]/div/button[1]")))
        logging.info(f"{LogColors.WARNING}🔍 Button says {connect_button.text}{LogColors.RESET}")
        
        while connect_button.text.strip().lower() == "connect node":
            logging.info(f"{LogColors.OKBLUE}🤔 Ooooooooooo....Maybe I should click it.....{LogColors.RESET}")
            connect_button.click()
            logging.info(f"{LogColors.OKGREEN}👌 I just clicked it!!!{LogColors.RESET}")
            WebDriverWait(driver, random.randint(1, 30) * delay_multiplier).until(EC.staleness_of(connect_button))

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
    wait = WebDriverWait(driver, 15 * delay_multiplier)
    logging.info(f"{LogColors.HEADER}🚀 Navigating to Dawn website...{LogColors.RESET}")

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
    
    emailElement = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@type='email']")))
    emailElement.send_keys(email)
    
    passElement = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@type='password']")))
    passElement.send_keys(password)

    capElement = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@class='captcha']/div/input")))
    capchaImg = wait.until(EC.visibility_of_element_located((By.XPATH, "//div[@class='captcha']/div/img")))

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

        login_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//a/button[contains(text(), 'Login')]")))
        login_button.click()
        
        try:
            wait.until(EC.url_changes(driver.current_url))
            solved = True
            logging.info(f"{LogColors.OKGREEN}✅ CAPTCHA Solved Successfully!{LogColors.RESET}")
        except:
            logging.info(f"{LogColors.FAIL}❌ Incorrect CAPTCHA, retrying...{LogColors.RESET}")

    logging.info(f"{LogColors.HEADER}💸 Earning started.{LogColors.RESET}")
def runGrass(driver, email, password, extension_id, delay_multiplier=1):
    logging.info(f"🚀 Starting Grass automation...")
    
    logging.info(f"🌍 Navigating to Grass dashboard...")
    clearMemory(driver)
    driver.get("https://app.getgrass.io/dashboard")
    WebDriverWait(driver, random.randint(7, 15) * delay_multiplier).until(EC.url_contains("dashboard"))
    
    if driver.current_url == "https://app.getgrass.io/dashboard":
        logging.info(f"✅ Already logged in. Skipping login process.")
        WebDriverWait(driver, random.randint(10, 50) * delay_multiplier).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        
        logging.info(f"🔧 Accessing extension settings...")
        driver.get(f'chrome-extension://{extension_id}/index.html')
        WebDriverWait(driver, random.randint(3, 7) * delay_multiplier).until(EC.presence_of_element_located((By.XPATH, "//button")))
        
        logging.info(f"🚀 Activating extension...")
        button = driver.find_element(By.XPATH, "//button")
        button.click()
        
        logging.info(f"🎉 Successfully logged in! Grass is running...")
        handle_cookie_banner(driver)
        logging.info(f"💰 Earning in progress...")
        return
    
    logging.info(f"🔄 Redirecting to login page...")
    driver.get("https://app.getgrass.io/")
    WebDriverWait(driver, random.randint(3, 7) * delay_multiplier).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
    handle_cookie_banner(driver)
    
    logging.info(f"🔑 Entering login credentials...")
    username = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, 
        '/html/body/div[1]/div/div[1]/div/div[2]/div/div[1]/div/div/form/div[2]/div[1]/div/input')))
    username.send_keys(email)
    
    passwd = driver.find_element(By.XPATH, 
        '/html/body/div[1]/div/div[1]/div/div[2]/div/div[1]/div/div/form/div[2]/div[2]/div/input')
    passwd.send_keys(password)
    
    logging.info(f"➡️ Clicking login button...")
    button = driver.find_element(By.XPATH, "/html/body/div[1]/div/div[1]/div/div[2]/div/div[1]/div/div/form/button")
    button.click()
    
    logging.info(f"⏳ Waiting for login response...")
    WebDriverWait(driver, random.randint(10, 50) * delay_multiplier).until(EC.url_contains("dashboard"))
    
    logging.info(f"🔧 Accessing extension settings...")
    driver.get(f'chrome-extension://{extension_id}/index.html')
    WebDriverWait(driver, random.randint(3, 7) * delay_multiplier).until(EC.presence_of_element_located((By.XPATH, "//button")))
    
    logging.info(f"🚀 Activating extension...")
    button = driver.find_element(By.XPATH, "//button")
    button.click()
    
    logging.info(f"🎉 Successfully logged in! Grass is running...")
    handle_cookie_banner(driver)
    logging.info(f"💰 Earning in progress...")
def runNodepay(driver, cookie=None, email=None, passwd=None, api_key=None, delay_multiplier=1):
    driver.set_window_size(1920, driver.get_window_size()['height'])
    driver.get("https://app.nodepay.ai/dashboard")
    WebDriverWait(driver, random.randint(9, 15) * delay_multiplier).until(EC.url_contains("dashboard"))
    
    if cookie and driver.current_url != "https://app.nodepay.ai/dashboard":
        add_cooki(driver, {"key": "np_token", "value": cookie})
        add_cooki(driver, {"key": "np_webapp_token", "value": cookie})
        driver.refresh()
        driver.get("https://app.nodepay.ai/dashboard")
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
        delay_multiplier: Multiplier for random sleep intervals.
    """
    wait = WebDriverWait(driver, 20)  # Set a max wait time of 20 seconds

    logging.info(f"🚀 Starting Gradient Node automation...")
    logging.info(f"🌍 Visiting Gradient Network dashboard...")
    clearMemory(driver)

    driver.get("https://app.gradient.network/dashboard")
    wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))

    if driver.current_url == "https://app.gradient.network/dashboard":
        logging.info(f"✅ Already logged in. Skipping login process.")

        logging.info(f"🔧 Accessing extension settings...")
        driver.get("chrome-extension://caacbgbklghmpodbdafajbgdnegacfmo/popup.html")
        return

    logging.info(f"🔄 Redirecting to login page...")
    driver.get("https://app.gradient.network/")
    wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))

    logging.info(f"🔑 Entering email...")
    email_input = wait.until(EC.presence_of_element_located((By.XPATH, 
        '//input[@class="ant-input css-11fzbzo ant-input-outlined rounded-full h-9 px-4 text-sm"]')))
    email_input.send_keys(email)

    logging.info(f"🔒 Entering password...")
    password_input = wait.until(EC.presence_of_element_located((By.XPATH, 
        '//input[@placeholder="Enter Password"]')))
    password_input.send_keys(password)

    logging.info(f"➡️ Clicking login button...")
    button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 
        'button.custom-flying-button.bg-black.text-white')))
    button.click()

    logging.info(f"🔀 Waiting for login to complete...")
    wait.until(EC.url_contains("dashboard"))

    logging.info(f"🔀 Switching back to main window...")
    window_handles = driver.window_handles
    driver.switch_to.window(window_handles[0])

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
    if docker == 'true':
        try:
            logging.info(f"Starting download for extension ID: {extension_id}")
            result = subprocess.run(["python3",repo_path, extension_id], check=True, text=True, capture_output=True)
            logging.info("Download successful!")
            logging.info(result.stdout)
        except subprocess.CalledProcessError as e:
            logging.info("An error occurred while downloading the extension:")
            logging.error(e.stderr)
    else:
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
    setup_logging()
    logging.info('Starting the script...')

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
    chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])


    prefs = {"profile.managed_default_content_settings.images":2}
    chrome_options.add_experimental_option("prefs", prefs)

    

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument(f"user-data-dir={user_data_dir}")
    chrome_options.add_argument("--profile-directory=Default")
    

    # Read variables from the OS env
    # Fetch universal credentials if available
    all_email = os.getenv('ALL_EMAIL')
    all_pass = os.getenv('ALL_PASS')

    # Fetch individual credentials, falling back to all_email/all_pass if not set
    grass_email = os.getenv('GRASS_USER') or os.getenv('GRASS_USER', all_email)
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
        chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0")

        chromedriver_version = get_chromedriver_version()
        logging.info(f'Using {chromedriver_version}')

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