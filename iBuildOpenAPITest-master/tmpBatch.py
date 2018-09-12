#!/usr/bin/env python
# -*- coding: utf-8 -*-

import threading
import queue
import time
import datetime
import json
from MallOpenAPI import OpenAPI
from config import AppConfig


queue     = queue.Queue()
UserCount = 2
my_list = range(UserCount)
for row in my_list[:UserCount]:
    queue.put(row)
ThreadCount = 5


def test_0():
    res = OpenAPI(method='Product.QuerySupplierProductList', data="""
                  {
                  "PageSize": 100,
                  "PageIndex":1,
                  "ProductStatus": 10,
                  "ProductName":"",
                  "IsChoiceProduct": true
                  }
                  """)
    print(json.dumps(res.json(), indent = 4, ensure_ascii = False))
    print(res)


def test_1():
    """Product.CreateSupplierProductGroup：创建普通商品"""
    Product = {
            "GroupName": "BingApiProduct-V1 AutoCreate-勿动",
            "OriginSysNo": 1044,
            "WebCategorySysNo": AppConfig.ENV['Product']['WebCategorySysNo'],
            "PromotionTitle": "这是推广标题",
            "Description": "<!DOCTYPE html><html lang='en'><head><meta http-equiv='Content-Type' content='text/html; charset=UTF-8'><meta http-equiv='x-ua-compatible' content='IE=edge'><title>震坤行采购服务平台 - 全国领先的MRO工业用品一站式采购服务平台</title><!-- title_icon --><meta http-equiv='pragma' content='no-cache'> <meta http-equiv='Cache-Control' content='no-cache, must-revalidate'> <meta http-equiv='expires' content='0'><!-- 通用的css样式放在这里，自定义的放在自己用到的地方 --><link rel='stylesheet' type='text/css' href='https://pathfinder-private.oss-cn-shanghai.aliyuncs.com/Webshop/images/product_detail.css'></head><body><div><!-- 详细信息 start --><div class='detailed_info' id='zkh_cp_detail_info'><div class='detail_content clearfix' id='advantage'><div class='left_imgs'><div id='href01'><h5><div><span>产品介绍 / <i>Introduction</i><em class='triangle01'></em></span></div><em class='slogan'></em><em class='triangle02'></em></h5><h6>产品特点：</h6><p>·Meterbox iLDM全球首创的智能软件和云服务\n·70米距离量程、1毫米的分辨率\n·±1.5毫米高精度 \n·距离、面积和体积轻松计算 \n·勾股定理计算功能、三角形测量功能 \n·连续测量、最大/最小数测量 \n·放样测量、长度累加测量、倾斜角测量\n·底部、顶部和延伸测量切换\n·自动关机功能、背光灯显示\n·IP54防护等级</p><img data-bind='attr: {src: product.urls.product_introduction)}' src='http://pathfinder-private.img-cn-shanghai.aliyuncs.com//PRODUCT/BIG/BIG_AT6743_01.jpg@watermark=1&object=d2F0ZXJtYXJrLnBuZ0AxMDBQ&t=90&p=5&x=10&y=10'></div></div></div><!-- 公司服务信息start --><div class='company_ads' id='contact_us'><table><tbody><tr><th><img src='http://pathfinder-private.oss-cn-shanghai.aliyuncs.com/Webshop/images/icon01.png'></th><td><h5>关于震坤行</h5><p>震坤行（zkh360)----全称为震坤行工业超市。是一个专业铸就自信、着眼长远发展、并且乐于承担社会责任的团队，竭诚期待与您的合作！</p></td></tr><tr><th><img src='http://pathfinder-private.oss-cn-shanghai.aliyuncs.com/Webshop/images/icon02.png'></th><td><h5>正品保证</h5><p>震坤行工业超市向您保证所售商品均为正品行货，开具正规发票。</p></td></tr><tr><th><img src='http://pathfinder-private.oss-cn-shanghai.aliyuncs.com/Webshop/images/icon03.png'></th><td><h5>全场免运费</h5><p>自 2014 年8月25日起，我司实行全线免运费的运输收费标准，不论普货或危险品，不论购买数量和金额，皆可享受我司的免费配送服务。</p></td></tr><tr><th><img src='http://pathfinder-private.oss-cn-shanghai.aliyuncs.com/Webshop/images/icon04.png'></th><td><h5>退换货无忧</h5><p>凭质保证书及震坤行发票，可享受全国联保服务，与您亲临商场选购的商品享受相同的质量保证。如有任何问题均可安全退换货物，请您放心购买！</p></td></tr></tbody></table></div><!-- 公司服务信息end --></div></div></body></html>",
            "IsTax": 1,
            "PublishState": 0,
            "UnitSysNo": 2,
            "ProductImageList": [
                {
                    "ImagePath": "https://img30.360buyimg.com/popWaterMark/jfs/t12148/5/761348074/234655/8b1c49bc/5a12b67eNbea9ed12.jpg",
                    "IsCommonDefault": True
                },
                {
                    "ImagePath": "https://img30.360buyimg.com/popWaterMark/jfs/t4387/47/4579786031/87655/f6bda6a5/591160e7N73d243b2.jpg",
                    "IsCommonDefault": False
                }
            ],
            "ProductList": [
                {
                    "Price": 100,
                    "TotalQty": 50,
                    "ChoicePrice": 90,
                    "ProductProperty": AppConfig.ENV['Product']['ProductProperty'][0]
                },
                {
                    "Price": 120,
                    "TotalQty": 60,
                    "ChoicePrice": 95,
                    "ProductProperty": AppConfig.ENV['Product']['ProductProperty'][1]
                }
            ]
        }
    # print (json.dumps(Product, indent=4, ensure_ascii=False))
    res = OpenAPI(method='Product.CreateSupplierProductGroup', data=json.dumps(Product))
    print(json.dumps(res.json(), indent = 4, ensure_ascii = False))


def _run():
    while 1:
        try:
            row = queue.get_nowait()
            try:
                print(row)
                print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3])
                test_1()
            except Exception as ee:
                print(ee)
                print(row[0], 'error')
        except Exception as e:
            print(e)
            return


if __name__ == "__main__":
    ts = [threading.Thread(target=_run, name='threading1') for i in range(ThreadCount)]
    for t in ts:
        t.start()
    t.join()
