from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time, random

class Unsaver:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.posts = []
        self.post_links = set()

        options = Options()
        options.add_argument("--headless") # No browser UI
        ch = input("Do you need the browser to show during automation(y/n): ").strip().lower()
        if(ch == 'y'): 
            self.driver = webdriver.Chrome()
        elif(ch == 'n'):
            self.driver = webdriver.Chrome(options=options)
        else:
            print("Invalid choice!, try again!")
            exit()
    
    def human_sleep(self, min_sec = 1, max_sec = 2):
        time.sleep(random.uniform(min_sec, max_sec))
    
    def initialize(self):
        self.driver.get("https://www.instagram.com/accounts/login/")
        self.human_sleep(4, 6)

        try:
            uname_input = self.driver.find_element(By.NAME, "username")
            pass_input = self.driver.find_element(By.NAME, "password")
            uname_input.send_keys(self.username)
            pass_input.send_keys(self.password)
            pass_input.send_keys(Keys.RETURN)
            self.human_sleep(8, 12)

            if "login" in self.driver.current_url and "factor" not in self.driver.current_url:
                print("Login may have failed. Still on login page. Check login credentials and try again.")
                self.driver.quit()
                exit()

            print("Logged in successfully.")    
        except Exception as e:
            print("Login error occured: {}".format(e))
            self.driver.quit()
            exit()

    def handle_2fa(self):
        try:
            code_input = self.driver.find_element(By.NAME, "verificationCode")
            code = input("Enter Instagram 2FA code: ")
            code_input.send_keys(code);
            code_input.send_keys(Keys.RETURN)
            print("2FA done!")
            self.human_sleep(8, 12)
        except Exception as e:
            print("No 2FA available to validate!")
    
    def load(self):
        print("Collecting saved posts...")
        self.driver.get("https://www.instagram.com/{}/saved/all-posts".format(self.username))
        self.human_sleep(4, 6)

        last_height = self.driver.execute_script("return document.body.scrollHeight")
        while True:
            self.posts = self.driver.find_elements(By.CSS_SELECTOR, "a[href*='/p/']")
            for post in self.posts:
                link = post.get_attribute("href")
                if link:
                    self.post_links.add(link)
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            self.human_sleep(1.5, 2.5)
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height
        self.posts = list(self.post_links)

    def unsave(self):
        print("Total posts to unsave: {}".format(len(self.posts)))
        for index, post in enumerate(self.posts):
            self.driver.get(post)
            self.human_sleep(2, 4)
            try:
                save_button = self.driver.find_element(By.CSS_SELECTOR, "svg[aria-label='Remove']").find_element(By.XPATH, "./../..")
                save_button.click()
                print("[{}/{}] Unsaved post: {}".format(index + 1, len(self.posts), post))
            except Exception as e:
                print("[{}/{}]Could not unsave post: {}: {}".format(index + 1, len(self.posts), post, e))
            self.human_sleep(2, 3)

    def __del__(self):
        self.driver.quit()

def main():
    print(r"""
             _           _
            (_)_ __  ___| |_ __ _       _   _ _ __  ___  __ ___   _____ _ __
            | | '_ \/ __| __/ _` |_____| | | | '_ \/ __|/ _` \ \ / / _ \ '__|
            | | | | \__ \ || (_| |_____| |_| | | | \__ \ (_| |\ V /  __/ |
            |_|_| |_|___/\__\__,_|      \__,_|_| |_|___/\__,_| \_/ \___|_|

                
    """)
    username = input("Enter Instagram username: ")
    password = input("Enter Instagram password: ")
    bot = Unsaver(username, password)
    bot.initialize()
    bot.handle_2fa()
    bot.load()
    bot.unsave()
    print("Unsaving process completed!!")

if __name__ == "__main__":
    main()