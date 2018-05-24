#!/usr/bin/env python3.5

# RUN:
#    ./gran_turismo_datalogger.py https://www.twitch.tv/videos/264031046?t=3m35s

import argparse
import random

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import time, sleep

def main():
    args = parse_args()
    open_broadcast()
    wait_for_online(args)

def wait_for_online():
    """
    wait until broadcast comes online
    """
    poll_time = 10 # seconds between "is online?" checks

    # I will sometimes refresh browser.
    # it's a defense against buffering or memory leak problems
    # (with twitch/chrome) that may or may not arise
    next_restart = time() + (random.randint(30, 120) * 60) # after 30 to 120 min

    while broadcast_is_offine():
        sleep(poll_time)
        if time() >= next_restart:
            close_broadcast()
            sleep(5)
            open_broadcast()
            next_restart = time() + (random.randint(30, 120) * 60)

    # now broadcast is online so we will wait until player
    # goes to a screen that indicates he is going to some track
    wait_for_track_indication()

def wait_for_track_indication():
    pass

def test():
    args = parse_args()
    print(args)
    driver = open_broadcast(args.BROADCAST)
    sleep(999999999999)
    #sleep(2)
    #close_broadcast(driver)

def open_broadcast(broadcast):
    driver = webdriver.Chrome()
    print("b:", broadcast)
    driver.get(broadcast)
    elem = driver.find_element_by_class_name(
            "pl-button__fullscreen--tooltip-left")
    elem.click()
    return driver

def close_broadcast(driver):
    driver.close()

def parse_args():
    parser = argparse.ArgumentParser()
    parser.description = ("Launch the gran turismo sport datalogger. Launches "
            "chromedriver to watch a twitch broadcast and analyses what's "
            "happening and writes lap times to data.log")
    parser.add_argument("BROADCAST",
            help="http link to a twitch broadcast of GT sport gameplay")
    args = parser.parse_args()
    return args

if __name__ == "__main__":
    #main()
    test()
