#!/usr/bin/env bash

python3.5 -m pytest tests \
  --cov=. \
  --cov-report html \
  --cov-report term \
  --no-cov-on-fail
