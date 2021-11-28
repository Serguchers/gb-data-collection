import json
import time

from lxml import html
from selenium import webdriver
from selenium.common import exceptions
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

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

time.sleep(5)
elem = driver.find_element(By.CLASS_NAME, "js-letter-list-item")
actions.move_to_element(elem)


check_list = []
actions.send_keys(Keys.DOWN)
actions.perform()

flag = True
counter = 0
while flag:
    current_state = len(check_list)

    actions.send_keys(Keys.PAGE_DOWN).perform()

    working_space = driver.page_source
    working_space = html.fromstring(working_space)
    data = working_space.xpath('//a[contains(@href, "/inbox/0")]')
    for i in data:
        link = "".join(i.xpath("./@href"))
        if link not in check_list:
            check_list.append(link)

    if current_state == len(check_list):
        counter += 1
        if counter == 2:
            break
    time.sleep(1)


with open("Homework - 5\mail-data.json", "w") as f:
    json.dump(check_list, f)
print()
