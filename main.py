from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import os,time
import random

load_dotenv()

EMAIL_ADDRESS = os.getenv('EMAIL_ADDRESS')
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')
TARGET_ACCOUNT = os.getenv('TARGET_ACCOUNT')

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)

user_data_dir = os.path.join(os.getcwd(), "chrome_profile")

chrome_options.add_argument(f"--user-data-dir={user_data_dir}")
CHROME_DRIVER_PATH = "C:/Users/Hi/Downloads/chromedriver-win64/chromedriver-win64"


class InstagramBot:
    def __init__(self):
        self.driver = webdriver.Chrome(options=chrome_options)
        self.wait = WebDriverWait(self.driver,10)
        self.actions = ActionChains(self.driver)

    def login(self):
        """
        logs in to the account
        :return:
        """
        self.driver.get('https://www.instagram.com/accounts/login/')

        try:

            # GETTING THE ELEMENT
            inputs = self.driver.find_elements(By.TAG_NAME,"input")
            email_text_box = inputs[0]
            password_text_box = inputs[1]

            # FILLING THE EMAIL IN THE EMAIL FIELD
            email_text_box.send_keys(EMAIL_ADDRESS)

            # FILLING THE PASSWORD IN THE PASSWORD FIELD
            password_text_box.send_keys(EMAIL_PASSWORD)

            # CLICKING THE LOGIN BUTTON
            login_button = self.driver.find_element(By.XPATH,'//*[@id="login_form"]/div/div[1]/div/div[3]/div/div')
            login_button.click()


        except:
            print("already logged in")

        #   SAVING CREDENTIAL POPUP

        try:
            # WAITING FOR THE POP TO APPEAR
            not_now_button = self.wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="mount_0_0_Qp"]/div/div/div[2]/div/div/div[1]/div[1]/div[1]/section/main/div/div/div/div')))
            not_now_button.click()
        except:
            print("pop not appeared")

    def find_followers(self):
        """
        Finds the followers to follow
        :return:
        """

        # FINDING THE SEARCH BUTTON AND CLICKING IT
        search_element = self.wait.until(EC.element_to_be_clickable((By.XPATH,"//*[local-name()='svg' and @aria-label='Search']/ancestor::a")))
        search_element.click()

        # FINDING THE SEARCH BAR AND ENTERING THE NAME
        search_bar = self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR,"input[aria-label='Search input']")))

        ## clearing the text inside the search bar
        search_bar.clear()

        ## sending the target name in the search bar
        search_bar.send_keys(TARGET_ACCOUNT)

        # PRESSING THE ENTER TO SEARCH
        search_bar.send_keys(Keys.ENTER)

        # SELECTING THE CORRECT PROFILE AND CLICKING IT
        profile = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,f"a[href*='/{TARGET_ACCOUNT}/']")))
        profile.click()

        # CLICKING THE FOLLOWERS BUTTON ON THE PROFILE
        followers_button = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,f"a[href*='/{TARGET_ACCOUNT}/followers/']")))
        followers_button.click()

    def follow(self):
        """
        follows the found followers
        :return:
        """
        x_path_variable = "//button[.//div[text()='Follow']]"

        # WAITING FOR THE SPINNING CIRCLE TO DISAPPEAR
        self.wait.until(EC.invisibility_of_element_located((By.CSS_SELECTOR, "div[data-visualcompletion='loading-state']")))

        # FINDING THE BUTTONS
        follow_elements = self.wait.until(EC.presence_of_all_elements_located((By.XPATH,x_path_variable)))

        # PRESSING EACH BUTTONS
        for btn in follow_elements:

            try:
                # FORCE CLICKING THE BUTTON USING JAVASCRIPT
                self.driver.execute_script('arguments[0].click();',btn)
                print("successfully followed")

                # USING TIMER TO ACT AS A HUMAN
                # timer = random.randint(1,5)
                time.sleep(10)

            except Exception as e:
                print(f"error: {e}")
                print("failed to follow")


bot = InstagramBot()

# logging in to the instagram
bot.login()

# Finding the followers
bot.find_followers()

# Following the followers
bot.follow()