import json
import time
from pprint import pprint

from pymongo import MongoClient
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

client = MongoClient("127.0.0.1", 27017)
db = client["email_link_data"]
emails = db.emails


driver = webdriver.Firefox(executable_path="../geckodriver")
# driver.implicitly_wait(10)
driver.get("https://mail.ru")
wait = WebDriverWait(driver, 20)
actions = ActionChains(driver)
driver.implicitly_wait(10)

driver.maximize_window()


elem = driver.find_element(By.NAME, "login")
elem.send_keys("study.ai_172@mail.ru")

elem = driver.find_element(By.XPATH, '//button[@data-testid="enter-password"]')
elem.click()


# elem = driver.find_element(By.NAME, 'password')
elem = wait.until(EC.element_to_be_clickable((By.NAME, "password")))
elem.send_keys("NextPassword172#")

elem = driver.find_element(By.XPATH, '//button[@data-testid="login-to-mail"]')
elem.click()

base_url = "https://e.mail.ru"
link_data = []

with open("./mail-data.json", "r") as f:
    data = json.load(f)

print(len(data))

for i in range(50):
    email_info = {}
    email = driver.get(base_url + data[i])

    time.sleep(1)

    subject = driver.find_element(By.CLASS_NAME, "thread__subject").text
    send_by = driver.find_element(By.CLASS_NAME, "letter-contact").text
    datetime = driver.find_element(By.CLASS_NAME, "letter__date").text
    content = driver.find_element(By.CLASS_NAME, "letter__body").text

    email_info["subject"] = subject
    email_info["send_by"] = send_by
    email_info["datetime"] = datetime
    email_info["content"] = content

    link_data.append(email_info)


for email in link_data:
    emails.insert_one(email)
