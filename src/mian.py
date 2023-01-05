#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import os

import getInfo
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import downloadData

if __name__ == "__main__":
    # 输入参数筛选影像条件的参数
    yearB = 2019
    yearE = 2022
    monthB = 6
    monthE = 9
    Cloud = 10
    WRS_X = 119
    WRS_Y = 43

    # 如果你知道你的chromedriver路径，请直接输入，如果不知道请单独输入"0"（不包括引号）代码会帮你找
    Konw_chromePath = "C:\Program Files\Google\Chrome\Application\chromedriver.exe"
    # 这里添加你想要搜索的卫星，包括['LT4_5','LC8','LE7_off','LE7_on']
    satellite_list = ['LC8']
    # 输入输出目录与文件名，构造输出路径
    Info_index = r'L:\大三课程\【周五早上】遥感探测学综合应用\期末'
    Info_name = 'test.csv'
    Info_path = os.path.join(Info_index, Info_name)

    # 获取筛选影像的信息
    chromedriver_path = getInfo.find_chromedriver_path(Konw_chromePath)
    driver = webdriver.Chrome(service=Service(chromedriver_path))
    # 返回并赋值获取的影像的信息列表，输出符合条件的影像信息表格
    out_datalist = getInfo.loop_extract_data(driver, satellite_list, WRS_X, WRS_Y, Cloud, yearB, yearE, monthB, monthE)
    getInfo.out_excel(out_datalist, Info_index, Info_name)

    print("影像信息已获取，准备下载...")
    # 根据获取筛选影像的信息，进行自动化批量下载
    id = downloadData.extract_id(Info_path)
    downloadData.downLoad(driver, id)
