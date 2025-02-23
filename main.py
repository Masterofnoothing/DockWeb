import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import random
import time
import logging
import subprocess


from flask import Flask, render_template, request, send_file
import threading
import time
import os
import requests
import json
import zipfile

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
                "despeed":"ofpfdpleloialedjbfpocglfggbdpiem","teneo":"emcclcoaglgcpoognfiggmhnhgabppkm"}
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


def download_from_provider_website(driver, extension_id, crx_download_url):
    """
    Download extension from the provider website.

    Args:
        driver (webdriver): The WebDriver instance.
        extension_id (str): The ID of the extension.
        crx_download_url (str): The URL to download the extension.

    Returns:
        str: The path to the downloaded CRX file.

    Raises:
        FileNotFoundError: If the CRX file is not found after extraction.
        requests.RequestException: If there is an error during the download process.
    """
    logging.info('Using the defined URL to download the extension CRX file from the provider website...')
    logging.info('Fetching the latest release information...')
    driver.get(crx_download_url)
    response_text = driver.execute_script("return document.body.textContent")
    response_json = json.loads(response_text)
    
    data = response_json['result']['data']
    version = data['version']
    linux_download_url = data['links']['linux']
    
    logging.info(f'Downloading the latest release version {version}...')
    response = requests.get(linux_download_url, verify=False)
    response.raise_for_status()
    
    zip_file_path = os.path.join(f"{extension_id}.zip")
    with open(zip_file_path, 'wb') as zip_file:
        zip_file.write(response.content)
        logging.info(f"Downloaded extension to {zip_file_path}")
    
    logging.info(f"Extracting the extension from {zip_file_path}")
    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        zip_ref.extractall('./')
    
    for root, dirs, files in os.walk('./'):
        for file in files:
            if file.endswith('.crx'):
                logging.info(f"Found CRX file: {file}")
                return os.path.join(root, file)
    
    raise FileNotFoundError('CRX file not found in the extracted folder.')



def runTeneo(driver, email, password, extension_id):
    logging.info(f"{LogColors.HEADER}🚀 Navigating to Teneo Website...{LogColors.RESET}")
    time.sleep(5)
    driver.get("https://dashboard.teneo.pro/dashboard")
    time.sleep(random.randint(7, 15))
    
    if driver.current_url == "https://dashboard.teneo.pro/dashboard":
        logging.info(f"{LogColors.OKBLUE}✅ Already logged in, skipping login{LogColors.RESET}")
        time.sleep(random.randint(10, 50))
        logging.info(f"{LogColors.OKGREEN}🖥️ Accessing extension settings page...{LogColors.RESET}")
        driver.get(f'chrome-extension://{extension_id}/index.html')
        time.sleep(random.randint(3, 7))
        
        try:
            joinButton = driver.find_element(By.XPATH, "/html/body/div/div/div/div[2]/button")
            joinButton.click()
            time.sleep(random.randint(3, 7))
            driver.get(f'chrome-extension://{extension_id}/index.html')
            time.sleep(random.randint(3, 7))
        except:
            pass
        
        connect_button = driver.find_element(By.XPATH, "/html/body/div/div/div/div[2]/div[1]/div/button[1]")
        logging.info(f"{LogColors.WARNING}🔍 Button says {connect_button.text}{LogColors.RESET}")
        while connect_button.text.strip().lower() == "connect node":
            logging.info(f"{LogColors.OKBLUE}🤔 Ooooooooooo....Maybe I should click it.....{LogColors.RESET}")
            connect_button.click()
            logging.info(f"{LogColors.OKGREEN}👌 I just clicked it!!!{LogColors.RESET}")
            time.sleep(random.randint(1, 30))
        
        logging.info(f"{LogColors.OKGREEN}💸 Earning...{LogColors.RESET}")
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


