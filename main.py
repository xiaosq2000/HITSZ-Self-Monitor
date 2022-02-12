# -*- coding: utf-8 -*-
import time
import argparse
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
parser = argparse.ArgumentParser(description='哈小深自动上报')
parser.add_argument('-i', '--id', help='学号', required=True)
parser.add_argument('-p', '--password', help='密码', required=True)
args = parser.parse_args()
studentID = args.id
studentPassword = args.password
options = Options()
options.headless = True
options.add_argument("--log-level=3")
driver = webdriver.Chrome(".\chromedriver.exe", options=options)
# 哈小深
driver.get('https://student.hitsz.edu.cn/xg_mobile/loginChange')
# 统一身份认证登录
driver.find_element_by_xpath(
    '/html/body/div[4]/div[1]/a').click()
# 输入学号
driver.find_element_by_xpath(
    '/html/body/div/div[2]/div/form/div/div[2]/ul/li[1]/input[1]').send_keys(studentID)
# 输入密码
driver.find_element_by_xpath(
    '/html/body/div/div[2]/div/form/div/div[2]/ul/li[1]/input[2]').send_keys(studentPassword)
# 登录
driver.find_element_by_xpath(
    '/html/body/div/div[2]/div/form/div/div[2]/ul/li[1]/span/input').click()
# 每日上报
driver.find_element_by_xpath(
    '/html/body/div[1]/div/div[2]/div/div[1]/div[1]').click()
# 今日是否已经上报
flag = driver.find_element_by_xpath(
    '/html/body/div[2]/div[2]/div[2]/div/div/div[1]/div[63]/div/div/span[1]').text
if flag == '已提交':
    print('您今日已上报，无需再次上报')
else:
    # 当前状态：其他
    driver.find_element_by_xpath(
        '/html/body/div[2]/div[2]/div[2]/div/div/div[1]/div[12]/div/input').click()
    action = ActionChains(driver)
    element1 = driver.find_element_by_xpath(
        '/html/body/div[3]/div[2]/div[2]/div/div[2]')
    time.sleep(1)
    action.drag_and_drop_by_offset(element1, 0, -102).perform()
    time.sleep(1)
    action.drag_and_drop_by_offset(element1, 0, -102).perform()
    time.sleep(1)
    driver.find_element_by_xpath(
        '/html/body/div[3]/div[2]/div[1]/a[2]').click()
    # 获取地理位置
    driver.find_element_by_xpath(
        '/html/body/div[2]/div[2]/div[2]/div/div/div[1]/div[17]/div[2]/div/div/span/a').click()
    time.sleep(1)
    # 拖动页面
    driver.execute_script("window.scrollTo(0, 1000)")
    time.sleep(1)
    # 已接种全部剂次
    driver.find_element_by_xpath(
        '/html/body/div[2]/div[2]/div[2]/div/div/div[1]/div[53]/div/label[3]').click()
    time.sleep(1)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    # 承诺
    driver.find_element_by_xpath(
        '/html/body/div[2]/div[2]/div[2]/div/div/div[1]/div[62]/label').click()
    time.sleep(1)
    # 提交信息
    driver.find_element_by_xpath(
        '/html/body/div[2]/div[2]/div[2]/div/div/div[1]/div[63]/div/div/span[1]').click()
    print('上报成功')
    time.sleep(2)
driver.close()