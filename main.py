import os
import re
import ast
import time
import json
import psutil
import random
import requests
import pyfiglet
import pyautogui
import os
# from pyvirtualdisplay import Display
# import Xlib.display
# from pyshadow.main import Shadow
# import pyautogui
from dotenv import load_dotenv, set_key
from bs4 import BeautifulSoup
from seleniumbase import SB
from seleniumbase import Driver
# import undetected_chromedriver
# from undetected_chromedriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains


global url
global session_id
# global driver
numerical_ip_address = "49.12.168.17"
ip_address = "EverlasterSMP.falixsrv.me"
server_port = "28294"
server_ip_address = ip_address + ":" + server_port
falix_email_address = "johnsmithencena@gmail.com"
falix_password = "noqhoG-4vivhe-kuqwab"

proxy_options = {
    'proxy': {
        'http': 'http://user:pass@ip.port',
        'https': 'https://user:pass@ip.port',
        'no_proxy': 'locahost,127.0.0.1'
    }
}

user_agents = [
    # Add your list of user agents here
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 13_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15',
]

def check_initialization():
    dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
    print(f"Loading .env file from: {dotenv_path}")  # Debugging
    load_dotenv(dotenv_path)
    print("Checking environment variables...")
    for key, value in os.environ.items():
        print(f"{key}: {value}")
    email = os.getenv("FALIX_EMAIL_ADDRESS")
    password = os.getenv("FALIX_PASSWORD")
    if not email:
        print("❌ ERROR: 'FALIX_EMAIL_ADDRESS' not found!")
        email = input("Enter your FALIX_EMAIL_ADDRESS: ")
        set_key(dotenv_path, "FALIX_EMAIL_ADDRESS", email)
    if not password:
        print("❌ ERROR: 'FALIX_PASSWORD' not found!")
        password = input("Enter your FALIX_PASSWORD: ")
        set_key(dotenv_path, "FALIX_PASSWORD", password)
    print(f"✅ Loaded Email: {email}")
    print(f"✅ Loaded Password: {password}")
    return email, password

def change_credientials(variable):
    dotenv_path = '.env'
    print("Please enter the following information when asked!:")
    print(f"{variable} is missing or incorrect. Please enter your {variable}.")
    falix_variable = input(f"Enter your {variable}: ")
    set_key(dotenv_path, variable, falix_variable)
    load_dotenv(dotenv_path, override=True)
    print("All necessary data has been collected and stored in environment variables.")
    return falix_variable

def login_website(driver, email, password):
    while True: 
        print(email, password)
        try:
            driver.uc_open_with_reconnect("https://client.falixnodes.net/auth/login", 6)
            # driver.open("https://client.falixnodes.net/auth/login")
            print("Login page loaded.")
            time.sleep(5)
            try:
                email_field = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.ID, "email-address"))
                )
                email_field.send_keys(email)
                print("Email entered!")
            except Exception:
                print("Email field not found, possibly due to CAPTCHA. Restarting login process...")
                continue 
            driver.find_element(By.ID, "password").send_keys(password)
            print("Password entered!")
            login_button = driver.find_element(By.NAME, "submit")
            login_button.click()
            print("Clicked on login button!")
            try:
                print("Checking for login failure...")
                alert_warning = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "alert.alert-danger"))).text
                if "incorrect" in alert_warning.lower():
                    email = change_credientials("FALIX_EMAIL_ADDRESS")
                    password = change_credientials("FALIX_PASSWORD")
                    print("Login failed due to incorrect credentials.")
                else:
                    print("Captcha found!")
                print("Login failed. Restarting the login process...")
                continue 
            except:
                print("Login successful!")
                break
        except Exception as e:
            print(f"Unexpected error during login: {e}")
            continue  

    print("Login process completed.")
    return driver  

