# -*- coding: utf-8 -*-
__author__ = 'admin'
import time
import random
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from login import login

def create_tender():
    driver = login('lilang1', '111111')
    time.sleep(2)
    driver.get('http://portal.jc.yzw.cn.qa:8000/TenderMgt/TenderInvitation/TenderCategory')  # 进入招标创建页面
    # wait = WebDriverWait(driver, 10)
    # wait.until(lambda x: x.find_element_by_xpath(u'//*[@id="btnSubmitData"]/div/a/span')).click()

    # 招标类型选择页面：物资招标、劳务招标、乱七八糟招标
    driver.find_element_by_xpath('//div[2]/div[1]/div/form/p/a').click()  # 选择物资招标
    time.sleep(1)
    # 物资选择页面
    driver.find_element_by_xpath('//*[@id="frmCategory"]/ul/li[1]/label').click()   # 选择品类， 开始下一步
    time.sleep(2)
    driver.find_element_by_xpath('/html/body/div[8]/div/div/div[3]/div[3]/a').click()   # 点击开始招标
    # 采购类型选择页面
    driver.find_element_by_xpath('//*[@id="frmStep3"]/div[2]/div/div/div/label[1]/span').click()
    driver.find_element_by_xpath('/html/body/div[8]/div/div/div[3]/div[3]/button[2]').click()
    # 招标方式选择页面
    driver.find_element_by_xpath('/html/body/div[8]/div/div/div[3]/div[3]/button[2]').click()
    # 招标名称金额输入页面
    driver.find_element_by_xpath('//*[@id="frmStep1"]/div[1]/div/div/div/input').send_keys(u'李朗测试招标')   # 招标名称
    driver.find_element_by_xpath('//*[@id="frmStep1"]/div[2]/div/div/div/input').send_keys(u'2455')   # 输入招标金额
    driver.find_element_by_xpath('/html/body/div[8]/div/div/div[3]/div[3]/button[2]').click()  # 内容-名称金额下一步
    # 组织架构、经办人选择页面
    driver.find_element_by_xpath('/html/body/div[8]/div/div/div[3]/div[3]/button[2]').click()  # 经办人选择后来个下一步
    # 项目选择页面
    driver.find_element_by_xpath('//*[@id="frmStep4"]/div/div/div/div[2]/input').click()
    driver.find_element_by_xpath('//*[@id="MultiProjectSelectorTable"]/tbody/tr[2]/td[1]/input').click()  # 选择项目
    driver.find_element_by_xpath('//*[@id="btnMultiProjectSelectorConfirm"]').click()  # 确定一下
    driver.find_element_by_xpath('/html/body/div[8]/div/div/div[3]/div[3]/button[2]').click()  # next
    # 合同类型选择页面
    driver.find_element_by_xpath('/html/body/div[8]/div/div/div[3]/div[3]/button[2]').click()  # next 采购合同
    # 确定是否根据清单分别确定中标供应商页面
    driver.find_element_by_xpath('/html/body/div[8]/div/div/div[3]/div[3]/button[2]').click()  # next 不根据清单
    # 概要汇总页面--拓展不同场景在这里玩下去
    driver.find_element_by_xpath('/html/body/div[8]/div/div/div[3]/div[3]/button[2]').click()  # next 概要汇总来个下一步
    # 招标清单选择页面--但清单和多清单在这玩
    driver.find_element_by_xpath('//*[@id="Template_Name"]').send_keys('03')  # 输入清单名称
    driver.find_element_by_xpath('//*[@id="btnQuery"]').click()  # 点击查询清单
    driver.find_element_by_xpath('//*[@id="TenderInvatationTemplateSelectGrid"]/tbody/tr[1]/td[1]/input').click()  # 选择第一个清单
    driver.find_element_by_xpath('//*[@id="btnNext"]').click()  # 下一步进入采购清单
    # 采购清单编辑页面
    driver.find_element_by_xpath('//*[@id="TenderListTableBox"]/div[3]/div/div[2]/div[1]/button[1]').click()  # 新增商品
    driver.find_element_by_xpath('//*[@id="ProductSelectorGrid"]/tbody/tr[1]/td[1]/input').click()  # 选择第一个商品
    driver.find_element_by_xpath('//*[@id="ProductSelectorGrid"]/tbody/tr[2]/td[1]/input').click()  # 选择第二个商品
    driver.find_element_by_xpath('//*[@id="btnSaveProductSelectorInfo"]').click()  # 保存一伙
    el = driver.find_elements_by_class_name('input-sm')
    for i in range(len(el)):
        try:
            el[i].send_keys('122')
        except:
            continue
    driver.find_element_by_xpath('/html/body/div[8]/div/div/div[2]/div[3]/a[2]').click()
    print 'test'





if __name__ == '__main__':
    create_tender()