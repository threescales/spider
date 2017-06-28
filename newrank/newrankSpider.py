#coding=utf-8
import sys
import time
import io
import json
import urllib
import urllib2
import hashlib
import requests
import numpy as np
from bs4 import BeautifulSoup
from openpyxl import Workbook
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from pyvirtualdisplay import Display


reload(sys)
sys.setdefaultencoding('utf8')


# Some User Agents
hds = [{'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'},
       {'User-Agent': 'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.12 Safari/535.11'},
       {'User-Agent': 'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Trident/6.0)'}]


from random import Random
#生成随机数
def random_str(randomlength=9):
    str = ''
    chars = 'abcdefghijklmnopqrstuvwxyz0123456789'
    length = len(chars) - 1
    random = Random()
    for i in range(randomlength):
        str+=chars[random.randint(0, length)]
    return str

#md5加密方法
def md5(str):
    import hashlib
    m = hashlib.md5()   
    m.update(str)
    return m.hexdigest()

#获取加密参数
def getsign(url,params):
    i = url+'?AppKey=joker&'
    randomStr = random_str()
    items = params.items()
    items.sort()
    for key,value in items:
        param = key+'='+value+'&'
        i+=param
    i += 'nonce='+ randomStr
    print i
    xyz = md5(i)
    params['nonce']=randomStr
    params['xyz']=xyz
    return params

#获取参数
def getParams():
    params={}
    params['end']='2017-05-31'
    params['rank_name']='民生'
    params['rank_name_group']='资讯'
    params['start']='2017-05-01'
    return params

# 保存数据的Excel
def print_lists_excel(wechat_lists, wechat_tag_lists):
    wb = Workbook(optimized_write=True)
    ws = []
    for i in range(len(wechat_tag_lists)):
        # utf8->unicode
        ws.append(wb.create_sheet(title=wechat_tag_lists[i].decode()))
    for i in range(len(wechat_tag_lists)):
        ws[i].append(['序号', '书名', '评分', '评价人数', '作者', '出版社'])
        count = 1
        for bl in wechat_lists:
            ws[i].append([count, bl['name'], bl['b'],
                          bl['c'], bl['d'], bl['e']])
            count += 1
    save_path = 'book_list'
    for i in range(len(wechat_tag_lists)):
        save_path += ('-' + wechat_tag_lists[i].decode())
    save_path += '.xlsx'
    wb.save(save_path)


#获取排行榜列表
def getRankList():
   url = 'http://www.newrank.cn/xdnphb/list/month/rank' 
   datas = getsign('/xdnphb/list/month/rank',getParams())
   try:
       data = urllib.urlencode(datas)
    
       request = urllib2.Request(url)
       opener = urllib2.build_opener(urllib2.HTTPCookieProcessor())  
       result = opener.open(request,data).read()
       return json.loads(result)
   except (urllib2.HTTPError, urllib2.URLError), e:
       print e
       return {}

#启动firefox
def setup():
    browser = webdriver.Firefox()
    return browser

#模拟登陆
def login(username, password, browser=None):
    browser.get("http://www.newrank.cn/public/login/login.html")
    tab = browser.find_elements_by_class_name('login-normal-tap')[1]
    tab.click()
    pwd_btn = browser.find_element_by_id('password_input')
    act_btn = browser.find_element_by_id("account_input")
    submit_btn = browser.find_element_by_id("pwd_confirm")  

    act_btn.send_keys(username)
    pwd_btn.send_keys(password)
    submit_btn.click()
    time.sleep(5)
    return browser

#request加cookies
def set_session(browser):
    request = requests.Session()
    request.headers.update(hds[1])
    cookies = browser.get_cookies()
    for cookie in cookies:
        request.cookies.set(cookie['name'],cookie['value'])
    return request


#获取公众号详情页面
def getDetail(account):
    account='hifm93'
    url='http://www.newrank.cn/public/info/detail.html?account='+account

    try:
        req = urllib2.Request(url, headers=hds[1])
        source_code = urllib2.urlopen(req).read()
        plain_text = str(source_code)
        print plain_text
    except (urllib2.HTTPError, urllib2.URLError), e:
        print e
        

if __name__ == '__main__':
    #rankList = getRankList()['value']
    #print_lists_excel(rankList,['民生'])
    browser = login('18624382369','12345678',setup())
    rq = set_session(browser)
    response = rq.get('http://www.newrank.cn/public/info/detail.html?account=hifm93')
    print '广播之声+++++++++++++++++++++++++++++++++++++++++++'+response.text
    response = rq.get('http://www.newrank.cn/public/info/detail.html?account=rmrbwx')
    print '人民日报+++++++++++++++++++++++++++++++++++++++++++'+response.text