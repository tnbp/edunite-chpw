#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from datetime import datetime
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
opts = Options()
opts.headless = True
assert opts.headless
browser = Firefox(options=opts)

edunite_user = "please.change@this.login"
edunite_pass = "PleaseChangeMeToo"

browser.get("https://secure.edunite.info/Login.aspx")
browser.find_element_by_id('TextBoxEmail').send_keys(edunite_user)
browser.find_element_by_id('TextBoxPassword').send_keys(edunite_pass)
browser.find_element_by_id('ButtonLogin').click()

browser.get("https://secure.edunite.info/Administration/School/Student.aspx")

query_string = input("Please enter query string: ")

browser.find_element_by_xpath('//*[@id="ctl00_ContentPlaceHolder_TextBoxSearchString"]').send_keys(query_string)
browser.find_element_by_xpath('//*[@id="ctl00_ContentPlaceHolder_ButtonSearch"]').click()

users_tr = browser.find_elements_by_class_name('dataGridItem')

if len(users_tr) > 0:
    print("Found " + str(len(users_tr)) + " users with query string '" + query_string + "':")
else:
    print("Couldn't find any users with query string '" + query_string + "'.")

for i, tr in enumerate(users_tr):
    print(str(i) + "\t", end='')
    users_td = tr.find_elements_by_tag_name('td')
    user_type = users_td[0].find_element_by_tag_name('a').get_attribute('class')
    if "type-s" in user_type:
        print("User Type: Student\t\t| ", end='')
    elif "type-p" in user_type:
        print("User Type: Parent\t\t| ", end='')
    else:
        print("WEIRD USER TYPE: " + user_type + "\t\t| ", end='')
    user_name = users_td[1].find_element_by_tag_name('a').get_attribute('title')
    print("User Name: " + user_name)
    
select_user = int(input("Please enter a number between 0 and " + str(len(users_tr)-1) + ":\t"))
users_tr[select_user].find_elements_by_tag_name('td')[1].click()

now = datetime.now()
new_password = "SuperSecretDefaultPassword"

if "Schüler/in" in browser.find_element_by_xpath('//*[@id="pageContent"]/h1').get_attribute('innerHTML'):
    print("!!STUDENT ACCOUNT!!")
    browser.find_element_by_xpath('//*[@id="tabStudent"]/ul/li[2]/a').click()
    print("LOGIN:\t\t" + browser.find_element_by_id('ctl00_ContentPlaceHolder_TextBoxLogin').get_attribute('value'))
    print("PASSWORD:\t" + new_password)
    browser.find_element_by_id('ctl00_ContentPlaceHolder_TextBoxPassword').send_keys(new_password)
    browser.find_element_by_id('ctl00_ContentPlaceHolder_TextBoxPasswordReenter').send_keys(new_password)
    browser.find_element_by_id('ctl00_ContentPlaceHolder_CheckBoxChangePassword').click()
    browser.find_element_by_id('ctl00_ContentPlaceHolder_ButtonSave').click()
    print("CHANGED PASSWORD???")
else:
    print("!!PARENT ACCOUNT!!")
    browser.find_element_by_xpath('//*[@id="tabParent"]/ul/li[3]/a').click()
    print("LOGIN:\t\t" + browser.find_element_by_id('ctl00_ContentPlaceHolder_TextBoxLogin').get_attribute('value'))
    print("PASSWORD:\t" + new_password)
    browser.find_element_by_id('ctl00_ContentPlaceHolder_TextBoxPassword').send_keys(new_password)
    browser.find_element_by_id('ctl00_ContentPlaceHolder_TextBoxPasswordReenter').send_keys(new_password)
    browser.find_element_by_id('ctl00_ContentPlaceHolder_CheckBoxChangePassword').click()
    browser.find_element_by_id('ctl00_ContentPlaceHolder_ButtonSave').click()
    print("CHANGED PASSWORD???")
    
browser.quit()
