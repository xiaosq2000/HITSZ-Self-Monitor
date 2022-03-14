# -*- coding: utf-8 -*-
from sys import exit
import os
import time
import json
import logging
from datetime import date
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains

with open("config.json", "r", encoding='utf-8') as config:
    config = json.load(config)

os.makedirs('log', exist_ok=True)
logging.basicConfig(filename='log/'+str(date.today())+'.log', level=logging.INFO,
                    format='%(asctime)s %(levelname)s:%(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', encoding='utf-8')
logger = logging.getLogger(__name__)

if config["settings"]["log_level"] == 'DEBUG':
    logging.getLogger().setLevel(logging.DEBUG)

try:
    options = Options()
    options.headless = config["settings"]["headless"]
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(ChromeDriverManager(
        path='./', print_first_line=False).install(), options=options)
except Exception as err:
    logger.error(err)
    logger.error('无法使用 webdriver-manager，请确保您没有使用 Proxy 或 VPN 。')
    exit()

try:
    logger.info("====== 哈小深自动上报 ======")
    logger.debug("打开哈小深疫情上报网页")
    driver.get('https://student.hitsz.edu.cn/xg_mobile/loginChange')
    logger.debug("进行统一身份认证登录")
    driver.find_element(
        by=By.XPATH, value='/html/body/div[4]/div[1]/a').click()
    logger.debug("输入学号")
    driver.find_element(
        by=By.XPATH, value='/html/body/div/div[2]/div/form/div/div[2]/ul/li[1]/input[1]').send_keys(config["profiles"]["id"])
    logger.debug("输入密码")
    driver.find_element(
        by=By.XPATH, value='/html/body/div/div[2]/div/form/div/div[2]/ul/li[1]/input[2]').send_keys(config["profiles"]["password"])
    driver.find_element(
        by=By.XPATH, value='/html/body/div/div[2]/div/form/div/div[2]/ul/li[1]/span/input').click()
except Exception as err:
    logger.error(err)
    logger.error(
        '上报失败，请确认您的 json 文件内容正确。若仍有问题，可发送日志文件至 xiaosq2000@gmail.com 。')
    driver.close()
    exit()

try:
    logger.debug("点击哈小深每日上报")
    driver.find_element(
        by=By.XPATH, value='/html/body/div[1]/div/div[2]/div/div[1]/div[1]').click()
    flag = driver.find_element(
        by=By.XPATH, value='/html/body/div[2]/div[2]/div[2]/div/div/div[1]/div[63]/div/div/span[1]').text
    if flag == '已提交':
        logger.info('您今日已上报，无需重复上报')
        driver.close()
        exit()
    else:
        logger.debug("选择当前状态")
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
        logger.debug("获取地理位置")
        driver.find_element(
            by=By.XPATH, value='/html/body/div[2]/div[2]/div[2]/div/div/div[1]/div[17]/div[2]/div/div/span/a').click()
        driver.execute_script("window.scrollTo(0, 1000)")  # 拖动页面
        logger.debug("选择已接种全部剂次")
        driver.find_element(
            by=By.XPATH, value='/html/body/div[2]/div[2]/div[2]/div/div/div[1]/div[53]/div/label[3]').click()
        driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);")
        logger.debug("勾选承诺")
        driver.find_element(
            by=By.XPATH, value='/html/body/div[2]/div[2]/div[2]/div/div/div[1]/div[62]/label').click()
        logger.debug("提交信息")
        driver.find_element(
            by=By.XPATH, value='/html/body/div[2]/div[2]/div[2]/div/div/div[1]/div[63]/div/div/span[1]').click()
        logger.info('上报成功')
        driver.close()
        exit()
except Exception as err:
    logger.error(err)
    logger.error(
        '上报失败。哈小深每日疫情上报系统可能发生了更新。')
    driver.close()
    exit()