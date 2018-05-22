#!/usr/bin/env python3

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

driver = webdriver.Chrome()
driver.get("https://www.twitch.tv/videos/264031046")
#assert "Python" in driver.title
elem = driver.find_element_by_class_name("pl-button__fullscreen--tooltip-left")
#elem = driver.find_element_by_name("q")
elem.click()
#elem.send_keys("pycon")
#elem.send_keys(Keys.RETURN)
#assert "No results found." not in driver.page_source
sleep(10)
driver.close()

# <button class="player-button qa-fullscreen-button pl-mg-r-1 pl-button__fullscreen--tooltip-left" id="" tabindex="-1" type="button"><span><span class="player-tip" data-tip="Fullscreen"></span><span class=""><svg id="icon_fullscreen" viewBox="0 0 30 30" xmlns="http://www.w3.org/2000/svg"><path d="M7,7 L15.2,7 L12.8,9.4 L15.8,12.4 L12.4,15.8 L9.4,12.8 L7,15.2 L7,7 Z M23,23 L14.8,23 L17.2,20.6 L14.2,17.6 L17.6,14.2 L20.6,17.2 L23,14.8 L23,23 Z"></path></svg></span></span></button>
