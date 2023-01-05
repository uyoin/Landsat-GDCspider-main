import os
import csv
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

# 创建字段来映射卫星和网址
dict1 = {}
dict1['LT4'] = '/html/body/div[1]/div[3]/div[1]/div[1]/div[2]/div[2]/div[2]/div/div[2]/div[4]'  # TM传感器
dict1['LT5'] = '/html/body/div[1]/div[3]/div[1]/div[1]/div[2]/div[2]/div[2]/div/div[2]/div[4]'  # TM传感器
dict1['LC8'] = '/html/body/div[1]/div[3]/div[1]/div[1]/div[2]/div[2]/div[2]/div/div[2]/div[1]'  # OLI传感器
dict1['LE7_off'] = '/html/body/div[1]/div[3]/div[1]/div[1]/div[2]/div[2]/div[2]/div/div[2]/div[2]'  # ETM传感器
dict1['LE7_on'] = '/html/body/div[1]/div[3]/div[1]/div[1]/div[2]/div[2]/div[2]/div/div[2]/div[3]'  # ETM传感器


def extract_id(csv_file):
    first_column = []
    # 打开CSV文件
    with open(csv_file, 'r') as f:
        # 创建一个CSV读取对象
        reader = csv.reader(f)

        # 遍历CSV文件的row
        for row in reader:
            # 对row第一个元素值（影像识别码）append到list中
            first_column.append(row[0])

    # 返回first_column（影像识别码）
    return first_column


def downLoad(driver, data_list):
    driver.get('http://www.gscloud.cn/accounts/login_user')
    email = driver.find_element(By.XPATH, '//input[@id="email"]')
    print("请输入您的地理空间数据云账号：")
    Account = input()
    print("请输入您的地理空间数据云密码：")
    passw = input()
    email.send_keys(Account)  # 账号
    password = driver.find_element(By.XPATH, '//input[@id="password"]')
    password.send_keys(passw)  # 密码
    captcha = driver.find_element(By.XPATH, '//input[@id="id_captcha_1"]')
    captcha_sj = input('请输入验证码：').strip()
    captcha.send_keys(captcha_sj)
    driver.find_element(By.XPATH, '//input[@id="btn-login"]').click()  # 输入验证码后点击登入按钮
    time.sleep(2)
    # 进入‘公开数据’页面
    driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/div[2]/ul/li/a').click()
    time.sleep(2)
    driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/div[2]/ul/li/div/ul/li[1]/a').click()
    time.sleep(2)

    for i in data_list:
        if i[:3] == 'LE7':
            driver.find_element(By.XPATH, dict1[i[:3] + '_on']).click()
            time.sleep(3)
            B = driver.find_element(By.XPATH,
                                    '/html/body/div[1]/div[3]/div[1]/div[1]/div[2]/div[2]/div[2]/div[2]/div[1]/table/tr[1]/td[2]/div/input')
            B.send_keys(i)
            B.send_keys(Keys.ENTER)
            time.sleep(3)
            q = driver.find_element(By.XPATH,
                                    '/html/body/div[1]/div[3]/div[1]/div[1]/div[2]/div[2]/div[2]/div[2]/div[1]/table/tr[3]/td').text
            if str(q) == "没有记录！":
                D = driver.find_element(By.XPATH,
                                        '/html/body/div[1]/div[3]/div[1]/div[1]/div[2]/div[1]/div[1]/nav/ol/li[2]').click()
                time.sleep(3)
                driver.find_element(By.XPATH, dict1[i[:3] + '_off']).click()
                time.sleep(3)
                B = driver.driver.find_element(By.XPATH,
                                               '/html/body/div[1]/div[3]/div[1]/div[1]/div[2]/div[2]/div[2]/div[2]/div[1]/table/tr[1]/td[2]/div/input')
                B.send_keys(i)
                B.send_keys(Keys.ENTER)
                time.sleep(3)
                C = driver.find_element(By.XPATH,
                                        '/html/body/div[1]/div[3]/div[1]/div[1]/div[2]/div[2]/div[2]/div[2]/div[1]/table/tr[3]/td[11]/div/div/p[2]')
                C.click()
                time.sleep(3)
                driver.find_element(By.XPATH,
                                    '/html/body/div[1]/div[3]/div[1]/div[1]/div[2]/div[1]/div[1]/nav/ol/li[2]').click()
                time.sleep(3)
            else:
                C = driver.find_element(By.XPATH,
                                        '/html/body/div[1]/div[3]/div[1]/div[1]/div[2]/div[2]/div[2]/div[2]/div[1]/table/tr[3]/td[11]/div/div/p[2]')
                C.click()
                time.sleep(3)
                driver.find_element(By.XPATH,
                                    '/html/body/div[1]/div[3]/div[1]/div[1]/div[2]/div[1]/div[1]/nav/ol/li[2]').click()
                time.sleep(3)
        else:
            A = driver.find_element(By.XPATH, dict1[i[:3]])
            A.click()
            time.sleep(3)
            B = driver.find_element(By.XPATH,
                                    '/html/body/div[1]/div[3]/div[1]/div[1]/div[2]/div[2]/div[2]/div[2]/div[1]/table/tr[1]/td[2]/div/input')
            B.send_keys(i)
            B.send_keys(Keys.ENTER)
            time.sleep(3)
            C = driver.find_element(By.XPATH,
                                    '/html/body/div[1]/div[3]/div[1]/div[1]/div[2]/div[2]/div[2]/div[2]/div[1]/table/tr[3]/td[11]/div/div/p[2]/img')
            C.click()
            time.sleep(3)
            driver.find_element(By.XPATH,
                                '/html/body/div[1]/div[3]/div[1]/div[1]/div[2]/div[1]/div[1]/nav/ol/li[2]').click()
            time.sleep(3)

    print("请耐心等待所有影像下载完毕，之后按任意键继续")
    os.system('pause')
