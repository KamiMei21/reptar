#!/usr/bin/env python3
#Example application for Reptar
import sys

from reptar.webdriver import Reptar


def main(argv):
    browser = Reptar()
    browser.get("https://duckduckgo.com/html")
    search_form = browser.find_element_by_id("search_form_input_homepage")
    search_form.send_keys("real python")
    search_form.submit()
    print(browser.page_source)
    browser.close()
    
if __name__ == "__main__":
    main(sys.argv)
