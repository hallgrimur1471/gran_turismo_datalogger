#!/usr/bin/env python3.5

# RUN:
#  ./gran_turismo_datalogger.py https://www.twitch.tv/videos/275549220?t=18m01s

"""
Documentation links:
    Python 3.5:
        https://docs.python.org/3.5/
    Pillow (PIL):
        https://pillow.readthedocs.io/en/5.1.x/reference/index.html
    MSS:
        http://python-mss.readthedocs.io/api.html
    Selenium:
        docs: https://docs.seleniumhq.org/docs/
        handbook (WIP): https://seleniumhq.github.io/docs/
        api: https://seleniumhq.github.io/selenium/docs/api/py/api.html
"""

import os
from os.path import abspath, dirname
import sys
import random
import argparse
import subprocess
from time import time, sleep
import math

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import mss
import mss.tools
import PIL as pil
from PIL import Image

def main():
    args = parse_args()
    cd_to_project_root()
    data_logger = DataLogger()
    data_logger.start()

def test():
    args = parse_args()
    cd_to_project_root()
    data_logger = DataLogger(args.BROADCAST)
    try:
        data_logger.start()
    finally:
        data_logger.stop()

def test2():
    cd_to_project_root()
    exemplar_image = Image.open("./exemplars/exit.png")
    similar_image = Image.open("./tests/img/exit_unsimilar.png")
    comparison = ImageCompare(exemplar_image, similar_image)
    print(comparison.similarity())

def parse_args():
    parser = argparse.ArgumentParser()
    parser.description = ("Launch the gran turismo sport datalogger. Launches "
            "chromedriver to watch a twitch broadcast and analyses what's "
            "happening and writes lap times to data.log")
    parser.add_argument("BROADCAST",
            help="http link to a twitch broadcast of GT sport gameplay")
    args = parser.parse_args()
    return args

