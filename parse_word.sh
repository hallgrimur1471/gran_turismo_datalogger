#!/usr/bin/env bash
tesseract "$1" -psm 8 stdout 2>/dev/null
