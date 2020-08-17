from . import model
from . import const
import re
import functools
import json
import traceback
import time
import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait

USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36"
options = Options()
options.add_argument(f'--user-agent="{USER_AGENT}"')
driver = webdriver.Chrome(options=options)
wait = WebDriverWait(driver, 5, 0.5)
driver.get(const.JXGL_URL)
session = None
config = json.load(open('../../config.json'))
schedule = []

def fill_credentials():
    time.sleep(3)
    driver.switch_to.frame('frmLogin')
    print('Filing credentials...')
    input_username = wait.until(EC.presence_of_element_located((By.ID,'txt_dsdsdsdjkjkjc')))
    input_username.clear()
    input_username.send_keys(config['jwc_username'])
    input_password = wait.until(EC.presence_of_element_located((By.ID,'txt_dsdfdfgfouyy')))
    input_password.clear()
    input_password.send_keys(config['jwc_password'])

def login_and_get_session():
    print(f'Trying to login and get session...')
    submit_button = wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="Logon"]/table/tbody/tr/td[10]/input[1]')))
    submit_button.click()
    try:
        wait.until(EC.url_matches('http://jxgl.cqu.edu.cn/MAINFRM.aspx'))
        print('Login successed')
        return True
    except:
        print('Login failed')
        traceback.print_exc()
        return False

def crawl_cqu_info():
    print('Start crawling...')
    time.sleep(5)
    driver.switch_to.frame('frmbody')
    driver.execute_script('openTheBar(3)')
    # driver.get(f'{const.JXGL_URL}/znpk/Pri_StuSel.aspx')
    schedule_submit = driver.find_element_by_xpath('//*[@id="memuLinkDiv3"]/div/table/tbody/tr[1]/td[2]/span')
    schedule_submit.click()
    time.sleep(5)
    driver.switch_to.frame('frmMain')
    time.sleep(5)
    driver.execute_script('ChkValue()')
    time.sleep(5)
    driver.switch_to.frame('frmRpt')
    time.sleep(5)
    table = driver.find_elements_by_xpath('/html/body/div[1]/div[1]/table[1]/tbody/tr')
    def process_items(items):
        for item in items:
            info = {}
            info['id'] = item.find_element_by_xpath('td[1]').text
            info['course'] = item.find_element_by_xpath('td[2]').text
            info['credit'] = item.find_element_by_xpath('td[3]').text
            info['credit_hour_total'] = item.find_element_by_xpath('td[4]').text
            info['lesson_hour'] = item.find_element_by_xpath('td[5]').text
            info['lab_hour'] = item.find_element_by_xpath('td[6]').text
            info['category'] = item.find_element_by_xpath('td[7]').text
            info['teacher'] = item.find_element_by_xpath('td[10]').text
            info['week'] = item.find_element_by_xpath('td[11]').text
            info['time'] = item.find_element_by_xpath('td[12]').text
            info['address'] = item.find_element_by_xpath('td[13]').text
            schedule.append(info)
            
    process_items(table)
    schema = model.CourseSchema(many=True)
    print(schedule)
    return schema.dump(schedule)
    


class Session:
    def __init__(self):
        fill_credentials()
        login_and_get_session()
        self._sess = requests.session()
        self._sess.cookies = driver.get_cookies()
    
    def schedule(self):
        crawl_cqu_info()
        driver.quit()
    
    
