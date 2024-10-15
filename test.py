from selenium import webdriver
from selenium.common.exceptions import *
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep
import csv, random

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

url = 'https://debank.com/ranking?page='
page_num = 200

for page_id in range(92, page_num + 1):
    driver.get(url + str(page_id))
    driver.implicitly_wait(5)

    users = driver.find_elements(By.CSS_SELECTOR, 'div.db-table-row')
    for user in users:
        user_id = user.find_element(By.CSS_SELECTOR, 'div.db-table-cell:nth-child(1)').text
        user_name_element = user.find_element(By.CSS_SELECTOR, 'div.db-table-cell:nth-child(2)').find_element(By.CSS_SELECTOR, 'div.db-user-content')
        user_name = user_name_element.text
        user_networth = user.find_element(By.CSS_SELECTOR, 'div.db-table-cell:nth-child(3)').text
        user_tvf = user.find_element(By.CSS_SELECTOR, 'div.db-table-cell:nth-child(4)').text.split('\n')[0]
        user_followers = user.find_element(By.CSS_SELECTOR, 'div.db-table-cell:nth-child(4)').text.split('\n')[1]

        actions = ActionChains(driver)
        actions.move_to_element(user_name_element).perform()
        sleep(0.5)
        social_links = driver.find_elements(By.TAG_NAME, 'a')
        for social_link in social_links:
            link = social_link.get_attribute('href')
            if link != None:
                if link.startswith('https://x.com/') and link != 'https://x.com/':
                    output = [user_id, user_name, link, user_networth, user_tvf, user_followers]

                    print(output)
                    open_out = open(f'twitter.csv','a',newline="", encoding='utf-8-sig')
                    file_o_csv = csv.writer(open_out, delimiter=',')
                    file_o_csv.writerow(output)
                    open_out.close()
                    break
        driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.ESCAPE)
        sleep(0.2)
    sleep(random.uniform(3, 8))