def selecting_servers(driver):
    """Verifies login and retrieves server details."""
    dotenv_path = ".env"  
    print("Waiting for server body...")
    try:
        found_servers_body = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "card.mt-0"))
        )
        print("Server body found!")
        found_servers = found_servers_body.find_elements(By.CLASS_NAME, "col")
        servers_string = ""  
        server_dictionary = {}  
        for index, col in enumerate(found_servers, start=1):
            server_name, server_status = col.text.split('\n')[:2]
            server_dictionary[index] = {"name": server_name, "status": server_status, 'element': col}
            print(f"Found server: {server_name} -> {server_status}, {col}")
            servers_string += f"{index}. {server_name}: {server_status}\n"
        set_key(dotenv_path, "FALIX_SERVERS", str(server_dictionary))
        load_dotenv(dotenv_path, override=True)

        res = os.environ["FALIX_SERVERS"]
        print("Server dictionary:")
        print(res)

        falix_server = input(f"Which server would you like to upkeep automatically?\n{servers_string}").strip()

        while not falix_server.isnumeric() or int(falix_server) not in server_dictionary:
            print("Please enter a valid number corresponding to the server you would like to keep running:")
            falix_server = input(servers_string).strip()

        selected_server = server_dictionary[int(falix_server)]
        print(f"Selected server: {selected_server['name']} ({selected_server['status']})")

        return driver, server_dictionary, int(falix_server)

    except Exception as e:
        print(f"Error fetching server data: {e}")
        driver.quit()
        raise Exception("Failed to fetch server data.")


def check_time():
    return time.asctime(time.localtime(time.time()))


def check_server_status(server_ip_address):
    while True:
        try:
            print(f"Querying {server_ip_address} status...")
            pre_parsed_data = requests.get(
                f'https://api.mcstatus.io/v2/status/java/{server_ip_address}').json()
        except:
            exit("Please provide the correct server IP address and port!")
        else:
            return pre_parsed_data


def check_chrome_instance():
    for proc in psutil.process_iter(['pid', 'name']):
        if proc.info['name'] == 'chrome.exe':
            return True
    return False


class TooManyClickFails(Exception):
    pass


