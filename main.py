import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import random
import time
import logging
import subprocess



extensionIds = {"nodepay":"lgmpfmgeabnnlemejacfljbmonaomfmm","grass":"ilehaonighjijnmpnagapkhpcdbhclfg","gradient":"caacbgbklghmpodbdafajbgdnegacfmo","dawn":"fpdkjdnhkakefebpekbdhillbhonfjjp"}
def setup_logging():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def clearMemory(driver):
    "Closes unused tabs to save memory"
    window_handles = driver.window_handles

    driver.switch_to.window(window_handles[0])

    for i in range(len(window_handles)-1):
        driver.switch_to.window(window_handles[i])



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

def runGrass(driver,email,password,extension_id):
     # Navigate to a webpage
        logging.info('Navigating to the website...')
        time.sleep(5)
        window_handles = driver.window_handles

        driver.switch_to.window(window_handles[0])
        driver.get("https://app.getgrass.io/")
        time.sleep(random.randint(3,7))
        handle_cookie_banner(driver)

        logging.info('Entering credentials...')
        username = driver.find_element(By.NAME,"user")
        username.send_keys(email)
        passwd = driver.find_element(By.NAME,"password")
        passwd.send_keys(password)
               
        
        logging.info('Clicking the login button...')
        button = driver.find_element(By.XPATH, "//button")
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
    window_handles = driver.window_handles

    driver.switch_to.window(window_handles[0])
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
    

    logging.info('Clicking the extension button...')
    driver.get("chrome-extension://caacbgbklghmpodbdafajbgdnegacfmo/popup.html")
    time.sleep(random.randint(6,13))
    button = driver.find_element(By.XPATH,"//button[@class='w-full h-[48px] text-center flex-row-center rounded-[125px] text-[16px] font-normal leading-[100%] bg-black text-white mt-[32px] z-20 Helveticae']")
    button.click()

    logging.info('Logged in successfully.')
    logging.info('Earning...')

def download_extension(extension_id, repo_path="./chrome-extension-downloader/bin/crxdl"):
    """
    Downloads a Chrome extension using the crxdl script.
    
    Args:
        extension_id (str): The ID of the Chrome extension to download.
        repo_path (str): Path to the crxdl executable script.
    
    Returns:
        None
    """
    try:
        print(f"Starting download for extension ID: {extension_id}")
        result = subprocess.run([repo_path, extension_id], check=True, text=True, capture_output=True)
        print("Download successful!")
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print("An error occurred while downloading the extension:")
        print(e.stderr)


def run():
    setup_logging()
    logging.info('Starting the script...')

    # Read variables from the OS env
    grass_email = os.getenv('GRASS_USER')
    grass_password = os.getenv('GRASS_PASS')

    gradient_email = os.getenv('GRADIENT_EMAIL')
    gradient_password = os.getenv('GRADIENT_PASS')


    chrome_options = Options()
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


    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--headless=new')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0")


    # Initialize the WebDriver
    driver = webdriver.Chrome(options=chrome_options)


    try:
        if  gradient_email and  gradient_password:
            runGradientNode(driver,gradient_email,gradient_password)
        clearMemory(driver)
        if  grass_email and  grass_password:
            runGrass(driver,grass_email,grass_password,extensionIds['grass'])
            
        clearMemory(driver)

        
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



run()