class DataLogger():
    """
    Monitors gran turismo spors gameplay broadcast, analyzes what's happening
    and logs lap times

    Note:
        This class uses relative paths. Your working directory must be
        gran_turismo_datalogger for this class to work.

    API:
        self.start()
        self.close()
    """

    def __init__(self, broadcast):
        """
        Args:
            broadcast (str): Link to a twitch broadcast
                             example: 
                             https://www.twitch.tv/videos/264031046?t=3m39s
        """
        self._broadcast = broadcast
        self._browser = webdriver.Chrome()
        self._screen = None
        self._screen_resolution = None

        self._has_seen_track_pre_stage_indication = False

    @property
    def broadcast():
        return self._broadcast

    def start(self):
        self._change_working_directory_to_datalogger()
        self._open_broadcast()
        with mss.mss() as screen:
            self._screen = screen
            self._verify_screen_resolution()
            self._wait_for_online()

    def stop(self):
        pass
        self._browser.quit()

    def _verify_screen_resolution(self):
        """
        Checks resolution of screen, throws error if resolution not supported
        """
        supported_resolutions = [(1600, 900)]

        monitor = self._screen.monitors[1:][0]
        resolution = (monitor["width"], monitor["height"])
        if resolution not in supported_resolutions:
            raise RuntimeError(
                    "Current screen resolution not supported, this application "
                    "monitors your screen using hard coded pixel positions and "
                    "therefor only few resolutions are supported. Please try "
                    "changing your display settings to one of the supported "
                    "resolutions: "+str(supported_resolutions))

        self._screen_resolution = resolution

    def _open_broadcast(self):
        self._browser.get(self._broadcast)
        elem = self._browser.find_element_by_class_name(
                "pl-button__fullscreen--tooltip-left")
        elem.click()

    def _close_broadcast(self):
        self._browser.close()

    def _wait_for_online(self):
        """
        wait until broadcast comes online
        """
        poll_time = 10 # seconds between "is online?" checks
    
        # I will sometimes refresh browser.
        # it's a defense against buffering or memory leak problems
        # (with twitch/chrome) that may or may not arise
        next_restart = time() + (random.randint(30, 120) * 60) # 30 to 120 min
    
        while self._broadcast_is_offline():
            sleep(poll_time)
            if time() >= next_restart:
                self._restart_browser()
                next_restart = time() + (random.randint(30, 120) * 60)
    
        # now broadcast is online so we will wait until player
        # goes to a screen that indicates he is going to some track
        self._wait_for_track_pre_stage_indication()

    def _broadcast_is_offline(self):
        # TODO: implement
        return False

    def _restart_browser(self):
        self._debug("restarting browser")
        self._close_broadcast()
        sleep(5)
        self._open_broadcast()

    def _wait_for_track_pre_stage_indication(self):
        """
        Look for signs that player is going to a track, we're looking for the
        screens that you go to just before you press "go to track"
        """
        exit_symbol_likelihood = 0
        go_to_track_likelihood = 0
        on_track_likelihood = 0

        believe_exit_symbol_is_there = 96
        believe_go_to_track_is_there = 95
        believe_is_on_track = 97

        exits = []
        times = []
        imgs = []

        duration = 90 # seconds
        duration = 60
        start = time()
        while time() - start < duration:
            # When you go to time trial, before you go to track
            # there is this red exit symbol, see examplars/exit.png
            exit_likelihood, exit_img = self._check_for_exit_symbol()

            exits.append(exit_likelihood)
            times.append(time())
            imgs.append(exit_img)
            sleep(0.2)
            #go_to_track_likelihood = self._check_for_go_to_track_symbol() !!!!!
    
            # NOTE: not yet ...
            #if (exit_likelihood >= believe_exit_is_there and
            #    go_to_track_likelihood >= believe_go_to_track_is_there
            #    ):
            #    self._note_down_track_info()
            #    self._has_seen_track_pre_stage_indication = True
    
            #if self._has_seen_track_pre_stage_indication:
            #    on_track_likelihood = self._check_for_on_track_indications()
    
            #if on_track_likelihood >= believe_on_track:
            #    self._start_logging_lap_times()

        with open("./exit_detection.data", 'w') as f:
            for i in range(len(exits)):
                f.write("{} {}\n".format(times[i], exits[i]))
                imgs[i].save("./data/exit_detection_imgs_02/exit"+
                             str(i).zfill(4)+".png")

        self.stop()

    def _check_for_exit_symbol(self):
        # exit symbol:
        #     x: 984, y: 821, w:47,  h:48
        if self._screen_resolution = (1920, 1080):
            exit = # TODO: continue here
        elif self._screen_resolution = (1600, 900):
            exit = {"top": 826, "left": 989, "width": 47, "height": 48}
        else:
            raise RuntimeError("Resolution not supported")

        screen_shot = self._screen.grab(exit)
        exit_img = self._screen_shot_2_image(screen_shot)
        exit_exemplar = Image.open("./exemplars/exit.png")

        comparison = ImageCompare(exit_img, exit_exemplar)
        return comparison.similarity(), exit_img

    def _screen_shot_2_image(self, screen_shot):
        """
        Converts mss.base.ScreenShot to PIL.Image
        """
        return Image.frombytes('RGB', screen_shot.size, screen_shot.bgra,
                               'raw', 'BGRX')

    def _start_loggin_lap_times(self):
        # TODO: implement
        pass

    def _note_down_track_info(self):
        """
        Called when it's likely we are on a page where player is just about to
        'go to track' here we want to figure out which track the player is going
        to and what car the player is driving
        """
        # TODO: implement this:
        # this function is going to be called many times so we want to keep
        # track of what we analyze to be the track name and car name
        # and the results will be the most common occurence from the analyses

        self._track = self._determine_track_name()
        self._car = self._determine_car_name()

    def _determine_track_name(self):
        # TODO: implement
        return "example_track_name"

    def _determine_car_name(self):
        # TODO: implement
        return "example_car_name"

def cd_to_project_root():
    this_scripts_file = abspath(__file__)
    this_scripts_directory = dirname(this_scripts_file)
    os.chdir(this_scripts_directory)

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

