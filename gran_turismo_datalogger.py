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
    args = parse_args()
    cd_to_project_root()
    data_logger = DataLogger()
    data_logger.start()

def test():
    try:
        args = parse_args()
        cd_to_project_root()
        data_logger = DataLogger()
        data_logger
        driver = open_broadcast(args.BROADCAST)
        sleep(8)
        wait_for_track_indication()
    except:
        raise
    finally:
        close_broadcast(driver)


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

        self._has_seen_track_pre_stage_indication = False

    @property
    def broadcast():
        return self._broadcast

    def start(self):
        self._change_working_directory_to_datalogger()
        self._open_broadcast()
        with mss.mss() as screen:
            self._screen = screen
            self._wait_for_online()

    def _change_working_directory_to_datalogger():
        this_scripts_file = abspath(__file__)
        this_scripts_directory = dirname(this_scripts_file)
        os.chdir(this_scripts_directory)

    def _open_broadcast():
        self._browser.get(self.broadcast)
        elem = self._browser.find_element_by_class_name(
                "pl-button__fullscreen--tooltip-left")
        elem.click()

    def _close_broadcast():
        self._browser.close()

    def _wait_for_online():
        """
        wait until broadcast comes online
        """
        poll_time = 10 # seconds between "is online?" checks
    
        # I will sometimes refresh browser.
        # it's a defense against buffering or memory leak problems
        # (with twitch/chrome) that may or may not arise
        next_restart = time() + (random.randint(30, 120) * 60) # 30 to 120 min
    
        while broadcast_is_offine():
            sleep(poll_time)
            if time() >= next_restart:
                self._restart_browser()
                next_restart = time() + (random.randint(30, 120) * 60)
    
        # now broadcast is online so we will wait until player
        # goes to a screen that indicates he is going to some track
        self._wait_for_track_pre_stage_indication()

    def _restart_browser():
        self._debug("restarting browser")
        self._close_broadcast()
        sleep(5)
        self._open_broadcast()

    def _wait_for_track_pre_stage_indication():
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

        # When you go to time trial, before you go to track
        # there is this red exit symbol, see examplars/exit.png
        exit_likelihood = self._check_for_exit_symbol()
        go_to_track_likelihood = self._check_for_go_to_track_symbol()

        if (exit_likelihood >= believe_exit_is_there and
            go_to_track_likelihood >= believe_go_to_track_is_there
            ):
            self._note_down_track_info()
            self._has_seen_track_pre_stage_indication = True

        if self._has_seen_track_pre_stage_indication:
            on_track_likelihood = self._check_for_on_track_indications()

        if on_track_likelihood >= believe_on_track:
            self._start_logging_lap_times()

    def _start_loggin_lap_times():
        # TODO: implement
        pass

    def _note_down_track_info():
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

    def _determine_track_name():
        # TODO: implement
        return "example_track_name"

    def _determine_car_name():
        # TODO: implement
        return "example_car_name"

def cd_to_project_root():
    this_scripts_file = abspath(__file__)
    this_scripts_directory = dirname(this_scripts_file)
    os.chdir(this_scripts_directory)

def change_working_directory_to_gran_turismo_datalogger():
    this_scripts_file = abspath(__file__)
    this_scripts_directory = dirname(this_scripts_file)
    os.chdir(this_scripts_directory)

def broadcast_is_offline():
    # TODO: implement
    return False

def look_for_exit_symbol():
    # exit symbol:
    #     x: 984, y: 821, w:47,  h:48
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

class ImageCompare():
    """
    Used for computing similarity between two images

    This class was based on this stuff:
        https://gist.github.com/attilaolah/1940208

    Usage example:
        cmp = ImageCompare(img1, img2)
        print(cmp.similarity())
    """
    def __init__(self, img1, img2):
        """
        Args:
            img1 (???): first image
            img2 (???): second image to compare to first image
        """
        # TODO: make these images python objects, which image library should
        #       we use?
        self._img1 = img1
        self._img2 = img2
        self._normalized_mean_square_distance = None

    @property
    def img1(self):
        return self._img1

    @img1.setter
    def img1(self, img):
        self._img1 = img
        self._mean_square_distance = None
        self._normalized_mean_square_distance = None
    
    @property
    def img2():
        return self._img2

    @img2.setter
    def img2(self, img):
        self._img2 = img
        self._mean_square_distance = None
        self._normalized_mean_square_distance = None

    def similarity(self):
        return 100.0 - self.normalized_mean_square_distance()

    @property
    def normalized_mean_square_distance(self):
        if self._normalized_mean_square_distance is not None:
            return self._normalized_mean_square_distance

        continue_iterating = True
        nmsds = [] # normalized mean square distances
        resize_size = 2 # first try comparing with images reduced to 2x2

        nmsd = self._calculate_normalized_mean_square_distance(resize_size)
        nmsds.append(nmsd)
        while continue_iterating:
            if (len(nmsds) >= 3 and
                abs(nmsds[-1] - nmsds[-2]) <= abs(nmsds[-2] - nmsds[-3])
                ):
                continue_iterating = False
            else:
                nmsds.append(
                    self._calculate_normalized_mean_square_distance(
                        resize_size))
            resize_size *= 2

    def _calculate_normalized_mean_square_distance(self, resize_size):
        size1 = self._img1.size
        size2 = self._img2.size

        newx = min(size1[0], size2[0], resize_size)
        newy = min(size1[1], size2[1], resize_size)

        # Rescale to a common size:
        self._img1_resized = self._img1.resize((newx, newy), Image.BICUBIC)
        self._img2_resized = self._img2.resize((newx, newy), Image.BICUBIC)

        #if not self._colour:
        #    # Store the images in B/W Int format
        #    imga = imga.convert('I')
        #    imgb = imgb.convert('I')

        # Store the common image size
        #self.x, self.y = newx, newy

        mean_square_distance = self._calculate_mean_square_distance()
        normalized_mean_square_distance = math.sqrt(mean_square_distance) / 255

    def calculate_mean_square_distance():
        (size_x, size_y) = self._img1_resized.size
        # MARK: I stopped here
        tmp = sum([(a-b)**2 for a, b in zip(self.imga_int, self.imgb_int)])
        self._mse = float(tmp) / size_x / size_y

        return self._mse



def get_snip(x, y, w, h):
    pass

if __name__ == "__main__": # pragma: no cover
    #main()
    test()

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
