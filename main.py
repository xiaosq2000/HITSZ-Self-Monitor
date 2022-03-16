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
    options.add_argument("--log-level=3")
    driver = webdriver.Chrome(ChromeDriverManager(
        path='./', print_first_line=False).install(), options=options)
except Exception as err:
    logger.error(err)
    logger.error('无法使用 webdriver-manager，请确保您没有使用 Proxy 或 VPN 。')
    exit()

if config["profiles"]["geo-location-emulation"]["enable"] == True:
    try:
        Map_coordinates = dict({
            "latitude": config["profiles"]["geo-location-emulation"]["latitude"],
            "longitude": config["profiles"]["geo-location-emulation"]["longitude"],
            "accuracy": 100
        })
        driver.execute_cdp_cmd(
            "Emulation.setGeolocationOverride", Map_coordinates)
    except Exception as err:
        logger.error(err)
        logger.error('经纬度模拟失败。')

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
    logger.debug("点击登录")
    driver.find_element(
        by=By.XPATH, value='/html/body/div/div[2]/div/form/div/div[2]/ul/li[1]/span/input').click()
    logger.debug("点击哈小深每日上报")
    driver.find_element(
        by=By.XPATH, value='/html/body/div[1]/div/div[2]/div/div[1]/div[1]').click()
except Exception as err:
    logger.error(err)
    logger.error(
        '登录失败，请检查您的 json 文件的内容与格式。')
    driver.close()
    exit()

try:
    driver.execute_script("window.scrollTo(0, 2500)")  # 拖动页面
    time.sleep(1)
    flag = driver.find_element(
        by=By.XPATH, value='/html/body/div[2]/div[2]/div[2]/div/div/div[1]/div[63]/div/div/span[1]').text

    if flag == '已提交':
        logger.info('您今日已上报，无需重复上报！')
        driver.close()
        exit()
    else:
        driver.execute_script("window.scrollTo(0, 0)")
        time.sleep(1)
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
        driver.execute_script("window.scrollTo(0, 500)")
        time.sleep(1)
        driver.find_element(
            by=By.XPATH, value='/html/body/div[2]/div[2]/div[2]/div/div/div[1]/div[17]/div[2]/div/div/span/a').click()
        time.sleep(1)

        logger.debug("选择地区风险等级")
        if config["profiles"]["current_location_risk_level"] == 'low':
            low_risk_button = driver.find_element(
                by=By.XPATH, value='/html/body/div[2]/div[2]/div[2]/div/div/div[1]/div[22]/div/label[1]')
            action = ActionChains(driver)
            action.click(low_risk_button)
            action.perform()
        else:
            if config["profiles"]["current_location_risk_level"] == 'medium':
                medium_risk_button = driver.find_element(
                    by=By.XPATH, value='/html/body/div[2]/div[2]/div[2]/div/div/div[1]/div[22]/div/label[2]')
                action = ActionChains(driver)
                action.click(medium_risk_button)
                action.perform()
            if config["profiles"]["current_location_risk_level"] == 'high':
                high_risk_button = driver.find_element(
                    by=By.XPATH, value='/html/body/div[3]/div[2]/div[2]/div/div/div[1]/div[22]/div/label[3]')
                action = ActionChains(driver)
                action.click(high_risk_button)
                action.perform()
            driver.execute_script("window.scrollTo(0, 1000)")
            time.sleep(1)
            current_location_blank = driver.find_element(
                by=By.XPATH, value='/html/body/div[2]/div[2]/div[2]/div/div/div[1]/div[24]/div[2]')
            action = ActionChains(driver)
            action.click(current_location_blank)
            action.send_keys(config["profiles"]["current_location_name"])
            action.perform()

        logger.debug("勾选承诺")
        driver.execute_script("window.scrollTo(0, 2500)")
        time.sleep(1)
        driver.find_element(
            by=By.XPATH, value='/html/body/div[2]/div[2]/div[2]/div/div/div[1]/div[62]/label').click()

        try:
            logger.debug("点击提交")
            driver.find_element(
                by=By.XPATH, value='/html/body/div[2]/div[2]/div[2]/div/div/div[1]/div[63]/div/div/span[1]').click()
        except Exception as err:
            logger.error(err)
            logger.error('提交按钮无法点击，建议人工检查是否已经上报。')
            driver.close()
            exit()

        time.sleep(1)
        flag = driver.find_element(
            by=By.XPATH, value='/html/body/div[2]/div[2]/div[2]/div/div/div[1]/div[63]/div/div/span[1]').text
        if flag == '已提交':
            logger.info('上报成功！')
            driver.close()
            exit()

        else:
            logger.error('上报失败，原因不明。')
            driver.close()
            exit()

except Exception as err:
    logger.error(err)
    logger.error(
        '可能是定位失败导致的无法上报，建议尝试模拟定位功能，或哈小深疫情上报系统发生了更新。')
    driver.close()
    exit()
