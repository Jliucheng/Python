import time
from bs4 import BeautifulSoup
import selenium.common.exceptions as ex
from selenium import webdriver
import os
import requests


def progressbar(url, path, name):
    print("准备下载喽，耐心等待一下吧，视频将下载到  {}".format(path))
    if not os.path.exists(path):
        os.mkdir(path)
    start = time.time()
    session = requests.session()
    response = session.get(url, stream=True)
    size = 0
    chunk_size = 1024 * 1024
    content_size = int(response.headers['Content-Length'])
    if response.status_code == 200:
        print('开始下载喽，文件大小：{size:.2f} MB'.format(size=content_size / chunk_size))
        filename = path + '{}.mp4'.format(name)
        with open(filename, 'wb') as f:
            start_time = time.time()
            for data in response.iter_content(chunk_size=chunk_size):
                end_time = time.time()
                f.write(data)
                size += len(data)
                print('\r' + '[下载进度]：{0}{1}    {2:.2f}%    网速：{3:.2f} MB/s'.format('>' * int(size * 20 / content_size),
                                                                '<' * (10 - int(size * 20 / content_size)), size / content_size * 100, size / chunk_size / (end_time - start_time)), end='')
    end = time.time()
    print('\n下载总共耗时: {tim:.2f} 秒'.format(tim=end - start))