def server_automation(current_driver, server_dictionary, falix_server_index, asc_time):
    server_ip = server_dictionary[falix_server_index]
    print(server_ip)
    server_fail = True
    auto_fail = False
    # print(f"Server automation started on {server_ip['element'].text}...")
    # print(server_ip['element'])
    try:
        data = check_server_status(server_ip['status'])
        print(data)
        if data['online'] is False or data['version']['name_clean'] == '⬤ OFFLINE':
            if current_driver is None:
                driver = Driver(uc=True, headless=False)
                driver.set_page_load_timeout = 200
                driver = login_website(driver, os.environ['FALIX_EMAIL_ADDRESS'], os.environ['FALIX_PASSWORD'])
            else:
                driver = current_driver
            print(asc_time)
            time.sleep(5)
            # try:
            #     driver.find_element(By.XPATH, "//div[@class='adngin-bottom_adhesive-close']//path").click()
            #     print("Clicked on ad button!")
            # except:
            #     print("No close button found, continuing...")
            print("Clicking manage...")
            manage_button = driver.find_elements(By.XPATH, "//form[@action='server/console']")[falix_server_index - 1]
            # for server in manage_button:
            #     print(server.text)
            #     print(server.location_once_scrolled_into_view)
            driver.execute_script("""
                var element = arguments[0];
                var rect = element.getBoundingClientRect();
                var yOffset = window.pageYOffset || document.documentElement.scrollTop;
                var offset = -70; // Adjust this value to fine-tune positioning (negative for a small gap)
                window.scrollTo({top: rect.top + yOffset + offset, behavior: 'smooth'});
            """, manage_button)
            time.sleep(3)
            manage_button.click()
            time.sleep(5)
            # manage_button = server_ip['element'].find_element(By.XPATH, "//form[@action='server/console']")
            # Scroll the element into view
            # action = ActionChains(driver)
            # action.move_to_element(manage_button).click().perform()
            # time.sleep(5)
            try:
                driver.find_element(By.XPATH, "//button[text()='Cancel']").click()
                print("Clicked on cancel button!")
            except:
                print("No cancel button found, continuing...")

            # driver.execute_script("arguments[0].click();", manage_button)

            # Optionally, move to the element before clicking
            # actions = ActionChains(driver)
            # actions.move_to_element(manage_button).perform()

            # Click the button
            # manage_button.click()
            auto_start_time = time.time()
            # server_fail = False
            # shadow_root_prior = driver.find_element(By.XPATH, "//*[@id='top']/div/div/div/div/div/div/div[2]/div/form/center/div")
            # act = ActionChains(driver)
            # act.send_keys(k)
            # captcha_verification_frame = driver.find_element(By.XPATH, "//*[@id='top']/div/div/div/div/div/div/div[2]/div/form/center/div/div")
            # print("PASS!")
            # captcha_verification_shadow_root = captcha_verification_frame.shadow_root
            # print(captcha_verification_shadow_root)
            # captcha_verification_document = captcha_verification_frame.contentDocument
            # captcha_verification_button = driver.execute_script("""
            # return document.querySelector('#top > div > div > div > div > div > div > div.col-md-7.d-flex.flex-center > div > form > center > div > div').shadowRoot.querySelector('#kNIq7 > div > label > input[type=checkbox]')
            # """)
            print("PASS!")
            time.sleep(5)
            print("Clicking on server box...")
            # server_box_click_count = 0
            while True:
                # RED COLOR: M256 512A256 256 0 1 0 256 0a256 256 0 1 0 0 512z -- svg-inline--fa fa-circle fa-2xl me-2 text-danger
                # GREEN COLOR: M256 512A256 256 0 1 0 256 0a256 256 0 1 0 0 512z -- svg-inline--fa fa-circle fa-2xl me-2 text-success
                try:
                    server_box = driver.find_element(By.ID, 'startbutton')
                    driver.execute_script("""
                        var element = arguments[0];
                        var rect = element.getBoundingClientRect();
                        var yOffset = window.pageYOffset || document.documentElement.scrollTop;
                        var offset = -70; // Adjust this value to fine-tune positioning (negative for a small gap)
                        window.scrollTo({top: rect.top + yOffset + offset, behavior: 'smooth'});
                    """, server_box)
                    # action.move_to_element(server_box).click().perform()
                    time.sleep(5)
                    server_box = driver.find_element(By.ID, 'startbutton')
                    server_box.click()
                    time.sleep(3)
                    try:
                        danger_alert = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'startbutton')))
                        print("Server box not clicked successfully, retrying...")
                    except Exception as e:
                        print("Server box clicked successfully!")
                        server_fail = False
                        break
                    time.sleep(5)
                    try:
                        disable_adblock = driver.find_element(By.ID, 'unblock')
                        print("Adblock found???")
                        driver.uc_open_with_reconnect("https://client.falixnodes.net/server/console", 6)
                        continue
                        print("This shouldn't be printed!")
                        # time.sleep(500)
                    except:
                        print("No adblock found, continuing...")
                    # disable_adblock = driver.find_element(By.ID, 'unblock')
                    # disable_adblock.click()
                    # time.sleep(500)
                    time.sleep(5)
                    try:
                        watch_ad_button = driver.find_element(By.XPATH, "//button[@aria-label='Watch Ad']")
                        print("Clicked on watch ad button!")
                        watch_ad_button.click()
                        time.sleep(30)
                        print("Ad watched successfully!")
                        server_fail = False
                        break
                        # count_down = driver.find_element(By.XPATH, "//div[@id='count_down']")

                        # while count_down.text != "Reward is in 0 seconds":
                        #     try:
                        #         count_down = driver.find_element(By.XPATH, "//div[@id='count_down']")
                        #         print(count_down.text)
                        #     except:
                        #         print("No cancel button found, continuing...")
                        #         time.sleep(5)
                        
                        # time.sleep(5)
                        # reward_ad = driver.find_element(By.XPATH, "//div[@id='close_button_icon']")
                        # reward_ad.click()
                        # print("Server box clicked successfully!")
                        # server_fail = False
                        # break
                    except Exception as e:
                        print("No ads/already watched ads, continuing..." + e)
                        time.sleep(5)
                    # server_box = driver.find_element(By.ID, 'startbutton')
                    # action = ActionChains(driver)
                    # action.move_to_element(server_box).click().perform()
                except Exception as e:
                        # server_box_click_count += 1
                    current_url = driver.current_url
                    if current_url == "https://client.falixnodes.net/#google_vignette":
                        print("Google vignette detected, refreshing...")
                        driver.uc_open_with_reconnect("https://client.falixnodes.net/server/console", 6)
                        continue
                    else:
                        print("Failed to click on server box or server not online yet..." + e)
                        # if server_box_click_count == 3:
                        #     print("Trying to click on server_box took too many attempts, restarting...")
                        #     raise TooManyClickFails
                        # else:
                        #     driver.refresh
                        #     time.sleep(2)
            # print("Clicking on start box...")
            time.sleep(7)
            # start_box_click_count = 0
            # while True:
            #     try:
            #         # pyautogui.moveTo(946, 578)
            #         time.sleep(3)
            #         # pyautogui.click()
            #         # pyautogui.click()
            #         break
            #     except:
            #         start_box_click_count += 1
            #         print("Failed to click on start box...")
            #         if start_box_click_count == 3:
            #             print("Trying to click on start_box took too many attempts, restarting...")
            #             raise TooManyClickFails
            #         else:
            #             # driver.refresh
            #             time.sleep(2)
            time.sleep(3)
            auto_process_time = time.time() - auto_start_time
            print(f"Automation took {auto_process_time:.2f} seconds to turn on.")
            driver.close()
            driver.quit()
        else:
            print("Server is already online, continuing...")
            server_fail = False
            if current_driver is not None:
                driver = current_driver
                driver.close()
                driver.quit()
    except Exception as e:
        exit(e)
        auto_fail = True
        driver.close()
        driver.quit()
        # if check_chrome_instance():
        #     os.system("taskkill /f /im chrome.exe")
        # else:
        #     pass
    finally:
        automation_schedule(auto_fail, server_fail)
        return None


