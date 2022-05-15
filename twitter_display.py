import os

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

import datetime
import time
import pathlib

options = webdriver.ChromeOptions()
options.add_experimental_option("useAutomationExtension", False)
options.add_experimental_option("excludeSwitches", ["enable-automation", "hide-scrollbars", "smooth-scrolling"])


script_directory = pathlib.Path().absolute()

options.add_argument(f"user-data-dir={script_directory}/user_data")

browser = webdriver.Chrome(executable_path=r'./chromedriver.exe', options=options)

browser.get("https://www.twitter.com/cantmera")  # Go to twitter
if 'nt' in os.name.lower():
    browser.maximize_window()
else:
    browser.fullscreen_window()  # Maximize the window

# hide blue bar
# blue_bar = browser.find_element(By.XPATH, r'//*[@id="layers"]/div')

blue_bar = None
header = None
sidebar = None
timeline_container = None
timeline = None
timeline_center = None
timeline_center2 = None
primary_column = None
primary_column2 = None
while sidebar is None:
    try:
        blue_bar = browser.find_element(By.XPATH, '//*[@id="layers"]/div')
        header = browser.find_element(By.XPATH, '//*[@id="react-root"]/div/div/div[2]/header')
        sidebar = browser.find_element(By.XPATH, '/html/body/div[1]/div/div/div[2]/main/div/div/div/div[2]')
        timeline = browser.find_element(By.XPATH, '//*[@id="react-root"]/div/div/div[2]/main')
        timeline_container = browser.find_element(By.XPATH, '//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div[1]')
        timeline_center = browser.find_element(By.XPATH, '//*[@id="react-root"]/div/div/div[2]/main/div')
        timeline_center2 = browser.find_element(By.XPATH, '//*[@id="react-root"]/div/div/div[2]/main/div/div/div')
        primary_column = browser.find_element(By.XPATH, '//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div[1]/div/div[2]/div/div')
        primary_column2 = browser.find_element(By.XPATH,
                                              '//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div[1]')
    except:
        # print("Not there yet...")
        pass
browser.execute_script("arguments[0].style.display = 'none';", sidebar)
browser.execute_script("arguments[0].style.display = 'none';", header)
browser.execute_script("arguments[0].style.display = 'none';", blue_bar)
browser.execute_script("arguments[0].style.alignItems = 'center';"
                       "arguments[0].style.width = '100vw';", timeline)
browser.execute_script("arguments[0].style.width = '500vw';", timeline_container)
browser.execute_script("arguments[0].style.width = '100vw';", timeline_center)
browser.execute_script("arguments[0].style.justifyContent = 'center';", timeline_center2)
browser.execute_script("arguments[0].classList.remove('r-1ye8kvj');", primary_column)
browser.execute_script("arguments[0].classList.remove('r-1ye8kvj');", primary_column2)
browser.execute_script("arguments[0].style.maxWidth = '80vw';", primary_column2)

# Add some new CSS
browser.execute_script('document.styleSheets[0].addRule("::-webkit-scrollbar", "display: none;")')

# hide sidebar
# sidebar = browser.findElement(By.xpath("//div[@data-testid='sidebarColumn']"))
# browser.execute_script("document.html.style.cssText += '::-webkit-scrollbar { display: none; }')")

prev_tweet_value = ""
topics = None
links = None

with open("smooth_scroll.js", "r") as f:
    script = f.read()
    f.close
# browser.execute_script("document.body.style.scrollBehavior = 'smooth'")
browser.execute_script("localStorage.setItem('scroll', false)")
browser.execute_script(script)
# browser.execute_script("setInterval(function () {(window.scrollByPages(1))}, 100);")
while True:
    # current_scroll = int(browser.execute_script("return window.pageYOffset"))
    # inner_height = int(browser.execute_script("return window.innerHeight"))
    # offset_height = int(browser.execute_script("return document.body.offsetHeight"))
    # browser.execute_script("window.scrollBy({top: 3, behavior: 'slow'})")

    # browser.execute_script(script)

    time.sleep(10)
    #/parent::*/parent::*/parent::*
    try:
        topics = browser.find_element(By.XPATH, '//*[@id="react-root"]//*[text()[contains(.,"Topics")]]/parent::div/parent::div/parent::div')
        links = browser.find_element(By.XPATH,
                                      '//*[@id="react-root"]//*[contains(@aria-labelledby, "accessible-list")]/div[contains(@aria-label, "Timeline")]/nav/parent::div/parent::section/parent::div/parent::div[contains(@style, "transform")]')
        # print(f"FOUND: {topics}")
    except:
        print("Not Found!")
        pass

    if topics is not None:
        browser.execute_script("if (arguments[0].style.display != 'none') { arguments[0].style.display = 'none'; }", topics)
        topics = None

    if links is not None:
        browser.execute_script("if (arguments[0].style.display != 'none') { arguments[0].style.display = 'none'; }", links)
        links = None

    elem = browser.find_element(By.XPATH, "/html/body/div[1]/div/div/div[2]/main/div/div/div/div[1]/div/div[1]/div[1]/div/div/div/div/div[2]/div/div")
    e_value = elem.get_attribute("innerHTML")
    if prev_tweet_value != e_value:
        prev_tweet_value = e_value
        browser.execute_script("localStorage.setItem('scroll', 'true'); window.scrollTo({top: 0, behavior: 'smooth'}); setTimeout(function () {localStorage.setItem('scroll', 'false')}, 3000);")