def runDawn(driver, email, password, extension_id):
    driver.get(f"chrome-extension://{extension_id}/pages/dashboard.html")
    time.sleep(random.randint(7,15))
    logging.info(f"{LogColors.HEADER}🚀 Navigating to Dawn website...{LogColors.RESET}")
    try:
        alert = driver.switch_to.alert
        alert_text = alert.text.lower()
        alert.accept()
        if "expired" not in alert_text:
            time.sleep(2.99)
            alert = driver.switch_to.alert
            alert.accept()

    except Exception as e:
        logging.info(f"{LogColors.OKBLUE}✅ Already Logged in, Skipping...{LogColors.RESET}")
        refresh_button = driver.find_element(By.ID, "refreshpoint")
        refresh_button.click()
        time.sleep(random.randint(10,15))
        
        element = driver.find_element(By.ID, "dawnbalance")
        text = element.text
        logging.info(f"{LogColors.OKGREEN}💰 Your Dawn Balance is {text}{LogColors.RESET}")

        time.sleep(random.randint(10,15))
        
        element = driver.find_element(By.CLASS_NAME, "connecttext")
        text = element.text
        if text.lower() == "connected":
            logging.info(f"{LogColors.OKGREEN}🔗 Dawn is connected{LogColors.RESET}")
            logging.info(f"{LogColors.HEADER}💸 Earning started...{LogColors.RESET}")
        return
    time.sleep(5)

    driver.get(f"chrome-extension://{extension_id}/pages/signin.html")
    time.sleep(random.randint(3, 7))

    emailElement = driver.find_element(By.XPATH, "/html/body/div[1]/div[2]/div[2]/form/div/div/div[1]/div[1]/input")
    emailElement.send_keys(email)
    time.sleep(random.randint(3, 7))

    passElement = driver.find_element(By.XPATH, "/html/body/div[1]/div[2]/div[2]/form/div/div/div[1]/div[2]/input")
    passElement.send_keys(password)
    time.sleep(random.randint(3, 7))

    capElement = driver.find_element(By.XPATH, "/html/body/div[1]/div[2]/div[2]/form/div/div/div[3]/div/div/input")
    capchaImg = driver.find_element(By.XPATH, "/html/body/div[1]/div[2]/div[2]/form/div/div/div[3]/div/img")

    flask_thread = threading.Thread(target=lambda: runFlask(), daemon=True)
    flask_thread.start()
    
    logging.info(f"{LogColors.WARNING}⚠️ Solve the CAPTCHA at http://localhost:5000{LogColors.RESET}")

    solved = False
    while not solved:
        try:
            os.remove(CAPTCHA_IMAGE_PATH)
            os.remove(CAPTCHA_RESULT_PATH)
        except:
            pass
        capchaImg.screenshot(CAPTCHA_IMAGE_PATH)
        capElement.click()
        capElement.clear()
        capElement.send_keys(askCapcha())
        time.sleep(random.randint(3, 7))
        login_button = driver.find_element(By.XPATH, "/html/body/div[1]/div[2]/div[2]/form/div/div/div[4]/a/button")
        login_button.click()
        time.sleep(random.randint(3, 7))

        if driver.current_url != f"chrome-extension://{extension_id}/pages/signin.html":
            solved = True
            logging.info(f"{LogColors.OKGREEN}✅ CAPTCHA Solved Successfully!{LogColors.RESET}")
        else:
            logging.info(f"{LogColors.FAIL}❌ Incorrect CAPTCHA, retrying...{LogColors.RESET}")

    time.sleep(random.randint(5,12))
    logging.info(f"{LogColors.HEADER}💸 Earning started.{LogColors.RESET}")



