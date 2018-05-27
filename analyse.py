#!/usr/bin/env python3.5

import os
import re
from os import listdir
from os.path import isfile, join
import subprocess
from subprocess import PIPE

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from gran_turismo_datalogger import change_working_directory_to_datalogger


def main():
    change_working_directory_to_datalogger()
    #times_trial_analyze()
    exit_analyze()

def exit_analyze():
    exits = []
    for file_ in listdir(join(os.getcwd(), "img")):
        exit_pattern = re.compile("exit[0-9]+\.png")
        if re.match(exit_pattern, file_):
            exits.append(file_)

    exits.sort()

    exit_sample = "sample_exit.png"
    diffs = []
    for exit in exits:
        diff = img_diff(exit, exit_sample)
        diffs.append(diff)
        print(exit, diff)

    fig, ax = plt.subplots()
    ax.plot(diffs)
    plt.show()



def img_diff(img1, img2):
    diff = subprocess.run(
        "./img_diff_test.py ./img/{} ./img/{}".format(img1, img2),
        stdout=PIPE, shell=True).stdout.decode().rstrip()
    print(diff)
    return float(diff)

def times_trial_analyze():
    times = []
    trials = []
    for file_ in listdir(os.getcwd()):
        time_pattern = re.compile("time[0-9]+\.png")
        trial_pattern = re.compile("trial[0-9]+\.png")
        if re.match(time_pattern, file_):
            times.append(file_)
        elif re.match(trial_pattern, file_):
            trials.append(file_)
    
    times.sort()
    trials.sort()
    
    for i in range(min(len(times), len(trials))):
        times_result = subprocess.run(
            "tesseract {} -psm 8 stdout 2>/dev/null".format(times[i]),
            stdout=PIPE, shell=True).stdout.decode().rstrip()
        trials_result = subprocess.run(
            "tesseract {} -psm 8 stdout 2>/dev/null".format(trials[i]),
            stdout=PIPE, shell=True).stdout.decode().rstrip()
        #result = subprocess.run('echo hi', stdout=PIPE, shell=True)
        print(times[i], trials[i])
        print(times_result, trials_result)

if __name__ == "__main__":
    main()
