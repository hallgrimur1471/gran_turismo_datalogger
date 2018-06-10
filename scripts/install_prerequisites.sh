#!/usr/bin/env bash

# for Ubuntu 16.04

# assuming installation of python3.5

# image OCR
sudo apt-get install -y tesseract-ocr 

# more image analyzis
sudo python3.5 -m pip uninstall PIL
sudo python3.5 -m pip install -U Pillow

# sound
sudo apt-get install -y sox

# testing
sudo python3.5 -m pip install pytest
sudo python3.5 -m pip install pytest-cov