def runGrass(driver, email, password, extension_id):
    logging.info(f"{LogColors.HEADER}🚀  Starting Grass automation...{LogColors.RESET}")

    # Navigate to the dashboard
    logging.info(f"{LogColors.OKBLUE}🌍  Navigating to Grass dashboard...{LogColors.RESET}")
    time.sleep(5)
    clearMemory(driver)
    driver.get("https://app.getgrass.io/dashboard")
    time.sleep(random.randint(7, 15))

    if driver.current_url == "https://app.getgrass.io/dashboard":
        logging.info(f"{LogColors.OKGREEN}✅  Already logged in. Skipping login process.{LogColors.RESET}")
        time.sleep(random.randint(10, 50))

        logging.info(f"{LogColors.WARNING}🔧  Accessing extension settings...{LogColors.RESET}")
        driver.get(f'chrome-extension://{extension_id}/index.html')
        time.sleep(random.randint(3, 7))

        logging.info(f"{LogColors.OKGREEN}🚀  Activating extension...{LogColors.RESET}")
        button = driver.find_element(By.XPATH, "//button")
        button.click()

        logging.info(f"{LogColors.OKGREEN}🎉 Successfully logged in! Grass is running...{LogColors.RESET}")
        handle_cookie_banner(driver)
        logging.info(f"{LogColors.OKBLUE}💰  Earning in progress...{LogColors.RESET}")

        time.sleep(random.randint(1, 30))
        return

    # Login process
    logging.info(f"{LogColors.WARNING}🔄  Redirecting to login page...{LogColors.RESET}")
    driver.get("https://app.getgrass.io/")
    time.sleep(random.randint(3, 7))
    handle_cookie_banner(driver)

    logging.info(f"{LogColors.OKBLUE}🔑  Entering login credentials...{LogColors.RESET}")
    username = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[1]/div/div[2]/div/div[1]/div/div/form/div[2]/div[1]/div/input')
    username.send_keys(email)
    passwd = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[1]/div/div[2]/div/div[1]/div/div/form/div[2]/div[2]/div/input')
    passwd.send_keys(password)

    logging.info(f"{LogColors.OKGREEN}➡️ Clicking login button...{LogColors.RESET}")
    button = driver.find_element(By.XPATH, "/html/body/div[1]/div/div[1]/div/div[2]/div/div[1]/div/div/form/button")
    button.click()

    logging.info(f"{LogColors.WARNING}⏳  Waiting for login response...{LogColors.RESET}")
    time.sleep(random.randint(10, 50))

    logging.info(f"{LogColors.WARNING}🔧  Accessing extension settings...{LogColors.RESET}")
    driver.get(f'chrome-extension://{extension_id}/index.html')
    time.sleep(random.randint(3, 7))

    logging.info(f"{LogColors.OKGREEN}🚀  Activating extension...{LogColors.RESET}")
    button = driver.find_element(By.XPATH, "//button")
    button.click()

    logging.info(f"{LogColors.OKGREEN}🎉  Successfully logged in! Grass is running...{LogColors.RESET}")
    handle_cookie_banner(driver)
    logging.info(f"{LogColors.OKBLUE}💰  Earning in progress...{LogColors.RESET}")

    time.sleep(random.randint(1, 30))


def runNodepay():
    pass

