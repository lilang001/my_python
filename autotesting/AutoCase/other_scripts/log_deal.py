# _*_ coding:utf-8 _*_
__author__ = 'Administrator'


filepath = u'D:\Autotesing\\trunk\AutoCase\other_scripts\\nginx_201604091200.log'

buff = list()

with open(filepath, 'rb') as f:
    for line in f:
        ip = line.split('- -')[0]
        time = line.split(' +0800')[0].split('/')[-1]
        way = line.split('"')[1].split('/')[0]
        url = line.split('"')[1].replace('GET ', '').split(' HTTP')[0]
        http = line.split('"')[1].replace('GET ', '').split(' ')[-1]
        status = line.split('"')[2].split(' ')[1]
        code = line.split('"')[2].split(' ')[2]
        source_url = line.split('"')[4]
        browser = line.split('"')[5]
        buff.append(ip+'~'+time+'~'+way+'~'+url+'~'+http+'~'+status+'~'+status+'~'+code+'~'+source_url+'~'+browser+'\n')
with open('D:\Autotesing\\trunk\AutoCase\other_scripts\\test2.txt', 'wb') as f:
    f.writelines(buff)