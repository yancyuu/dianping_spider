#!/usr/bin/env python
# Desc: 用pyspider来调度
# Created on 2022-06-27 17:00:28
# Project: public_comment
"""
      ┏┛ ┻━━━━━┛ ┻┓
      ┃　　　　　　 ┃
      ┃　　　━　　　┃
      ┃　┳┛　  ┗┳　┃
      ┃　　　　　　 ┃
      ┃　　　┻　　　┃
      ┃　　　　　　 ┃
      ┗━┓　　　┏━━━┛
        ┃　　　┃   神兽保佑
        ┃　　　┃   代码无BUG！
        ┃　　　┗━━━━━━━━━┓
        ┃CREATE BY SNIPER┣┓
        ┃　　　　         ┏┛
        ┗━┓ ┓ ┏━━━┳ ┓ ┏━┛
          ┃ ┫ ┫   ┃ ┫ ┫
          ┗━┻━┛   ┗━┻━┛

"""
from time import sleep
from pyspider.libs.base_handler import *
from bs4 import BeautifulSoup
from faker import Factory
from utils import requests_utils,spider_controller

class Handler(BaseHandler):
    crawl_config = {
    }
    # 处理失败的shop_id
    false_basic_msg = []
    def __init__(self) -> None:
        super().__init__()
        self.controller = spider_controller.controller
        
    
    @every(minutes=24 * 60)
    def on_start(self):
        print(requests_utils.requests_util.get_proxy())
        area = self.controller.get_regoin()
        url = "https://www.dianping.com/search/keyword/7/10_深圳"
        # 获取区域值
        regions = area[0]
        # 获取详细分类
        classfy = area[1]
        try:
            # 第一个是用来存id的
            # 第二个是用来存名称的
            for sub_class in classfy:
                gadd = f'g{sub_class}' if sub_class != "" else ''
                # for sub_id in regions:
                #     radd = f'r{sub_id}' if sub_id != "" else ''
                #     aim_url = f'{url}/{gadd}{radd}'
                #     print(aim_url)
                #     self.crawl(aim_url, proxy= requests_utils.requests_util.get_proxy(), callback=self.local_page)
                sub_id = 31
                radd = f'r{sub_id}' if sub_id != "" else ''
                aim_url = f'{url}/{gadd}{radd}'
                print(aim_url)
                sleep(2)
                self.crawl(aim_url, proxy= requests_utils.requests_util.get_proxy(), callback=self.local_page, save={"url": aim_url, "regoin_id": sub_id, "classfy_id":sub_class})
        except Exception as e:
            # 告警
            self.false_basic_msg.append({'false_sub_class':sub_class,'false_sub_regoin':sub_id})
            print(e)
            print("区域id{sub_id} 食物分类{sub_class} 爬取失败".format(sub_id=sub_id, sub_class=sub_class))
        
     # 这里直接用自己的方法(因为文本处理比较麻烦)    
    def local_page(self, response):
        try:
            #先处理页面的数据
            each = BeautifulSoup(str(response.doc))
            #获取页面的页数
            page=each.find_all('a',class_="PageLink")
            pages = [_['title'] for _ in page]
            
            total_page = int(pages[-1])
            print(total_page)
            self.controller.main(total_page,response.save["url"])
        except Exception as e:
            print(e)
            print("获取页数失败 {save}".format(save=response.save))
        

    def index_page(self,response):
        pass

