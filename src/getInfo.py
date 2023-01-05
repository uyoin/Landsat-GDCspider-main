import os
import time
import tqdm.notebook
from tqdm import tqdm
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

_chromedriver_path_cache = {}


def find_chromedriver_path(Konw_chromePath):
    if Konw_chromePath == 0:
        if "chromedriver_path" in _chromedriver_path_cache:
            return _chromedriver_path_cache["chromedriver_path"]
        else:
            chromedriver_path = None
            for root, dirs, files in tqdm(os.walk("C:\\"), desc="Searching for chromedriver.exe"):
                for file in files:
                    if file == "chromedriver.exe":
                        chromedriver_path = os.path.join(root, file)
                        break
            if chromedriver_path is None:
                _chromedriver_path_cache[
                    "chromedriver_path"] = "Your computer does not have chromedriver, please install it first!"
                return "Your computer does not have chromedriver, please install it first!"
            else:
                _chromedriver_path_cache["chromedriver_path"] = chromedriver_path
                return chromedriver_path
    else:
        chromedriver_path = Konw_chromePath
        return chromedriver_path


def extract_data(driver, satellite, num, cloud, year_range, month_range):
    # num是条带号和行编号，比如num=[123,40]
    [x_num, y_num] = num
    year = [str(i) for i in year_range]
    # 各个卫星及其对应的表单网址，如有需要可以自行添加新卫星的名称和对应网站
    dict1 = {}
    dict1['LT4_5'] = 'http://www.gscloud.cn/sources/accessdata/243?pid=1'  # TM传感器
    dict1['LC8'] = 'http://www.gscloud.cn/sources/accessdata/411?pid=263'  # OLI传感器
    dict1['LE7_off'] = 'http://www.gscloud.cn/sources/accessdata/241?pid=263'  # ETM传感器
    dict1['LE7_on'] = 'http://www.gscloud.cn/sources/accessdata/242?pid=1'  # ETM传感器
    #

    driver.get(dict1[satellite])
    time.sleep(3)
    B = driver.find_element(By.XPATH,
                            '/html/body/div[1]/div[3]/div[1]/div[1]/div[2]/div[2]/div[2]/div[2]/div[1]/table/tr[1]/td[3]/div/input')
    B.send_keys(str(x_num))
    C = driver.find_element(By.XPATH,
                            '/html/body/div[1]/div[3]/div[1]/div[1]/div[2]/div[2]/div[2]/div[2]/div[1]/table/tr[1]/td[4]/div/input')
    C.send_keys(str(y_num))
    E = driver.find_element(By.XPATH,
                            '/html/body/div[1]/div[3]/div[1]/div[1]/div[2]/div[2]/div[2]/div[2]/div[1]/table/tr[1]/td[6]/div/input')
    E.send_keys(str(cloud))

    r = []
    for j in range(len(year)):
        D = driver.find_element(By.XPATH,
                                '/html/body/div[1]/div[3]/div[1]/div[1]/div[2]/div[2]/div[2]/div[2]/div[1]/table/tr[1]/td[5]/div/input')
        D.clear()
        D.send_keys(year[j])
        D.send_keys(Keys.ENTER)
        time.sleep(3)

        # 跳过空条目的年份
        q = driver.find_element(By.XPATH,
                                '/html/body/div[1]/div[3]/div[1]/div[1]/div[2]/div[2]/div[2]/div[2]/div[1]/table/tr[3]/td').text
        if str(q) == "没有记录！": continue

        while True:
            # 把同一页每一行数据的信息存入list1中；list1=[[数据标识],[日期],[云量],[数据有无]]
            list1 = [[], [], [], []]
            x = driver.find_elements(By.XPATH,
                                     '/html/body/div[1]/div[3]/div[1]/div[1]/div[2]/div[2]/div[2]/div[2]/div[1]/table/tr')
            for i in range(3, len(x) + 1):
                date = driver.find_element(By.XPATH,
                                           '/html/body/div[1]/div[3]/div[1]/div[1]/div[2]/div[2]/div[2]/div[2]/div[1]/table/tr[{}]/td[5]'.format(
                                               i)).text
                month = date.split('-')[1]
                if int(month) >= month_range[0] and int(month) <= month_range[1]:
                    biaoshi = driver.find_element(By.XPATH,
                                                  '/html/body/div[1]/div[3]/div[1]/div[1]/div[2]/div[2]/div[2]/div[2]/div[1]/table/tr[{}]/td[2]'.format(
                                                      i))
                    cloud = driver.find_element(By.XPATH,
                                                '/html/body/div[1]/div[3]/div[1]/div[1]/div[2]/div[2]/div[2]/div[2]/div[1]/table/tr[{}]/td[6]'.format(
                                                    i))
                    youwu = driver.find_element(By.XPATH,
                                                '/html/body/div[1]/div[3]/div[1]/div[1]/div[2]/div[2]/div[2]/div[2]/div[1]/table/tr[{}]/td[9]'.format(
                                                    i))
                    if youwu.text == "有":
                        list1[0].append(biaoshi.text)
                        list1[1].append(date)
                        list1[2].append(cloud.text)
                        list1[3].append(youwu.text)
            print(list1)

            for k in range(len(list1[0])):
                n = []
                [n.append(i[k]) for i in list1]
                r.append(n)

            # 判断是否可以往下翻页，可以的话就翻页
            i = driver.find_element(By.XPATH,
                                    '/html/body/div[1]/div[3]/div[1]/div[1]/div[2]/div[2]/div[2]/div[3]/div[2]/table/tr/td[10]/a')
            if i.get_attribute("class") == "l-btn l-btn-plain":
                i.click()
                time.sleep(4)
            else:
                break

    return r


def loop_extract_data(driver, satellite_list, WRS_X, WRS_Y, Cloud, yearB, yearE, monthB, monthE):
    out_datalist = []
    for satellite in satellite_list:
        # satellite, num, cloud, year_range, month_range
        r = extract_data(driver, satellite, [WRS_X, WRS_Y], Cloud, [str(i) for i in range(yearB, yearE)],
                         [monthB, monthE])
        out_datalist += r
    return out_datalist

def out_excel(in_list, out_workspace, filename):
    # 输出符合条件的遥感影像条目
    result_path = os.path.join(out_workspace, filename)
    result = open(result_path, 'w')
    for m in range(len(in_list)):
        for n in range(len(in_list[m])):
            result.write(str(in_list[m][n]))
            result.write(',')
        result.write('\n')
    result.close()


