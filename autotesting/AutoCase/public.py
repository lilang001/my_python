# -*- coding: utf-8 -*-
__author__ = '李朗'
from selenium import webdriver
from mysql import update_output, data
from Autotesing import settings
from datetime import timedelta
import re
import requests



class Driver():
    @staticmethod
    def driver_init():
        try:
            if not hasattr(Driver, 'driver'):
                driver = webdriver.Chrome()
                driver.maximize_window()
                driver.implicitly_wait(10)
        except Exception:
            pass
        return driver

# 登录操作,校验昵称对不对啊
def login_lps(username, password):
    base_url = "http://q.dev.com/"
    driver = Driver.driver_init()
    try:
        driver.get(base_url)
        driver.find_element_by_xpath("//*[@id=\"microoh-navbar-collapse\"]/div[1]/div/a[1]").click()
        driver.find_element_by_id("id_account_l").send_keys(username)
        driver.find_element_by_id("id_password_l").send_keys(password)
        driver.find_element_by_id("login_btn").click()
        actual = driver.find_element_by_xpath("/html/body/div[3]/header/div/div[2]/div[1]/div[1]/dl/dt/a[2]/span").text
    except Exception:
        actual = u'找不到元素'

    expect = data('lps_lilang', 'mz_user_userprofile', ['nick_name'], username=username)[0][0]
    update_output('login_lps', actual, expect)

def equal(method, a, b):
    expect = list()
    actual = list()
    if len(a) == len(b) and len(b) > 0:
        for i, j in zip(a, b):
            for x in range(len(i) if len(i) < len(j) else len(j)):
                c = str(i[x]).replace('"', '').replace(' ', '').replace('\xe2\x80\x8b', '')  # 处理双引号，空格，看不见的空白
                d = str(j[x]).replace('"', '').replace(' ', '').replace('\xe2\x80\x8b', '')
                expect.append(c)
                actual.append(d)
                if c != d:
                    print (u'test', c.encode('gbk', 'ignore'), d.encode('gbk', 'ignore'))
    else:
        expect.append('fuck')
        actual.append('fuck_off')
    update_output(method, ','.join(expect), ','.join(actual))

emoticon_dict = {'\U0001F60A': '01', '\U0001F603': '02', '\U0001F61E': '03', '\U0001F620': '04', '\U0001F61C': '05',
              '\U0001F60D': '06', '\U0001F613': '07', '\U0001F625': '08', '\U0001F60F': '09', '\U0001F614': '10',
              '\U0001F601': '11', '\U0001F609': '12', '\U0001F623': '13', '\U0001F616': '14', '\U0001F62A': '15',
              '\U0001F61D': '16', '\U0001F60C': '17', '\U0001F628': '18', '\U0001F637': '19', '\U0001F633': '20',
              '\U0001F612': '21', '\U0001F630': '22', '\U0001F632': '23', '\U0001F62D': '24', '\U0001F602': '25',
              '\U0001F622': '26', '\U0000263A': '27', '\U0001F604': '28', '\U0001F621': '29', '\U0001F61A': '30',
              '\U0001F618': '31', '\U0001F631': '32', '\U0001F47F': '33', '\U0001F431': '34', '\U0001F42F': '35',
              '\U0001F43B': '36', '\U0001F436': '37', '\U0001F435': '38', '\U0001F437': '39', '\U0001F47D': '40',
              '\U0001F4A9': '41', '\U0001F44D': '42', '\U0001F44E': '43', '\U0001F44C': '44', '\U0001F44F': '45',
              '\U0001F446': '46', '\U0001F447': '47', '\U0001F448': '48', '\U0001F449': '49', '\U00002764': '50',
              '\U0001F494': '51', '\U0001F389': '52', '\U00002197': '53', '\U00002196': '54', '\U00002198': '55',
              '\U00002199': '56'
                 }

def content_deal(content):
    emoticon = re.compile(r'\\U[0-9A-Fa-f]{8}')
    emoticon_codes = emoticon.findall(content)
    for emoticon_code in emoticon_codes:
        if emoticon_dict.has_key(emoticon_code):
            text = ''.join(('<img ', 'src="', settings.SITE_URL,
                            'group/static/ueditor/dialogs/emoji/images/emoji_00',
                            emoticon_dict[emoticon_code], '.gif" _src="', settings.SITE_URL,
                            'group/static/ueditor/dialogs/emoji/images/emoji_00',
                            emoticon_dict[emoticon_code], '.gif">'))
            content = content.replace(emoticon_code, text)
    return content

def time_deal(my_time):
    my_time = int(my_time)
    if timedelta(seconds=my_time).days/365 > 0:
        return str(timedelta(seconds=my_time).days/365)+'年前'
    elif timedelta(seconds=my_time).days/30 > 0:
        return str(timedelta(seconds=my_time).days/30)+'个月前'
    elif timedelta(seconds=my_time).days > 0:
        return str(timedelta(seconds=my_time).days)+'天前'
    elif my_time/3600 > 0:
        return str(my_time/3600)+'小时前'
    elif my_time/60 > 0:
        return str(my_time/60)+'分钟前'
    else:
        return '刚刚'

def login_by_res(name, pwd):
    ses = requests.session()
    header = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.89 Safari/537.36",
           "Referer": settings.SITE_URL}
    form_data = {'account_l': name, 'password_l': pwd}
    # post 换成登录的地址，模拟登录
    ses.post('http://www.142.com/user/login/', data=form_data, headers=header)
    return ses

def modify_pwd():
    ses = requests.session()
    header = {'Cookie': 'csrftoken=KwGVLi5gm9Tr8cbQhbm1PAU05rrDPezg',
              'Referer': 'http://www.142.com/xadmin/',
              'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:39.0) Gecko/20100101 Firefox/39.0'}
    form_data = {'csrfmiddlewaretoken': 'KwGVLi5gm9Tr8cbQhbm1PAU05rrDPezg',
                 'username': 'admin@maiziedu.com',
                 'password': 'SV3xOQ02WLP',
                 'this_is_the_login_form': '1',
                 'next': '/xadmin/'}
    # post 换成登录的地址，模拟登录
    ses.post('http://www.142.com/xadmin/', data=form_data, headers=header)
    # ses.get('http://www.142.com/xadmin/mz_user/userprofile/?_q_=rocky%40maiziedu.com')
    md_pass = ses.get('http://www.142.com/xadmin/mz_user/userprofile/7/update/password/')
    token = md_pass.cookies._cookies['.142.com']['/']['csrftoken'].value
    data_pwd = {'None': u'修改密码',
                 'csrfmiddlewaretoken': token,
                 'password1': '11111111',
                 'password2': '11111111'}
    header2 = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:39.0) Gecko/20100101 Firefox/39.0'}
    res = ses.post('http://www.142.com/xadmin/mz_user/userprofile/7/update/password/', data=data_pwd, headers=header2)
    result = res.text

    return result

def test_login():
    header = {'Cookie': 'maiziedu=i7u8ojgw1mdm4yvk9ulpngnm2cvurkbd'}
    s = requests.get('http://121.199.32.122/', headers=header)
    s.text
    print (s.text)


if __name__ == "__main__":
    modify_pwd()


