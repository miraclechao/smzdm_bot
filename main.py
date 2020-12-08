"""
什么值得买自动签到脚本
使用github actions 定时执行
@author : stark
"""
import requests,os
from sys import argv

import config
from utils.serverchan_push import push_to_wechat

import requests
import re
#添加请求头信息
headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36'     
    }
def get_detailurl():
    menu = ['bingtong','erjiaben','jiachun','cusuan']
    base_url = 'http://jiage.cngold.org/{}/'
    detail_urls = []
    for i in menu:
        detail_url = base_url.format(i)
        # print(detail_url)
        detail_urls.append(detail_url)
    lis = []
    for detail_url in detail_urls:
        resp = requests.get(detail_url,headers = headers)
        resp.encoding = 'utf-8'
        html = resp.text
        li = re.findall(r'''<div.*?news_list_lab.*?href="(.*?)"\starget''',html,re.VERBOSE|re.DOTALL)
        lis.append(li[0])
        # print(lis)
    return lis
def parse_detail_url(lis):
    end_results = []
    for li in lis:
        resp = requests.get(li,headers = headers)
        resp.encoding = 'utf-8'
        html = resp.text
        lis = re.findall(r'''<th\scolspan.*?>(.*?)</th>''',html,re.VERBOSE|re.DOTALL)[0][0:13]
        mingcheng = re.findall(r'''<th\scolspan.*?td>(.*?)</td>''',html,re.VERBOSE|re.DOTALL)
        lis1 = re.findall(r'''<th\scolspan.*?td>.*?</td>.*?<td>(.*?)</td>''',html,re.VERBOSE|re.DOTALL)
        lis2 = re.findall(r'''<th\scolspan.*?td>.*?</td>.*?<td>.*?</td>.*?<td>.*?</td>.*?<td>(.*?)</td>''',html,re.VERBOSE|re.DOTALL)
        mingcheng = "".join(mingcheng[0].split())
        lis1 = "".join(lis1[0].split())
        lis2 = "".join(lis2[0].split())
        end_result = str(lis+mingcheng+' '+lis1+'元/吨。对比昨日价格'+lis2[0])
        # print(end_result)
        end_results.append(end_result)
    # print(end_results)
    end_result = '\n'.join(end_results)
    return end_result  
def main():
    lis = get_detailurl()
    end_result = parse_detail_url(lis)
    print(end_result)
    api = "https://sc.ftqq.com/SCU122408T2c2ede4298638d75f2240b174765a0ec5f9e6f114d95f.send"
    title = u"溶剂价格"
    content = end_result
    data = {
    "text":title,
    "desp":content
    }
    req = requests.post(api,data = data)
if __name__ == "__main__":
    main() 
    
