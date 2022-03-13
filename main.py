# -*- coding: utf-8 -*-
import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains

with open("config.json", "r", encoding='utf-8') as config:
    config = json.load(config)

options = Options()
options.headless = config["settings"]["headless"]
options.add_argument("--log-level=3")
options.add_argument("--start-maximized")
driver = webdriver.Chrome(ChromeDriverManager(
    path='./', print_first_line=False).install(), options=options)

print("打开哈小深疫情上报网页")
driver.get('https://student.hitsz.edu.cn/xg_mobile/loginChange')
print("开始统一身份认证登录")
driver.find_element(by=By.XPATH, value='/html/body/div[4]/div[1]/a').click()
print("输入学号")
driver.find_element(
    by=By.XPATH, value='/html/body/div/div[2]/div/form/div/div[2]/ul/li[1]/input[1]').send_keys(config["profiles"]["id"])
print("输入密码")
driver.find_element(
    by=By.XPATH, value='/html/body/div/div[2]/div/form/div/div[2]/ul/li[1]/input[2]').send_keys(config["profiles"]["password"])
driver.find_element(
    by=By.XPATH, value='/html/body/div/div[2]/div/form/div/div[2]/ul/li[1]/span/input').click()
print("成功登录，开始每日上报")
driver.find_element(
    by=By.XPATH, value='/html/body/div[1]/div/div[2]/div/div[1]/div[1]').click()
print("今日是否已经上报")
flag = driver.find_element(
    by=By.XPATH, value='/html/body/div[2]/div[2]/div[2]/div/div/div[1]/div[63]/div/div/span[1]').text
if flag == '已提交':
    print('您今日已上报，无需再次上报')
else:
    print("当前状态...")
    driver.find_element(
        by=By.XPATH, value='/html/body/div[2]/div[2]/div[2]/div/div/div[1]/div[12]/div/input').click()
    picker_indicator = driver.find_element(
        by=By.XPATH, value='/html/body/div[3]/div[2]/div[2]/div/div[2]')
    action = ActionChains(driver)
    index = 7
    while index > 1:
        action.move_to_element(picker_indicator)
        action.drag_and_drop_by_offset(picker_indicator, 0, +34)
        index -= 1

    while index < config["profiles"]["current_status"]:
        action.move_to_element(picker_indicator)
        action.drag_and_drop_by_offset(picker_indicator, 0, -34)
        index += 1

    time.sleep(1)
    action.perform()
    driver.find_element(
        by=By.XPATH, value='/html/body/div[3]/div[2]/div[1]/a[2]').click()
    print("获取地理位置...")
    driver.find_element(
        by=By.XPATH, value='/html/body/div[2]/div[2]/div[2]/div/div/div[1]/div[17]/div[2]/div/div/span/a').click()
    driver.execute_script("window.scrollTo(0, 1000)")  # 拖动页面
    print("已接种全部剂次...")
    driver.find_element(
        by=By.XPATH, value='/html/body/div[2]/div[2]/div[2]/div/div/div[1]/div[53]/div/label[3]').click()
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    print("承诺...")
    driver.find_element(
        by=By.XPATH, value='/html/body/div[2]/div[2]/div[2]/div/div/div[1]/div[62]/label').click()
    print("提交信息...")
    driver.find_element(
        by=By.XPATH, value='/html/body/div[2]/div[2]/div[2]/div/div/div[1]/div[63]/div/div/span[1]').click()
    print('上报成功')
driver.close()