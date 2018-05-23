#!/usr/bin/env python3

from brow.interface.selenium import ChromeBrowser as Browser

with Browser.session() as b:
    b.load("https://marcyes.com")
    print(b.body)

    # follow a link
    css_selector="a#some_id"
    elem = b.element(css_selector)
    elem.click()
    print(b.url)
