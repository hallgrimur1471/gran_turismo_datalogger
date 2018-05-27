#!/usr/bin/env python3.5

# RUN:
#    ./gran_turismo_datalogger.py https://www.twitch.tv/videos/264031046?t=3m39s

import os
from os.path import abspath, dirname
import random
import argparse
import subprocess

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import mss
import mss.tools
from time import time, sleep

def main():
    change_working_directory_to_datalogger()
    args = parse_args()
    driver = open_broadcast()
    wait_for_online(args)

def change_working_directory_to_datalogger():
    this_scripts_file = abspath(__file__)
    this_scripts_directory = dirname(this_scripts_file)
    os.chdir(this_scripts_directory)

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
            debug("restarting browser")
            close_broadcast()
            sleep(5)
            open_broadcast()
            next_restart = time() + (random.randint(30, 120) * 60)

    # now broadcast is online so we will wait until player
    # goes to a screen that indicates he is going to some track
    wait_for_track_indication()

def broadcast_is_offline():
    # TODO: implement
    return False

def wait_for_track_indication():
    # exit symbol:
    #     x: 984, y: 821, w:47,  h:48
    with mss.mss() as sct:

        # When you go to time trial, before you go to track
        # there is this red exit symbol, see examplars/exit.png
        exit_diff = look_for_exit_symbol(sct)

        exit_diff_thershold = 96
        if exit_diff > exit_diff_threshold:
            pass
            # the exit_symbol is probably there

        time = {"top": 11, "left": 97, "width": 36, "height": 15}
        trial = {"top": 10, "left": 134, "width": 31, "height": 15}
        #exit = {"top": 984, "left": 821, "width": 47, "height": 48}
        exit = {"top": 826, "left": 989, "width": 47, "height": 48}
        time_imgs = []
        trial_imgs = []
        exit_imgs = []
        play_mario()
        for i in range(1000):
            #time_imgs.append(sct.grab(time))
            #trial_imgs.append(sct.grab(trial))
            exit_imgs.append(sct.grab(exit))
            sleep(0.03)
        play_mario()
        #for i, image in enumerate(time_imgs):
        #    mss.tools.to_png(image.rgb, image.size,
        #                     output="time{}.png".format(str(i).zfill(3)))
        #for i, image in enumerate(trial_imgs):
        #    mss.tools.to_png(image.rgb, image.size,
        #                     output="trial{}.png".format(str(i).zfill(3)))
        for i, image in enumerate(exit_imgs):
            mss.tools.to_png(image.rgb, image.size,
                             output="exit{}.png".format(str(i).zfill(3)))

def look_for_exit_symbol():
    exit = {"top": 826, "left": 989, "width": 47, "height": 48}
    img = sct.grab(exit)
    mss.tools.to_png(img.rgb, img.size, output="exit.png")
    examplar = "./exemplars/exit.png"
    diff = subprocess.run(
        "./img_diff_test.py {} ./img/{}".format(img, exemplar),
        stdout=PIPE, shell=True).stdout.decode().rstrip()
    diff = float(diff)
    return diff


def play_mario():
    #subprocess.run(["play", "./mario_coin.wav", ">", "/dev/null", "2>&1"])
    #subprocess.Popen("play ./mario_coin.wav > /dev/null 2>&1", shell=True)
    subprocess.run("play ./mario_coin.wav > /dev/null 2>&1", shell=True)

#with mss.mss() as sct:
#    #monitor = {"top": 160, "left": 160, "width": 200, "height": 200}
#    monitor = {"top": 0, "left": 0, "width": 1600, "height": 900}
#    output = "sct-{top}x{left}_{width}x{height}.png".format(**monitor)
#
#    last_time = time()
#    while True:
#        sct_img = sct.grab(monitor)
#        new_time = time()
#        print(new_time - last_time)
#        last_time = time()
#    print(sct_img.__dict__)
#    print(len(sct_img.raw)/4)
#
#    mss.tools.to_png(sct_img.rgb, sct_img.size, output=output)
#    print(output)

def get_snip(x, y, w, h):
    pass

def test():
    try:
        change_working_directory_to_datalogger()
        args = parse_args()
        driver = open_broadcast(args.BROADCAST)
        sleep(8)
        wait_for_track_indication()
    except:
        raise
    finally:
        close_broadcast(driver)

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