class Cartoon:
    def __init__(self):
        # ai_jie_xi_url = 'https://jiexi.t7g.cn/?url='
        self.xiao_xiao_jie_xi = 'https://jx.ihuikr.com/player/analysis.php?v='
        print('''动漫更新时间播报：
                    1、《武庚纪》 每周周四上午十点更新
                    2、《一人之下4》每周周五上午十二点更新
                    3、《斗罗大陆》每周周六上午十点更新
                    4、《魔道祖师》每周周六上午十二点更新''')
        print("选择要看的动漫：1、《武庚纪》  2、《一人之下4》  3、《斗罗大陆》  4、《魔道祖师》")
        self.num = int(input("请输入编号："))
        self.header = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (XHTML, like Gecko) "
                          "Chrome/86.0.4240.198 "
                          "Safari/537.36",
        }
        self.path = 'E:/Videos/'
        if self.num == 1:
            self.video_name = '武庚纪'
            self.movie3()
        elif self.num == 2:
            self.video_name = '一人之下4'
            self.movie()
        elif self.num == 3:
            self.video_name = '斗罗大陆'
            self.movie()
        elif self.num == 4:
            self.video_name = '魔道祖师'
            self.movie2()
        else:
            print("输入编号有误！！！")

    def movie(self):
        response = requests.get('https://v.qq.com/x/search/?q={}&stag=0&smartbox_ab='.format(self.video_name),
                                headers=self.header)
        response.encoding = 'UTF-8'
        soup = BeautifulSoup(response.text, 'lxml')
        Episodes = soup.select(
            'body > div.search_container > div.wrapper > div.wrapper_main > '
            'div:nth-child(2) > div > div._playlist > div > div > div > div > a')
        epi, hre = Episodes[-3].text, Episodes[-3].get('href')
        print("已经更新《{}》第 {} 集，url={}".format(self.video_name, epi, hre))
        url = self.xiao_xiao_jie_xi + hre
        print("1、在线看 2、下载看")
        nu = int(input("请输入选择的序号："))
        if nu == 2:
            driver = webdriver.Chrome("./chromedriver.exe")
            driver.minimize_window()
            driver.get(url)
            time.sleep(2)
            vedio_url = driver.find_element_by_css_selector('#video').get_attribute('src')
            driver.close()
            print("视频源url={}".format(vedio_url))
            progressbar(vedio_url, self.path + self.video_name, '/第{}集'.format(epi))
            print('《{}》  第{}集，已经下载完成了'.format(self.video_name, epi))
        elif nu == 1:
            driver = webdriver.Chrome("./chromedriver.exe")
            driver.get(url)
            time.sleep(2)
            vedio_url = driver.find_element_by_css_selector('#video').get_attribute('src')
            print("视频源url={}".format(vedio_url))
        else:
            print("输入编号有误！！！")

    def movie2(self):
        global href, episode
        driver = webdriver.Chrome("./chromedriver.exe")
        driver.minimize_window()
        selector = 'body > div.search_container > div.wrapper > div.wrapper_main > div:nth-child(2) > div > div._playlist > div > div.tmpinnerList > div > div > span > span > div > a'
        driver.get('https://v.qq.com/x/search/?q={}&stag=0&smartbox_ab='.format(self.video_name))
        # 此处由于《魔道祖师》下面还有很多的a.item_foldmore，所以可以直接循环
        while True:
            if driver.find_element_by_css_selector("a.item_foldmore").get_attribute("data-id") == 'k4mutekomtrdbux':
                driver.find_element_by_css_selector("a.item_foldmore").click()
                time.sleep(2)
            else:
                divs = driver.find_elements_by_css_selector(selector)
                if divs:
                    href = divs[-3].get_attribute('href')
                    episode = divs[-3].text[1:3]
                    print("已经更新《{}》第 {} 集， url={}".format(self.video_name, divs[-3].text[1:3], href))
                break
        url = self.xiao_xiao_jie_xi + href
        print("1、在线看 2、下载看")
        nu = int(input("请输入选择的序号："))
        if nu == 2:
            driver.get(url)
            driver.minimize_window()
            time.sleep(2)
            vedio_url = driver.find_element_by_css_selector('#video').get_attribute('src')
            driver.close()
            progressbar(vedio_url, self.path + self.video_name, '/第{}集'.format(episode))
            print('《{}》  第{}集，已经下载完成了'.format(self.video_name, episode))
        elif nu == 1:
            driver.get(url)
            time.sleep(2)
            driver.maximize_window()
            vedio_url = driver.find_element_by_css_selector('#video').get_attribute('src')
            print("视频源url={}".format(vedio_url))
        else:
            print("输入编号有误！！！")

    def movie3(self):
        global href, episode
        driver = webdriver.Chrome("./chromedriver.exe")
        driver.minimize_window()
        selector = 'body > div.search_container > div.wrapper > div.wrapper_main > div:nth-child(2) > div.result_item.result_item_v > div._playlist > div > div.tmpinnerList > div > div > span > span > div > a'
        driver.get('https://v.qq.com/x/search/?q={}&stag=0&smartbox_ab='.format(self.video_name))
        driver.find_element_by_css_selector(
            'body > div.search_container > div.wrapper > div.wrapper_main > div:nth-child(2) > div.result_item.result_item_v > div._playlist > div > div.result_tabs > a.item._last_tab').click()
        time.sleep(2)
        while True:
            try:
                driver.find_element_by_css_selector("a.item_foldmore")
                if driver.find_element_by_css_selector("a.item_foldmore").get_attribute("data-id") == 'ipmc5u3dwb48mv2':
                    driver.find_element_by_css_selector("a.item_foldmore").click()
                    time.sleep(2)
            except ex.NoSuchElementException:
                divs = driver.find_elements_by_css_selector(selector)
                if divs:
                    href = divs[-2].get_attribute('href')
                    episode = divs[-2].text[1:4]
                    print("已经更新《{}》第 {} 集， url={}".format(self.video_name, episode, href))
                break
        url = self.xiao_xiao_jie_xi + href
        print("1、在线看 2、下载看")
        nu = int(input("请输入选择的序号："))
        if nu == 2:
            driver.get(url)
            driver.minimize_window()
            time.sleep(2)
            vedio_url = driver.find_element_by_css_selector('#video').get_attribute('src')
            print("视频源url={}".format(vedio_url))
            driver.close()
            progressbar(vedio_url, self.path + self.video_name, '/第{}集'.format(episode))
            print('《{}》  第{}集，已经下载完成了'.format(self.video_name, episode))
        elif nu == 1:
            driver.get(url)
            time.sleep(2)
            driver.maximize_window()
            vedio_url = driver.find_element_by_css_selector('#video').get_attribute('src')
            print("视频源url={}".format(vedio_url))
        else:
            print("输入编号有误！！！")


if __name__ == "__main__":
    cartoon = Cartoon()
