import os
import random

import requests
import time
from bs4 import BeautifulSoup


def getips():
    '''
    爬取http://www.xicidaili.com/nn/首页的高匿代理ip
    :return: 代理ip列表
    '''
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'
    }
    url = 'http://www.xicidaili.com/nn/'
    web_data = requests.get(url, headers=headers)
    soup = BeautifulSoup(web_data.text, 'lxml')
    ips = soup.find_all('tr')
    ip_list = []
    for i in range(1, len(ips)):
        ip_info = ips[i]
        tds = ip_info.find_all('td')
        ip_list.append(tds[1].text + ':' + tds[2].text)
    return ip_list



def get(url, timeout=None, proxy=None, num_retries=6):
    '''
    自定义请求逻辑：
    先尝试直接连接请求，随机使用User-Agent，
    若请求失败，重试6次，
    若重试6次之后仍旧失败，开始使用代理ip，
    若使用代理ip请求失败，则随机更换代理ip，最高尝试更换6次代理ip，
    更换6次代理ip后仍旧请求失败，放弃使用代理，延长timeout直接连接
    :param url: 
    :param timeout: 
    :param proxy: 
    :param num_retries: 
    :return: 
    '''
    UserAgents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3072.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:46.0) Gecko/20100101 Firefox/46.0',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.87 Safari/537.36 OPR/37.0.2178.32',''
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.57.2 (KHTML, like Gecko) Version/5.1.7 Safari/534.57.2',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2486.0 Safari/537.36 Edge/13.10586',
        'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 BIDUBrowser/8.3 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Maxthon/4.9.2.1000 Chrome/39.0.2146.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36 Core/1.47.277.400 QQBrowser/9.4.7658.400',
        'Mozilla/5.0 (Linux; Android 5.0; SM-N9100 Build/LRX21V) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/37.0.0.0 Mobile Safari/537.36 MicroMessenger/6.0.2.56_r958800.520 NetType/WIFI',
        'Mozilla/5.0 (iPhone; CPU iPhone OS 7_1_2 like Mac OS X) AppleWebKit/537.51.2 (KHTML, like Gecko) Mobile/11D257 QQ/5.2.1.302 NetType/WIFI Mem/28'
    ]
    headers = {'User-Agent': random.choice(UserAgents)}
    if proxy is None:
        try:
            return requests.get(url, headers=headers, timeout=timeout)
        except:
            if num_retries > 0:  # num_retries:限定的重试次数
                print(u'获取网页出错，10s后将重新获取，倒数第：', num_retries, u'次')
                time.sleep(10)
                return get(url, timeout, num_retries=(num_retries-1))
            else:
                print(u'重试6次失败，开始使用代理')
                time.sleep(10)
                iplist = getips()
                IP = ''.join(str(random.choice(iplist)).strip())
                proxy = {'http': IP}
                return get(url, timeout, proxy)
    else:
        try:
            iplist = getips()
            IP = ''.join(str(random.choice(iplist)).strip())
            proxy = {'http': IP}
            print(u'当前代理是：', proxy)
            return requests.get(url, headers=headers, proxies=proxy)
        except:
            if num_retries > 0:
                time.sleep(10)
                iplist = getips()
                IP = ''.join(str(random.choice(iplist)).strip())
                proxy = {'http': IP}
                print(u'使用代理获取网页失败，正在更换代理，10S后将重新获取倒数第', num_retries, u'次')
                print(u'当前代理是：', proxy)
                return get(url, timeout, proxy, num_retries - 1)
            else:
                print(u'更换6次代理仍旧失败，代理可能已失效，取消代理')
                return get(url, 3)


for start_page_index in range(1, 47 + 1):
    # 爬取第start_page_index页
    start_url = 'http://www.bh-bj.com/category/fuliba/page/' + str(start_page_index)
    start_html = get(start_url)
    bs = BeautifulSoup(start_html.text, 'lxml')
    print('开始爬取第' + str(start_page_index)+ '页')
    # 获取当前页的所有文章并遍历
    articles = bs.findAll('article', class_='excerpt excerpt-one')
    for article_index in range(0, articles.__len__()):
        # 爬取当前页第article_index+1篇文章
        article_name = articles[article_index].find('header').find('h2').find('a').text

        # 创建文件夹存放当前文章主题的所有图片
        dirname = article_name.replace(' ', '_').replace('\\', '_').replace('/', '_').replace(':', '_').replace(
            '*', '_').replace('?', '_').replace('"', '_').replace('<', '_').replace('>', '_').replace('|', '_')
        path = os.path.join('D:\\fuliba', dirname)
        if os.path.exists(path):
            print('文件夹已存在，进行下一个主题的爬取')
            continue
        else:
            os.makedirs(path)
            os.chdir(path)
            print(article_name)

            article_href = articles[article_index].find('header').find('h2').find('a')['href']
            article_html = get(article_href)

            article_soup = BeautifulSoup(article_html.text, 'lxml')
            article_last_page = article_soup.find('div', class_='article-paging').findAll('span')[-1].text
            for page_index in range(1, int(article_last_page) + 1):
                # 爬取文章中的第page_index页
                article_page_url = article_href + '/' + str(page_index)
                article_page_soup = BeautifulSoup(get(article_page_url).text, 'lxml')
                # 获取当前页面的所有图片并遍历

                flag = 0
                while flag == 0:
                    try:
                        article_content = article_page_soup.find('article', class_='article-content')
                        article_imgs = article_content.findAll('img')
                        flag = 1
                    except AttributeError:
                        print('捕获AttributeError异常，1s后重试，当前article_content：' + str(article_content))
                        time.sleep(1)
                        continue

                for article_img_index in range(0, article_imgs.__len__()):
                    # 爬取当前页面的第article_img_index张图片
                    # 获取图片地址
                    article_img_src = article_imgs[article_img_index]['src']
                    # 为图片起名
                    name = str(article_img_src).split('/')[-1]
                    # 向图片地址发起请求并获取response
                    img = get(article_img_src)
                    # 在本地以追加模式创建二进制文件
                    f = open(name, 'ab')
                    # 将response的二进制内容写入到文件中
                    f.write(img.content)
                    # 关闭文件流对象
                    f.close()


print('第' + start_page_index + '页爬取完毕')
