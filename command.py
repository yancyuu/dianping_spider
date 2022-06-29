# -*- coding:utf-8 -*-
# Desc: 用来命令行调度（用来测试）
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

import argparse
from urllib import request

from function.search import Search
from utils.spider_controller import controller
from utils.config import global_config
from utils.logger import logger
from utils.spider_config import spider_config
from utils.requests_utils import requests_util


parser = argparse.ArgumentParser()

parser.add_argument('--normal', type=int, required=False, default=1,
                    help='spider as normal(search->detail->review)')
parser.add_argument('--detail', type=int, required=False, default=0,
                    help='spider as custom(just detail)')
parser.add_argument('--review', type=int, required=False, default=0,
                    help='spider as custom(just review)')
parser.add_argument('--shop_id', type=str, required=False, default='',
                    help='custom shop id')
parser.add_argument('--need_more', type=bool, required=False, default=False,
                    help='need detail')
parser.add_argument('--start_page', type=int, required=False, default=1,
                    help='need start_page')
args = parser.parse_args()
if __name__ == '__main__':
    false_basic_msg = []
    if args.normal == 1:
        controller.main()
    #测试用
    if args.normal == 2:
        area = controller.get_regoin()
        url = "http://www.dianping.com/search/keyword/7/10_深圳"
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
                total_page = controller.get_total_page(aim_url, sub_id, sub_class)
                logger.info("正在爬取区域 {regoin} 分类{classfy} url{url}".format(regoin=sub_id, classfy=sub_class, url= aim_url))
                logger.info("开始页数 {start_page} 总共页数{pages}".format(start_page=args.start_page, pages=total_page))
                controller.main(total_page, args.start_page, aim_url)
        except Exception as e:
            # 告警
            false_basic_msg.append({'false_sub_class':sub_class,'false_sub_regoin':sub_id})
            print(e)
            print("区域id{sub_id} 食物分类{sub_class} 爬取失败".format(sub_id=sub_id, sub_class=sub_class))
    if args.detail == 1:
        shop_id = args.shop_id
        logger.info('爬取shop_id：' + shop_id + '详情')
        controller.get_detail(shop_id, detail=args.need_more)
    if args.review == 1:
        shop_id = args.shop_id
        logger.info('爬取shop_id：' + shop_id + '评论')
        controller.get_review(shop_id, detail=args.need_more)
