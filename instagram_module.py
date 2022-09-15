from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from settings import data
import time
import random


class InstagramBot:
    def __init__(self, username: str, password: str, path_chrome_driver: str = "chrome_driver/chromedriver"):
        self.__username = username
        self.__password = password
        path_driver = Service(path_chrome_driver)
        options = webdriver.ChromeOptions()
        self.browser = webdriver.Chrome(service=path_driver, options=options)
        self.wrong_user_page = '/html/body/div[1]/div/div/div/div[1]/div/div/div/div[1]/section/main/div/div/div/h2'
        self.like_button = '/html/body/div[1]/div/div/div/div[1]/div/div/div/div[1]/section/main/div[1]/div[1]/\n' \
                           'article/div/div[2]/div/div[2]/section[1]/span[1]/button'

    def close_browser(self):
        self.browser.close()
        self.browser.quit()

    def login(self):

        try:
            browser = self.browser
            browser.get('https://www.instagram.com')
            time.sleep(random.randrange(3, 5))

            login_input = browser.find_element(By.NAME, 'username')
            login_input.clear()
            login_input.send_keys(self.__username)

            time.sleep(3)

            password_input = browser.find_element(By.NAME, 'password')
            password_input.clear()
            password_input.send_keys(self.__password)

            password_input.send_keys(Keys.ENTER)
            time.sleep(10)

        except Exception as ex:
            print(f"Authorization failed with this mistake: {ex}")
            self.close_browser()

    def like_photo_by_hashtag(self, hashtag: str, number_posts: int, scroll_number: int = 5):
        """Like photos with chosen hashtag"""

        try:
            browser = self.browser
            browser.get(f'https://www.instagram.com/explore/tags/{hashtag}/')
            time.sleep(5)

            posts_urls = []
            for _ in range(1, scroll_number):
                browser.execute_script('window.scrollTo(0, document.body.scrollHeight);')
                time.sleep(random.randrange(3, 5))
                hrefs = browser.find_elements(By.TAG_NAME, 'a')
                for link in hrefs:
                    if '/p/' in link.get_attribute('href'):
                        if link.get_attribute('href') not in posts_urls:
                            posts_urls.append(link.get_attribute('href'))

            for url in posts_urls[0:number_posts]:
                try:
                    browser.get(url)
                    time.sleep(3)
                    browser.find_element(By.XPATH, self.like_button).click()
                    time.sleep(random.randrange(80, 95))
                except Exception as ex:
                    print(f"Like don't sent, mistake in like_photo_by_hashtag method: {ex}")
                    continue

        except Exception as ex:
            print(f"Mistake in like_photo_by_hashtag method: {ex}")
            self.close_browser()

    def xpath_checker(self, xpath_url: str) -> bool:
        """Check xpath_url on page and return True or False"""

        browser = self.browser
        try:
            browser.find_element(By.XPATH, xpath_url)
            exist = True
        except NoSuchElementException:
            exist = False
        return exist

    def put_like_from_url(self, post_url: str):
        """Send like for post_url"""

        browser = self.browser
        browser.get(post_url)
        time.sleep(4)

        wrong_user_page = self.wrong_user_page
        if self.xpath_checker(wrong_user_page):
            print('Mistake url, in method "put_like_from_url"')

        else:
            print('Start liking')
            time.sleep(2)

            browser.find_element(By.XPATH, self.like_button).click()
            time.sleep(5)

            print(f'Like on post {post_url} sent')
            self.close_browser()

    def put_many_likes_for_person(self, user_url: str):
        """Send likes for posts in profile -> user_url"""

        browser = self.browser
        browser.get(user_url)
        time.sleep(4)

        wrong_user_page = self.wrong_user_page
        if self.xpath_checker(wrong_user_page):
            print('Not valid user_url, in method put_many_likes_for_person')
            self.close_browser()
        else:
            print(f'Find profile {user_url}, ready send likes')
            time.sleep(2)

            posts_count = int(browser.find_element(By.XPATH, '/html/body/div[1]/div/div/div/div[1]/div/div/div/div[1]\n'
                                                             '/section/main/div/header/section/ul/li[1]/div/span').text)
            loops_count = int(posts_count / 12)

            posts_urls = []
            for i in range(0, loops_count):
                hrefs = browser.find_elements(By.TAG_NAME, 'a')
                hrefs = [item.get_attribute('href') for item in hrefs if '/p/' in item.get_attribute('href')]

                for link in hrefs:
                    posts_urls.append(link)

                browser.execute_script('window.scrollTo(0, document.body.scrollHeight);')
                time.sleep(random.randrange(3, 5))
                print(f"Iteration {i + 1}")

            set_posts_url = set(posts_urls)
            unique_posts_url = list(set_posts_url)
            file_name = user_url.split('/')[-2]

            with open(f'{file_name}.txt', 'w') as file:
                for post_url in unique_posts_url:
                    file.write(post_url + '\n')

            with open(f'{file_name}.txt') as file:
                urls_list = file.readlines()

                try:
                    for post_url in urls_list[0:3]:
                        browser.get(post_url)
                        time.sleep(2)

                        browser.find_element(By.XPATH, self.like_button).click()
                        time.sleep(random.randrange(80, 95))

                except Exception as ex:
                    print(f"Mistake in method 'put_many_likes_for_person' during liking posts: {ex}")
                    self.browser.close()

            self.close_browser()

    def send_message(self, username: str, message: str):

        browser = self.browser
        time.sleep(random.randrange(2, 4))
        close_notifications = '/html/body/div[1]/div/div/div/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[3]/button[2]'
        browser.get('https://www.instagram.com/direct/inbox/')

        if self.xpath_checker(close_notifications):
            browser.find_element(By.XPATH, close_notifications).click()
            print('Close notifications mistake')

        direct_button = '/html/body/div[1]/div/div/div/div[1]/div/div/div/div[1]/div[1]/section/div/div[2]/div/div/div[2]/div/div[3]/div/button'
        WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, direct_button)))
        message_send = browser.find_element(By.XPATH, direct_button).click()
        print('Send message...')
        time.sleep(random.randrange(2, 4))
        find_user = browser.find_element(By.XPATH, '/html/body/div[1]/div/div/div/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div[2]/div[1]/div/div[2]/input')
        find_user.send_keys(username)
        time.sleep(random.randrange(2, 5))

        user_list = browser.find_element(By.XPATH, '/html/body/div[1]/div/div/div/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div[2]/div[2]').find_element(By.TAG_NAME, 'button').click()
        time.sleep(random.randrange(2, 5))

        next_button = browser.find_element(By.XPATH, '/html/body/div[1]/div/div/div/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div[1]/div/div[3]/div/button').click()
        time.sleep(random.randrange(2, 5))

        text_area = browser.find_element(By.XPATH, '/html/body/div[1]/div/div/div/div[1]/div/div/div/div[1]/div[1]/section/div/div[2]/div/div/div[2]/div[2]/div/div[2]/div/div/div[2]/textarea')
        text_area.clear()
        text_area.send_keys(message)
        time.sleep(random.randrange(2, 5))
        text_area.send_keys(Keys.ENTER)
        print(f"Сообщение для {username} успешно отправлено!")

        time.sleep(5)
        self.close_browser()


insta_bot = InstagramBot(data.login_instagram, data.password_instagram)
insta_bot.login()
insta_bot.send_message('teztour_by', 'Hello')