class ImageCompare():
    """
    Used for computing similarity between two images

    This class was based on this stuff:
        https://gist.github.com/attilaolah/1940208
    In the gist pixel values where converted to int using:
        yield pixel[0] | (pixel[1]<<8) | (pixel[2]<<16)
    I think the values did not give correct pixel differences since the
    difference between pixels
        (0,255,0) - (0,0,0)
    will be greater than
        (255,0,0) - (0,0,0)
    So I rewrote the class, only with support to calculate mean square error
    and with improved pixel difference system

    Usage example:
        img1 = pil.Image.open("./image1.png")
        img2 = pil.Image.open("./image2.png")
        comparsion = ImageCompare(img1, img2)
        print(comparison.similarity())
    """
    def __init__(self, img1, img2):
        """
        Args:
            img1 (PIL.Image): first image
            img2 (PIL.Image): second image to compare to first image
        """
        self._img1 = img1
        self._img2 = img2
        self._normalized_mean_square_distance = None

    @property
    def img1(self):
        return self._img1

    @img1.setter
    def img1(self, img):
        self._img1 = img
        self._normalized_mean_square_distance = None
    
    @property
    def img2():
        return self._img2

    @img2.setter
    def img2(self, img):
        self._img2 = img
        self._normalized_mean_square_distance = None

    @property
    def normalized_mean_square_distance(self):
        if self._normalized_mean_square_distance is not None:
            return self._normalized_mean_square_distance

        continue_iterating = True
        nmsds = [] # normalized mean square distances
        resize_size = 2 # first try comparing with images reduced to 2x2

        while continue_iterating:
            if (len(nmsds) >= 3 and
                abs(nmsds[-1] - nmsds[-2]) <= abs(nmsds[-2] - nmsds[-3])
                ):
                continue_iterating = False
            else:
                nmsd = self._calculate_normalized_mean_square_distance(
                        resize_size)
                nmsds.append(nmsd)
            resize_size *= 2

        return nmsds[-1]

    def similarity(self):
        return 100.0 - 100*self.normalized_mean_square_distance

    def _calculate_normalized_mean_square_distance(self, resize_size):
        (img1_width, img1_height) = self._img1.size
        (img2_width, img2_height) = self._img2.size

        new_width = min(img1_width, img2_width, resize_size)
        new_height = min(img1_height, img2_height, resize_size)

        # Rescale to resize_size
        img1_resized = self._img1.resize(
                (new_width, new_height), resample=Image.BICUBIC)
        img2_resized = self._img2.resize(
                (new_width, new_height), resample=Image.BICUBIC)

        mean_square_distance = self._calculate_mean_square_distance(
                img1_resized, img2_resized)
        normalized_mean_square_distance = math.sqrt(mean_square_distance) / 255
        return normalized_mean_square_distance

    def _calculate_mean_square_distance(self, img1, img2):
        (width, height) = img1.size
        mse = 0
        for i in range(width):
            for j in range(height):
                img1_pixel = img1.getpixel((i,j))
                img2_pixel = img2.getpixel((i,j))
                mse += (img1_pixel[0] - img2_pixel[0])**2 # R
                mse += (img1_pixel[1] - img2_pixel[1])**2 # G
                mse += (img1_pixel[2] - img2_pixel[2])**2 # B
        mse = float(mse) / (width*height*3)
        return mse

def get_snip(x, y, w, h):
    pass

if __name__ == "__main__": # pragma: no cover
    #main()
    test()
    #test2()

#        time = {"top": 11, "left": 97, "width": 36, "height": 15}
#        trial = {"top": 10, "left": 134, "width": 31, "height": 15}
#        #exit = {"top": 984, "left": 821, "width": 47, "height": 48}
#        exit = {"top": 826, "left": 989, "width": 47, "height": 48}
#        time_imgs = []
#        trial_imgs = []
#        exit_imgs = []
#        play_mario()
#        for i in range(1000):
#            #time_imgs.append(sct.grab(time))
#            #trial_imgs.append(sct.grab(trial))
#            exit_imgs.append(sct.grab(exit))
#            sleep(0.03)
#        play_mario()
#        #for i, image in enumerate(time_imgs):
#        #    mss.tools.to_png(image.rgb, image.size,
#        #                     output="time{}.png".format(str(i).zfill(3)))
#        #for i, image in enumerate(trial_imgs):
#        #    mss.tools.to_png(image.rgb, image.size,
#        #                     output="trial{}.png".format(str(i).zfill(3)))
#        for i, image in enumerate(exit_imgs):
#            mss.tools.to_png(image.rgb, image.size,
#                             output="exit{}.png".format(str(i).zfill(3)))
#
