import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import random
import time
import logging
import subprocess



extensionIds = {"nodepay":"lgmpfmgeabnnlemejacfljbmonaomfmm","grass":"ilehaonighjijnmpnagapkhpcdbhclfg","gradient":"caacbgbklghmpodbdafajbgdnegacfmo"}
def setup_logging():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def runGrass(driver,email,password,extension_id):
     # Navigate to a webpage
        logging.info('Navigating to the website...')
        driver.get("https://app.getgrass.io/")
        time.sleep(random.randint(3,7))

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
        logging.info('Earning...')


def runNodepay():
    pass

def runGradientNode(driver,email,password):
    logging.info("Visiting app.gradient.network...................")
    driver.get("https://app.gradient.network/")

    time.sleep(random.randint(3,7))

    logging.info('Entering credentials...')
    email_input =driver.find_element(By.XPATH, '//input[@class="ant-input css-11fzbzo ant-input-outlined rounded-full h-9 px-4 text-sm"]')
    email_input.send_keys(email)


    time.sleep(random.randint(3,7))
    password_input = driver.find_element(By.XPATH, '//input[@placeholder="Enter Password"]')
    password_input.send_keys(password)


    button = driver.find_element(By.CSS_SELECTOR, 'button.custom-flying-button.bg-black.text-white')
    button.click()


    time.sleep(random.randint(3,7))

    window_handles = driver.window_handles

    driver.switch_to.window(window_handles[0])
    

    logging.info('Clicking the extension button...')
    driver.get("chrome-extension://caacbgbklghmpodbdafajbgdnegacfmo/popup.html")
    time.sleep(random.randint(3,7))
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
        result = subprocess.run([repo_path, extension_id], check=True, text=True, capture_output=True,shell=True)
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

    # Check if credentials are provided
    if  grass_email and  grass_password:
        logging.error('Installing Grass')
        download_extension(extensionIds["grass"])
    if  gradient_email and  gradient_password:
        logging.error('Installing Gradient')
        download_extension(extensionIds['gradient'])

    chrome_options = Options()
    chrome_options.add_extension()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--headless=new')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0")


    # Initialize the WebDriver
    driver = webdriver.Chrome(options=chrome_options)


    try:
        if  grass_email and  grass_password:
            runGrass(driver,gradient_email,grass_password,extensionIds['grass'])
            

        if  gradient_email and  gradient_password:
            runGradientNode(driver,gradient_email,gradient_password)

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