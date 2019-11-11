import requests
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup
import os

usr = ''
passwd = ''
wait_time = 10
download_path = ""

def login():
    login_url = 'https://account.sharky-china.com/login?locale=en'
    
    profile = webdriver.FirefoxProfile()
    profile.set_preference('browser.download.folderList', 2)
    profile.set_preference('browser.download.dir', download_path)
    profile.set_preference('browser.download.manager.showWhenStarting', False)    
    profile.set_preference('browser.helperApps.neverAsk.saveToDisk','application/x-openvpn-profile')
    options = Options()
    options.add_argument('--headless')

    browser = webdriver.Firefox(executable_path='./geckodriver', firefox_profile=profile, options=options)
    
    browser.get(login_url)
    time.sleep(wait_time)

    try:
        user_name_box = browser.find_element_by_id('username')
        user_name_box.clear()
        user_name_box.send_keys(usr)
    except Exception as _:
        print("Fail to fill in username.")
        exit()
    
    try:
        passwd_box = browser.find_element_by_id('password')
        passwd_box.clear()
        passwd_box.send_keys(passwd)
    except Exception as _:
        print("Fail to fill in password")
        exit()
    
    try:
        login_botton = browser.find_element_by_xpath("//button[@type='submit']")
        login_botton.click()
        print("Login")
    except Exception as _:
        print("Login Fail")
        exit()
    time.sleep(wait_time)
    return browser

def enter_manual(browser):
    try:
        time.sleep(wait_time)
        browser.get('https://account.sharky-china.com/setup/manual')
        time.sleep(wait_time)
    except Exception as _:
        print("Error when entering manual page")
        exit()

def change_to_en(browser):
    browser.find_element_by_xpath("//a[@class='locale locale-en ewivdvu2 css-12fyz5o-Link-LanguageLink eeapdel0']").click()

def get_config_list(browser):
    try:
        raw_config_list = browser.find_elements_by_xpath("//div[@class='css-1d120kr-Third e1mbx5kv3']")
    except Exception as _:
        print("Error when getting config_list")
        exit()
    
    config_list = []

    for server in raw_config_list:
        temp_config = {}
        
        try:
            html = server.get_attribute("innerHTML")
            soup = BeautifulSoup(html, 'lxml')
            country = soup.select("p[class='css-1nr7cc-Title e595umj10']")[0].text
            country_url = soup.select("p[class='css-10o7jgy-SubTitle e595umj11']")[0].text
            country_tcp = server.find_element_by_xpath(".//div[@class=\"css-1tub5pl-LinkContainer e595umj12\"]/a[1]")
            country_udp = server.find_element_by_xpath(".//div[@class=\"css-1tub5pl-LinkContainer e595umj12\"]/a[2]")
            # print(country)
            # print(country_url)
            # print(country_tcp)
            # print(country_udp)
            # print("\n")
            temp_config['country'] = country
            temp_config['url'] = country_url
            temp_config['tcp'] = country_tcp
            temp_config['udp'] = country_udp
            config_list.append(temp_config)
        except Exception as _:
            pass

    return config_list

def test_ping(url):
    re = os.system("ping -n 4 %s" % url)
    if re == 0:
        return True
    return False

def try_servers(config_list, browser):
    for server in config_list:
        if test_ping(server['url']):
            browser.execute_script("arguments[0].click();", server['udp'])
            browser.execute_script("arguments[0].click();", server['tcp'])
            print("%s available" % server['country'])

def check_ini():
    if usr == '':
        print("Error: Not set username")
        exit()
    if passwd == '':
        print("Error: Not set password")
        exit()
    if download_path == "":
        print("Error: Not set download path")
        exit()

if __name__ == '__main__':
    check_ini()
    browser = login()
    enter_manual(browser)
    config_list = get_config_list(browser)
    try_servers(config_list, browser)
    print("All the available .ovpn files saved in %s" % download_path)
