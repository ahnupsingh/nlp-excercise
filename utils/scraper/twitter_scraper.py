from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from dotenv import load_dotenv
import os
import csv
from .base import Scraper
from django.conf import settings

class TwitterScraper(Scraper):
    def __init__(self):
        self.username = settings.TWITTER_USERNAME
        self.password = settings.TWITTER_PASSWORD
        self.driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()), options=Options()
        )
        self.login_url = "https://x.com/i/flow/login"
        self.driver.get(self.login_url)

    def scrape(self, text):
        pass
    
    def scroll_down(self):
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)

    def get_search_query(self, key):
        search_queries = {
            "2024_#indianrailways": "(#indianrailways) since:2024-01-01 -filter:links -filter:replies",
            "2024_indianrail": "(indianrailways) since:2024-01-01 -filter:links -filter:replies",
            "2024_railmin": "(@RailMinIndia) since:2024-01-01 -filter:links -filter:replies",
        }
        search_query = search_queries.get(key)
        if not search_query:
            raise ValueError("No search query available for the specified year")
        return search_query

    def get_tweet_for_year(self, year):
        search_query = self.get_search_query(year)
        self.driver.get(self.login_url)
        time.sleep(5)

        email_field = self.driver.find_element(
            By.XPATH,
            '//*[@id="layers"]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/div[4]/label/div/div[2]/div/input',
        )

        print(email_field)
        email_field.send_keys(self.username)

        next_button = self.driver.find_element(
            By.XPATH,
            '//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/button[2]',
        )
        print(next_button)

        next_button.click()
        time.sleep(5)
        password_field = self.driver.find_element(
            By.XPATH,
            '//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div/div[3]/div/label/div/div[2]/div[1]/input',
        )
        password_field.send_keys(self.password)
        time.sleep(5)
        login_button = self.driver.find_element(
            By.XPATH,
            '//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[2]/div/div[1]/div/div/button',
        )
        login_button.click()
        # Maximize the window
        self.driver.maximize_window()

        time.sleep(5)
        # after login

        search_button = self.driver.find_element(
            By.XPATH,
            '//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div[2]/div/div[2]/div/div/div/div[1]/div/div/div/form/div[1]/div/div/div/div/div[2]/div/input',
        )
        search_button.send_keys(
            search_query,
            Keys.ENTER,
        )
        time.sleep(10)

        # tweet_set = set() # Store each concatenated span text in this list
        tweet_dict = {}
        # 50 scrolls
        for i in range(17):
            print("scroll count", i)
            print("tweet counts:", len(tweet_dict))
            elements = self.driver.find_elements(By.CSS_SELECTOR, "div[data-testid='tweetText']")
            for element in elements:
                # Get the value of the 'id' attribute
                element_id = element.get_attribute("id")
                # print(element_id)
                # Get the text content of the element
                element_text = element.text
                # tweet_set.add(element_text)
                tweet_dict[element_id] = element_text
                if len(tweet_dict) > 200:
                    break
            self.scroll_down()

        # Write data to CSV after collecting all tweets
        # Set the directory path based on the year
        directory_path = f"output/year_wise_data_2024"

        # Check if the directory exists, and if not, create it
        if not os.path.exists(directory_path):
            os.makedirs(directory_path)

        # Path to the CSV file
        file_path = f"{directory_path}/{year}_data.csv"
        with open(file_path, "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["index", "text", "year"])  # Corrected header row
            for index, (tweet_id, tweet_text) in enumerate(tweet_dict.items(), start=1):
                writer.writerow([index, tweet_text, year])

        self.driver.quit()