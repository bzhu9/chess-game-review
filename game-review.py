import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from tempfile import mkdtemp
from dotenv import load_dotenv


def lambda_handler(event=None, context=None):
    load_dotenv()

    USERNAME = os.getenv("USERNAME")
    PASS = os.getenv("PASS")
    link = event["link"]
    print(USERNAME, PASS, link)
    # exit(0)

    chrome_options = webdriver.ChromeOptions()
    print("options")
    chrome_options.binary_location = "/opt/chrome/chrome"
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-notifications")
    chrome_options.add_argument('--disable-extensions')
    chrome_options.add_argument('--disable-infobars')
    # Adding argument to disable the AutomationControlled flag
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")

    # Exclude the collection of enable-automation switches
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])

    # Turn-off userAutomationExtension
    chrome_options.add_experimental_option("useAutomationExtension", False)
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1280x1696")
    chrome_options.add_argument("--single-process")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-dev-tools")
    chrome_options.add_argument("--no-zygote")
    chrome_options.add_argument(f"--user-data-dir={mkdtemp()}")
    chrome_options.add_argument(f"--data-path={mkdtemp()}")
    chrome_options.add_argument(f"--disk-cache-dir={mkdtemp()}")
    chrome_options.add_argument("--remote-debugging-port=9222")
    print("options2")
    driver = webdriver.Chrome("/opt/chromedriver", options=chrome_options)
    print("driver")
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    driver.execute_cdp_cmd('Network.setUserAgentOverride', {
        "userAgent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.53 Safari/537.36'})
    print(driver.execute_script("return navigator.userAgent;"))

    # chrome_options.add_argument('--headless')

    driver.get("https://www.chess.com/login")
    driver.implicitly_wait(0.5)

    username = driver.find_element(By.ID, "username")
    password = driver.find_element(By.ID, "password")
    login = driver.find_element(By.ID, "login")

    username.send_keys(USERNAME)
    password.send_keys(PASS)
    login.click()

    # Check Login Success
    if "Home" not in driver.title:
        html = driver.page_source
        print(html)
        print("NO HOME")

    game_number = link.split("/")[-1]
    link = "https://www.chess.com/analysis/game/live/" + game_number
    driver.get(link)

    driver.implicitly_wait(20)
    html = driver.page_source
    print(html)

    driver.quit()
    return {
        "statusCode": 200,
        "body": "{'Success': 'Success'}",
        "headers": {
            'Content-Type': 'text/html',
        }
    }