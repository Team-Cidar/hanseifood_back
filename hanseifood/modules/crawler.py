import glob
import os
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class ExcelCrawler:
    __driver = None
    __driver_path = ''
    __driver_options = None

    def __init__(self, driver_path):
        # Chrome Driver Path, Options
        options = webdriver.ChromeOptions()
        options.add_argument(
            "user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36")
        options.add_experimental_option("prefs", {'intl.accept_languages': 'ko',  # driver language setting
                                                  "download.default_directory": os.getcwd() + "/datas",  # set download path
                                                  })

        self.__driver_path = driver_path
        self.__driver_options = options

    def getFile(self):
        self.__driver = webdriver.Chrome(executable_path=self.__driver_path, options=self.__driver_options)
        self.__driver.get("https://portal.hansei.ac.kr/portal/default/gnb/hanseiTidings/weekMenuTable.page")
        self.__driver.switch_to.frame("IframePortlet_13444")
        a_tag = WebDriverWait(self.__driver, 10).until(
            EC.visibility_of_element_located(
                (By.XPATH, "/html/body/div/div[3]/form/div/table/tbody/tr[1]/td[2]/span/a")))
        a_tag.click()
        download_a = WebDriverWait(self.__driver, 10).until(EC.visibility_of_element_located(
            (By.XPATH, "/html/body/div[2]/div[3]/div[1]/table[1]/tbody/tr[4]/td/span/a[2]")))
        self.__download_file(download_a)
        self.__driver.close()
        self.__driver.quit()
        return self.__rename_last_downloaded_file()

    def __download_file(self, a_tag):
        download_path = os.getcwd() + '/datas/*'
        files = glob.glob(download_path)
        bef_len = len(files)
        a_tag.click()
        while len(files) == bef_len:
            files = glob.glob(download_path)

    def __rename_last_downloaded_file(self):
        files = glob.glob(os.getcwd() + '/datas/*')
        latest_file = max(files, key=os.path.getctime)
        filename = latest_file.split('/')[-1].split('.')[0]
        new_file_name = time.strftime('%Y%m%d', time.localtime())
        new_path_name = latest_file.replace(filename, new_file_name)
        os.rename(latest_file, new_path_name)
        return new_file_name


if __name__ == '__main__':
    ...
    # driver_path = "./drivers/chromedriver"
    # ex = ExcelCrawler(driver_path)
    # ex.getFile()  # 크롤링, 다운로드, 이름변경 3종 세트 메서드