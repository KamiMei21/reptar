#!/usr/bin/env python3
#Selenium example application for Chrome
import sys

from time import sleep

from reptar.webdriver import Reptar

def main(argv):
    browser = Reptar()
    browser.get("https://duckduckgo.com")
    print(browser.page_source)
    browser.quit()
    
if __name__ == "__main__":
    main(sys.argv)