def runGradientNode(driver, email, password):
    logging.info(f"{LogColors.HEADER}🚀 Starting Gradient Node automation...{LogColors.RESET}")

    # Navigate to Gradient dashboard
    logging.info(f"{LogColors.OKBLUE}🌍 Visiting Gradient Network dashboard...{LogColors.RESET}")
    clearMemory(driver)

    driver.get("https://app.gradient.network/dashboard")
    time.sleep(random.randint(7, 15))

    if driver.current_url == "https://app.gradient.network/dashboard":
        logging.info(f"{LogColors.OKGREEN}✅ Already logged in. Skipping login process.{LogColors.RESET}")

        logging.info(f"{LogColors.WARNING}🔧 Accessing extension settings...{LogColors.RESET}")
        driver.get("chrome-extension://caacbgbklghmpodbdafajbgdnegacfmo/popup.html")
        return

    logging.info(f"{LogColors.WARNING}🔄 Redirecting to login page...{LogColors.RESET}")
    driver.get("https://app.gradient.network/")
    time.sleep(random.randint(6, 13))

    # Enter login credentials
    logging.info(f"{LogColors.OKBLUE}🔑 Entering email...{LogColors.RESET}")
    email_input = driver.find_element(By.XPATH, '//input[@class="ant-input css-11fzbzo ant-input-outlined rounded-full h-9 px-4 text-sm"]')
    email_input.send_keys(email)

    time.sleep(random.randint(6, 13))

    logging.info(f"{LogColors.OKBLUE}🔒 Entering password...{LogColors.RESET}")
    password_input = driver.find_element(By.XPATH, '//input[@placeholder="Enter Password"]')
    password_input.send_keys(password)

    # Click login button
    logging.info(f"{LogColors.OKGREEN}➡️ Clicking login button...{LogColors.RESET}")
    button = driver.find_element(By.CSS_SELECTOR, 'button.custom-flying-button.bg-black.text-white')
    button.click()

    time.sleep(random.randint(6, 13))

    # Handle window switching
    logging.info(f"{LogColors.WARNING}🔀 Switching back to main window...{LogColors.RESET}")
    window_handles = driver.window_handles
    driver.switch_to.window(window_handles[0])

    logging.info(f"{LogColors.OKGREEN}🎉 Successfully logged in! Gradient Node is running...{LogColors.RESET}")
    logging.info(f"{LogColors.OKBLUE}💰 Earning in progress...{LogColors.RESET}")


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

    
    chrome_options = Options()
    chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])


    prefs = {"profile.managed_default_content_settings.images":2}
    chrome_options.add_experimental_option("prefs", prefs)

    
    # Set Chrome user data directory
    user_data_dir =  os.path.join(os.getcwd(), "chrome_user_data")
    os.makedirs(user_data_dir, exist_ok=True)

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument(f"user-data-dir={user_data_dir}")
    chrome_options.add_argument("--profile-directory=Default")
    

    # Read variables from the OS env
    # Fetch universal credentials if available
    all_email = os.getenv('ALL_EMAIL')
    all_pass = os.getenv('ALL_PASS')

    # Fetch individual credentials, falling back to all_email/all_pass if not set
    grass_email = os.getenv('GRASS_USER', all_email)
    grass_password = os.getenv('GRASS_PASS', all_pass)

    gradient_email = os.getenv('GRADIENT_EMAIL', all_email)
    gradient_password = os.getenv('GRADIENT_PASS', all_pass)

    dawn_email = os.getenv('DAWN_EMAIL', all_email)
    dawn_password = os.getenv('DAWN_PASS', all_pass)

    teneo_email = os.getenv('TENEO_EMAIL', all_email)
    teneo_password = os.getenv('TENEO_PASS', all_pass)
    if docker == 'true':



        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--headless=new')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0")

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
        driver = webdriver.Chrome(options=chrome_options)

    else:



        driver = webdriver.Chrome(options=chrome_options)


        if  grass_email and  grass_password:
            logging.info('Installing Grass')
            download_extension(extensionIds["grass"],driver)
        if  gradient_email and  gradient_password:
            logging.info('Installing Gradient')
            download_extension(extensionIds['gradient'],driver)
        if teneo_email and teneo_password:
            logging.info("Installing teneo Community Node....")
            download_extension(extensionIds['teneo'],driver)

        if  dawn_email and  dawn_password:
            logging.info('Installing Dawn')
            download_extension(extensionIds['dawn'],driver)
         

    # Enable CDP
    driver.execute_cdp_cmd("Network.enable", {})

    # Block CSS requests
    driver.execute_cdp_cmd("Network.setBlockedURLs", {"urls": ["*.css", "*.png", "*.svg"]})





    try:
        if  gradient_email and  gradient_password:
            runGradientNode(driver,gradient_email,gradient_password)
        clearMemory(driver)
        if  grass_email and  grass_password:
            runGrass(driver,grass_email,grass_password,extensionIds['grass'])
        clearMemory(driver)
        if teneo_email and teneo_password:
            runTeneo(driver,teneo_email,teneo_password,extensionIds['teneo'])
        clearMemory(driver)
        if dawn_email and dawn_password:
            runDawn(driver,dawn_email,dawn_password,extensionIds['dawn'])
            

        clearMemory(driver)
        
        #Loading a simple webpage to save resources as gradient node website is really heavy 
        #I could use this as a way to see advertisement lol 
        #if u are reading this and want your website instead of example.com contact me XD 

        driver.get("https://example.com")

        
    except Exception as e:
        logging.error(f'An error occurred: {e}')

    while True:
        try:
            time.sleep(3600)
        except KeyboardInterrupt:
            logging.info('Stopping the script...')
            driver.quit()
            break


if __name__ == "__main__":

    run()