def automation_schedule(a_status: bool, s_status: bool):
    try:
        if a_status:
            print("Automation failed, retrying in 3 seconds...")
            time.sleep(3)
        elif not s_status:
            # if check_chrome_instance():
            #     os.system("taskkill /f /im chrome.exe")
            # else:
            #     pass
            print("Automation successfully started the server, continuing after 3 minutes...")
            time.sleep(180)
        else:
            # if check_chrome_instance():
            #     os.system("taskkill /f /im chrome.exe")
            # else:
            #     pass
            print("Checking server status...")
            time.sleep(10)
    except:
        print("Something is going wrong here...")


def main():
    """Main function to run the automation script."""
    print(pyfiglet.figlet_format("Welcome to the automation script!"))
    print('?')

    # Validate and load environment variables
    email, password = check_initialization()

    driver = Driver(uc=True, headless=False)
    driver.set_page_load_timeout = 200

    # Initialize login and server data
    driver = login_website(driver, email, password)
    driver, server_dictionary, server_data = selecting_servers(driver)
    # while True:
    #     try:

    #         if not server_data:
    #             print("Retrying login...")
    #             driver.quit()
    #             continue

    #         print("Server data fetched successfully.")
    #         break

    #     except Exception as e:
    #         print(f"Error: {e}")
    #         if driver:
    #             driver.quit()
    #         raise

    # Main loop for server automation
    try:
        while True:
            asc_time = check_time()
            print(f"Current time: {asc_time}")
            print(f"DRIVER: {driver}")
            driver = server_automation(driver, server_dictionary, server_data, asc_time)
    except KeyboardInterrupt:
        exit("Exiting the automation script...")


if __name__ == "__main__":
    main()