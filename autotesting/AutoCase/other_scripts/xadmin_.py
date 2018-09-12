# -*- coding: utf-8 -*-

import requests
from pyquery import PyQuery as PQ

session = requests.session()
session.headers.update({'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:39.0) Gecko/20100101 Firefox/39.0'})


def login(username, password):
    url = "http://www.142.com/xadmin/"
    resp = session.get(url)
    data = form_data(resp.text, 'login-form')
    data.update({'username': username, 'password': password})
    # login
    print session.post(url, data=data).text


def form_data(text, form_id):
    data = dict()
    for input in PQ(text)('#{0} input'.format(form_id)):
        _ = PQ(input)
        data[_.attr['name']] = _.attr['value']
    return data


def modpwd(user_id, p1, p2):
    url = 'http://www.142.com/xadmin/mz_user/userprofile/{0}/update/password/'.format(user_id)
    resp = session.get(url)
    data = form_data(resp.text, 'userprofile_form')
    data.update({'password1': p1, 'password2': p2})
    s = session.post(url, data=data).text
    return s


if __name__ == "__main__":
    login('admin@maiziedu.com', 'SV3xOQ02WLP')
    modpwd(10, '11111111', '11111111')