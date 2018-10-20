# -*- coding: utf-8 -*-
# Author： firejq
# Created on 2018-10-04

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from configparser import ConfigParser

import time
import os
import random
import requests
import sys


def getini(conf_path):
    """读取ini配置

    :param conf_path:
    :return:
    """
    dd_path = ''
    cf = ConfigParser()
    try:
        cf.read(conf_path)
        dd_path = cf.get('baseconf', 'download_path')
    except BaseException as e:
        print('没有检测到配置文件，采取默认配置，图片保存在当前 images 目录下。')
    finally:
        if dd_path == '':
            cur_path = os.getcwd().split(os.path.sep)
            dd_path = os.path.sep.join(cur_path) + os.path.sep + 'images'
        return dd_path


def get_ua():
    """获取随机 UA 值

    :return:
    """
    user_agents = [
        ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
         '(KHTML, like Gecko) Chrome/60.0.3072.0 Safari/537.36'),
        ('Mozilla/5.0 (Windows NT 6.1; WOW64; rv:46.0) Gecko/20100101 '
         'Firefox/46.0'),
        ('Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML,'
         ' like Gecko) Chrome/50.0.2661.87 Safari/537.36 OPR/37.0.2178.32'),
        ('Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.57.2 '
         '(KHTML, like Gecko) Version/5.1.7 Safari/534.57.2'),
        ('Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 '
         '(KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36'),
        ('Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 '
         '(KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36'),
        ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
         '(KHTML, like Gecko) Chrome/46.0.2486.0 Safari/537.36 Edge/13.10586'),
        ('Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) '
         'like Gecko'),
        ('Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, '
         'like Gecko) Chrome/47.0.2526.106 BIDUBrowser/8.3 Safari/537.36'),
        ('Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, '
         'like Gecko) Maxthon/4.9.2.1000 Chrome/39.0.2146.0 Safari/537.36'),
        ('Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, '
         'like Gecko) Chrome/47.0.2526.80 Safari/537.36 Core/1.47.277.400 '
         'QQBrowser/9.4.7658.400'),
        ('Mozilla/5.0 (Linux; Android 5.0; SM-N9100 Build/LRX21V) '
         'AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 '
         'Chrome/37.0.0.0 Mobile Safari/537.36 '
         'MicroMessenger/6.0.2.56_r958800.520 NetType/WIFI'),
        ('Mozilla/5.0 (iPhone; CPU iPhone OS 7_1_2 like Mac OS X) '
         'AppleWebKit/537.51.2 (KHTML, like Gecko) Mobile/11D257 '
         'QQ/5.2.1.302 NetType/WIFI Mem/28'),
        ('Mozilla/5.0 (iPod; U; CPU iPhone OS 2_1 like Mac OS X; '
         'ja-jp) AppleWebKit/525.18.1 (KHTML, like Gecko) Version/3.1.1 '
         'Mobile/5F137 Safari/525.20')
    ]
    return random.choice(user_agents)


def get_driver():
    """获取驱动程序

    :return:
    """
    chrome_options = Options()
    # 设置中文
    chrome_options.add_argument('lang=zh_CN.UTF-8')
    # 设置头部
    chrome_options.add_argument(
        'user-agent="' + get_ua() + '"')
    # 设置无 GUI
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    # 加载 chromedriver
    return webdriver.Chrome(
        executable_path='chromedriver.exe',
        chrome_options=chrome_options)


def img_download(img_url):
    """下载单个图片连接

    :param img_url:
    :return:
    """
    # 为图片起名
    name = str(img_url).split('/')[-1]
    # 向图片地址发起请求并获取 response
    headers = {'User-Agent': get_ua()}
    img = requests.get(url=img_url, headers=headers)
    # 在本地以追加模式创建二进制文件
    f = open(name, 'ab')
    # 将response的二进制内容写入到文件中
    f.write(img.content)
    # 关闭文件流对象
    f.close()


if __name__ == '__main__':
    # 获取路径配置
    ini_path = 'tuyimm_scraping.ini'
    download_path = getini(conf_path=ini_path)
    # print(download_path)

    driver = get_driver()
    while True:
        theme_id = input('Please input theme id:')
        if theme_id == 'exit' or theme_id == '':
            break
        elif '-' not in theme_id:
            theme_id += '-1-1'
        url = 'http://www.tuyimm.vip/thread-' + theme_id + '.html'
        # url = 'http://www.tuyimm.vip/thread-16290-1-1.html'
        print('开始检测 ' + url)

        driver.get(url)
        print('网页资源加载完毕')

        # 获取主题标题
        subject = driver.find_element_by_css_selector('#thread_subject').text
        print(subject)
        dirname = subject.replace(' ', '_').replace('\\', '_').replace(
            '/', '_').replace(':', '_').replace('*', '_').replace(
            '?', '_').replace('"', '_').replace('<', '_').replace(
            '>', '_').replace('|', '_')
        path = os.path.join(download_path, dirname)
        if not os.path.exists(path):
            # 创建主题文件夹
            os.makedirs(path)
        else:
            is_continue = input('该主题目录已存在，是否覆盖下载？y/n')
            if is_continue == 'n':
                continue
        # 切换工作目录
        os.chdir(path)

        imgs_small = driver.find_elements_by_class_name('pattimg_zoom')
        print('共检测到' + str(len(imgs_small)) + '张图片')
        pic_num = 0
        for i in range(len(imgs_small) + 1):
            if i == 0:
                ActionChains(driver).click(imgs_small[0]).perform()
                time.sleep(0.5)

            # ActionChains(driver).click(imgs_small[i]).perform()
            # WebDriverWait(driver, 20).until(
            # lambda d: d.find_element_by_id('imgzoom_zoom').is_displayed())

            time.sleep(0.5)
            while True:
                try:
                    img_big = driver.find_element_by_id('imgzoom_zoom')
                    break
                except NoSuchElementException as e:
                    time.sleep(0.5)
                    continue
            try:
                title = driver.find_element_by_class_name('imgzoom_title')
                title = title.text
            except NoSuchElementException as e:
                title = 'None-' + str(i) + '.jpg'
            try:
                img_src = img_big.get_attribute('src')
            except Exception as e:
                print('第' + str(i) + '张图片下载出现问题', title)
                continue
            print('正在下载第' + str(i) + '张图片', title, img_src)
            # 下载图片
            img_download(img_src)
            pic_num += 1

            next_btn = driver.find_element_by_id('zimg_next')
            # close_btn = driver.find_element_by_class_name('imgclose')
            ActionChains(driver).click(next_btn).perform()

        print('下载完成，总计【' + str(pic_num) + '】张图')

    driver.quit()
    print('退出下载工具')
