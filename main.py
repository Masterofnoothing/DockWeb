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
                "despeed":"ofpfdpleloialedjbfpocglfggbdpiem"}
docker = os.getenv("ISDOCKER")

if not docker:
    from dotenv import load_dotenv


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
def runDawn(driver, email, password, extension_id):
    driver.get(f"chrome-extension://{extension_id}/pages/dashboard.html")
    time.sleep(random.randint(7,15))
    try:
        # Switch to the alert
        alert = driver.switch_to.alert

        # Accept the alert
        alert.accept()
        time.sleep(0.99)
        alert = driver.switch_to.alert

        # Accept the alert
        alert.accept()
    except:
        logging.info("Already Logged in Skipping")
        return
    logging.info("Navigating to the website...")
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


    # Start Flask server in a separate thread
    flask_thread = threading.Thread(target=lambda: runFlask(), daemon=True)
    flask_thread.start()

    
    logging.info("Solve the CAPTCHA at http://localhost:5000")

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
        login_button = driver.find_element(By.XPATH,"/html/body/div[1]/div[2]/div[2]/form/div/div/div[4]/a/button")
        login_button.click()
        time.sleep(random.randint(3, 7))

        if driver.current_url != f"chrome-extension://{extension_id}/pages/signin.html":
            solved = True
            logging.info("Capcha Solved Sucessfully")
        else:
            logging.info("Incorrect Capcha")

    # Fina a way to stop the flask thread

    
    time.sleep(random.randint(5,12))

    logging.info("Earning started.")


def runGrass(driver,email,password,extension_id):
     # Navigate to a webpage
        logging.info('Navigating to the grass...')
        time.sleep(5)
        clearMemory(driver)
        driver.get("https://app.getgrass.io/dashboard")
        time.sleep(random.randint(7,15))
        if driver.current_url == "https://app.getgrass.io/dashboard":
            logging.info("Already logged in skipping login")
            time.sleep(random.randint(10,50))
            logging.info('Accessing extension settings page...')
            driver.get(f'chrome-extension://{extension_id}/index.html')
            time.sleep(random.randint(3,7))

            logging.info('Clicking the extension button...')
            button = driver.find_element(By.XPATH, "//button")
            button.click()

            logging.info('Logged in successfully.')
            handle_cookie_banner(driver)
            logging.info('Earning...')

            time.sleep(random.randint(1,30))

            return
        driver.get("https://app.getgrass.io/")
        time.sleep(random.randint(3,7))
        handle_cookie_banner(driver)

        logging.info('Entering credentials...')
        username = driver.find_element(By.XPATH,'/html/body/div[1]/div/div[1]/div/div[2]/div/div[1]/div/div/form/div[2]/div[1]/div/input')
        username.send_keys(email)
        passwd = driver.find_element(By.XPATH,'/html/body/div[1]/div/div[1]/div/div[2]/div/div[1]/div/div/form/div[2]/div[2]/div/input')
        passwd.send_keys(password)
               
        
        logging.info('Clicking the login button...')
        button = driver.find_element(By.XPATH, "/html/body/div[1]/div/div[1]/div/div[2]/div/div[1]/div/div/form/button")
        button.click()
        logging.info('Waiting response...')

        time.sleep(random.randint(10,50))
        logging.info('Accessing extension settings page...')
        driver.get(f'chrome-extension://{extension_id}/index.html')
        time.sleep(random.randint(3,7))

        logging.info('Clicking the extension button...')
        button = driver.find_element(By.XPATH, "//button")
        button.click()

        logging.info('Logged in successfully.')
        handle_cookie_banner(driver)
        logging.info('Earning...')

        time.sleep(random.randint(1,30))


def runNodepay():
    pass

def runGradientNode(driver,email,password):
    logging.info("Visiting app.gradient.network...................")
    clearMemory(driver)

    driver.get("https://app.gradient.network/dashboard")
    time.sleep(random.randint(7,15))
    if driver.current_url == "https://app.gradient.network/dashboard":
        logging.info("Already loggen in skipping login")
        driver.get(f"chrome-extension://caacbgbklghmpodbdafajbgdnegacfmo/popup.html")
        return
    driver.get("https://app.gradient.network/")

    time.sleep(random.randint(6,13))

    logging.info('Entering credentials...')
    email_input =driver.find_element(By.XPATH, '//input[@class="ant-input css-11fzbzo ant-input-outlined rounded-full h-9 px-4 text-sm"]')
    email_input.send_keys(email)


    time.sleep(random.randint(6,13))
    password_input = driver.find_element(By.XPATH, '//input[@placeholder="Enter Password"]')
    password_input.send_keys(password)


    button = driver.find_element(By.CSS_SELECTOR, 'button.custom-flying-button.bg-black.text-white')
    button.click()


    time.sleep(random.randint(6,13))

    window_handles = driver.window_handles

    driver.switch_to.window(window_handles[0])
    

    logging.info('Logged in successfully.')
    logging.info('Earning...')

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
    user_data_dir = os.path.join(os.getcwd(), "chrome_user_data")
    os.makedirs(user_data_dir, exist_ok=True)

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument(f"user-data-dir={user_data_dir}")
    chrome_options.add_argument("--profile-directory=Default")


    # Read variables from the OS env
    if docker == 'true':
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

        driver = webdriver.Chrome(options=chrome_options)

    else:
        load_dotenv()

        grass_email = os.getenv('GRASS_USER')
        grass_password = os.getenv('GRASS_PASS')

        gradient_email = os.getenv('GRADIENT_EMAIL')
        gradient_password = os.getenv('GRADIENT_PASS')

        dawn_email = os.getenv('DAWN_EMAIL')
        dawn_password = os.getenv('DAWN_PASS')



        driver = webdriver.Chrome(options=chrome_options)


        if  grass_email and  grass_password:
            logging.info('Installing Grass')
            download_extension(extensionIds["grass"],driver)
        if  gradient_email and  gradient_password:
            logging.info('Installing Gradient')
            download_extension(extensionIds['gradient'],driver)

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
        if dawn_email and dawn_password:
            runDawn(driver,dawn_email,dawn_password,extensionIds['dawn'])
            
        clearMemory(driver)

        #Loading a simple webpage to save resources as gradient node website is really heavy 
        #I could use this as a way to see advertisement lol 
        #if u are reading this and want your website instead of example.com contact me XD 

        driver.get("https://example.com")

        
    except Exception as e:
        logging.error(f'An error occurred: {e}')
        driver.quit()

    while True:
        try:
            time.sleep(3600)
        except KeyboardInterrupt:
            logging.info('Stopping the script...')
            driver.quit()
            break


if __name__ == "__main__":

    run()