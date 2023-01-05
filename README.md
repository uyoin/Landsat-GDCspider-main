# Landsat-GDCspider-main
本项目通过selenium库实现地理空间数据云Landsat影像的自动提取与下载。

# 所需库
``` python
import os
import getInfo
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import downloadData
``` 
# 使用
## 打开“main.py”代码，输入以下参数：
### ①yearB：搜寻影像的开始年份，例如：2002
### ②yearE ：搜寻影像的结束年份，例如：2022
### ③monthB：搜寻影像的开始月份，例如：5
### ④monthE：搜寻影像的结束月份，例如：6
### ⑤Cloud：搜寻影像的最大云量，例如：10
### ⑥WRS_X ：WRS带号（X），例如：119
### ⑥WRS_Y ：WRS带号（Y），例如：43
### ⑧Konw_chromePath：如果你知道你的chromedriver路径，请直接输入，如果不知道请单独输入"0"（不包括引号）代码会帮你找
### ⑨satellite_list：这里添加你想要搜索的卫星，包括['LT4_5','LC8','LE7_off','LE7_on']
### ⑩Info_index、Info_name：输入输出目录与文件名，构造输出路径，例如Info_index = r'L:\大三课程\【周五早上】遥感探测学综合应用\期末'，Info_name = 'test.csv'
# 说明
这里说明的是为什么使用selenium库，而不是请求URL法。首先，之前曾写过几次URL请求，感觉挺熟悉了，所以就想换一种方式去爬取数据。其次就是地理空间数据云这个网站很容易发现你下载频率过快，所以我认为selenium库是模拟人类行为进行点击元素的，应该是比较不容易被发现，至少我在测试的过程中并没有被发现。之后就是cookie的说明，之前在写URL请求都是直接用head参数构造一个表头，而cookie就直接写在里面的。然而因为第一次用selenium库，而且这也不是重点所以没有花时间去研究selenium库的cookie要怎么去给他提交请求。现在我对此进行了研究，发现可以WebDriver的add_cookie方法来添加Cookie:driver.add_cookie（cookie），cookie参数即是事先准备的好的cookie
# 代码主要功能与实现大致流程原理
本项目分为三个部分：“mian.py”、“downloadData.py”、“getInfo.py”，  
其中“mian.py”是主函数，在此设置程序的主入口，调用“downloadData.py”、“getInfo.py”所编写的函数进行基于地理空间数据云图像批量自动化信息爬取与自动下载流程。 
## getInfo.py
“getInfo.py”组成：find_chromedriver_path(Konw_chromePath)、extract_data(driver, satellite, num, cloud, year_range, month_range)、loop_extract_data(driver, satellite_list, WRS_X, WRS_Y, Cloud, yearB, yearE, monthB, monthE)、out_excel(in_list, out_workspace, filename)。  
  ①其中find_chromedriver_path（Konw_chromePath）函数主要功能是在计算机中查找ChromeDriver的路径，如果已知ChromeDriver的路径，直接在参数中写入实际的路径，则直接返回路径，否则，会在你的电脑中遍历所有文件夹，查找名为“chromedriver.exe”的文件，如果找到，则返回文件的路径，否则返回错误信息“Your computer does not have chromedriver，please install it first！”。  
  ②extract_data（driver，satellite，num，cloud，year_range，month_range）函数主要功能是使用Selenium库爬取地理空间数据云遥感影像数据，首先使用Selenium库中的WebDriver对象来打开浏览器，根据用户输入的卫星名称、条带号、行编号、云量和时间范围，向网站的搜索表单中输入信息。之后提交表单，获取搜索结果，并遍历所有年份，每次输入一个年份，提交表单。判断该年份是否有数据，如果没有则跳过。对于每个年份，遍历所有月份，每次输入一个月份，并提交表单。判断该月份是否有数据，如果没有则跳过。提取搜索结果中的有效数据，保存到清单中，将清单中的数据输出到Excel档案中，最后关闭浏览器。  
  ③loop_extract_data（driver，satellite_list，WRS_X，WRS_Y，Cloud，yearB，yearE，monthB，monthE）函数主要功能是循环调用extract_data函数，批量爬取遥感影像数据。首先遍历卫星list中的每个卫星，并调用extract_data函数爬取该卫星的遥感影像数据。之后将爬取到的数据保存到list中，最后返回所有卫星的数据list。
  ④out_excel（in_list，out_workspace，filename）函数主要功能是。首先构造档案路径，并使用open函数打开文件。遍历输入的数据list，将每一行数据的每一项写入档案中，并在每一行的末尾换行，最后关闭文件。 
## downloadData.py
“downloadData.py”由两个函数组成：extract_id（csv_file）、download（driver，data_list）。  
  ①其中extract_id（csv_file）函数主要功能是读取csv文件（也就是刚刚筛选提取的图像信息）并返回第一列的所有值（图像识别码）的列表。首先，打开csv文件。然后创建一个csv读取器对象，之后迭代csv文件中的行。而对于每行，将第一列的值添加到列表中。最后，返回第一列的值的列表。  
  ②download（driver，data_list）函数主要功能是使用Selenium库登入地理空间数据云平台，并在平台上搜索指定的遥感影像数据条目，然后将这些条目下载到本地。首先会打开地理空间数据云平台的登入页面，然后输入用户的帐号和密码。然后，会等待输入验证码，并在输入后模拟点击登入按钮。登录后，会跳转到公开数据页面，并在该页面上根据extract_id（csv_file）函数返回的图像识别码列表搜索指定的遥感影像数据条目，然后将其下载到本地。  
# 致谢
本项目为了实现徐逸祥老师所上的“遥感探测学综合应用”课程的期末汇报而做，感谢老师提供的机会与指导。
