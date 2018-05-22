#!/usr/bin/env bash

cd $(dirname "$0")
ls laptime_*.png | xargs -I {} tesseract {} stdout
