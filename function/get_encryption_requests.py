# -*- coding:utf-8 -*-

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
import json
import zlib
import base64
import time
from bs4 import BeautifulSoup

from utils.requests_utils import requests_util
from utils.cache import cache
from utils.logger import logger
from utils.spider_config import spider_config
from function.detail import Detail


def get_token(shop_url):
    ts = int(time.time() * 1000)
    cts = int(time.time() * 1000) - 600
    tokens = str({"rId": '100041', "ver": "1.0.6", "ts": ts, "cts": cts, "brVD": [1920, 186],
                  "brR": [[1920, 1080], [1920, 1040], 24, 24], "bI": [shop_url, shop_url],
                  "mT": ["1244,588"], "kT": [], "aT": [], "tT": [], "aM": "",
                  "sign": "eJxTKs7IL/BMsTU2NTAwMLVUAgApvgRP"}).encode()
    _token = zlib.compress(tokens)
    token = base64.b64encode(_token).decode()
    return token


def get_shop_url(shop_id):
    """
    根据shop id 拼接shop url
    @param shop_id:
    @return:
    """
    shop_url = 'http://www.dianping.com/shop/' + str(shop_id)
    return shop_url


def get_font_msg():
    """
    获取加密字体映射文件，如果常规流程，这一步应该是由search中完成并存入缓存。
    如果冷启动，一次search更新缓存
    @return:
    """
    if cache.search_font_map != {}:
        return cache.search_font_map
    else:
        Detail().get_detail_font_mapping('H5BIJ8PN64Rmywap')
        return cache.search_font_map


def get_retry_time():
    """
    获取ip重试次数
    @return:
    """
    # 这里处理解决请求会异常的问题,允许恰巧当前ip出问题，多试一条
    if spider_config.REPEAT_NUMBER == 0:
        retry_time = 5
    else:
        retry_time = spider_config.REPEAT_NUMBER + 1
    return retry_time


def get_basic_hidden_info(shop_id):
    """
    获取基础隐藏信息（名称、地址、电话号、cityid）
    @param shop_id:
    @return:
    """
    assert len(shop_id) == len('H2noKWCDigM0H9c1')
    shop_url = get_shop_url(shop_id)
    url = 'http://www.dianping.com/ajax/json/shopDynamic/basicHideInfo?' \
          'shopId=' + str(shop_id) + \
          '&_token=' + str(get_token(shop_url)) + \
          '&tcv=' + str(spider_config.TCV) + \
          '&uuid=' + str(spider_config.UUID) + \
          '&platform=1' \
          '&partner=150' \
          '&optimusCode=10' \
          '&originUrl=' + str(shop_url)

    r = requests_util.get_request_for_interface(url)
    r_json = json.loads(requests_util.replace_json_text(r.text, get_font_msg()))

    if r_json['code'] == 200:
        msg = r_json['msg']['shopInfo']
        shop_name = msg['shopName']

        shop_address = BeautifulSoup(msg['address'], 'lxml').text if msg['address'] \
                                                                     is not None else '' + BeautifulSoup(
            msg['crossRoad'], 'lxml').text \
            if msg['crossRoad'] is not None else ''
        shop_number = BeautifulSoup(msg['phoneNo'], 'lxml').text if msg['phoneNo'] is not None else '' + ', ' + \
                                                                                                    BeautifulSoup(
                                                                                                        msg['phoneNo2'],
                                                                                                        'lxml').text if \
            msg['phoneNo2'] is not None else ''
        return {
            'shop_id': shop_id,
            'shop_name': shop_name,
            'shop_address': shop_address,
            'shop_phone': shop_number
        }
    else:
        logger.warning('json响应码异常，尝试更改提pr，或者提issue')


def get_review_and_star(shop_id):
    """
    获取评分、人均，评论数
    @param shop_id:
    @return:
    """
    assert len(shop_id) == len('H2noKWCDigM0H9c1')
    shop_url = get_shop_url(shop_id)
    url = 'http://www.dianping.com/ajax/json/shopDynamic/reviewAndStar?' \
          'shopId=' + str(shop_id) + \
          '&cityId=19' \
          '&mainCategoryId=2821' \
          '&_token=' + str(get_token(shop_url)) + \
          '&uuid=' + str(spider_config.UUID) + \
          '&platform=1' \
          '&partner=150' \
          '&optimusCode=10' \
          '&originUrl=' + shop_url

    r = requests_util.get_request_for_interface(url)
    r_json = json.loads(requests_util.replace_json_text(r.text, get_font_msg()))

    if r_json['code'] == 200:
        try:
            shop_base_score = r_json['fiveScore']
        except:
            shop_base_score = 0.0
        score_title_list = r_json['shopScoreTitleList']
        avg_price = BeautifulSoup(r_json['avgPrice'], 'lxml').text
        review_count = BeautifulSoup(r_json['defaultReviewCount'], 'lxml').text
        score_list = []
        for each in r_json['shopRefinedScoreValueList']:
            score_list.append(BeautifulSoup(each, 'lxml').text)
        scores = {}
        for i, score in enumerate(score_list):
            scores[score_title_list[i]] = score_list[i]
        return {
            'shop_id': shop_id,
            'star_point': shop_base_score,
            'comment_list': scores,
            'mean_price': avg_price,
            'review_number': review_count
        }
    else:
        logger.warning('json响应码异常，尝试更改提pr，或者提issue')


def get_shop_tabs(shop_id):
    """
    获取招牌菜、店铺环境等
    @param shop_id:
    @return:
    """
    assert len(shop_id) == len('H2noKWCDigM0H9c1')
    shop_url = get_shop_url(shop_id)
    # Todo 这个接口需要登录，以后再说


def get_promo_info(shop_id):
    """
    coupon_info
    @param shop_id:
    @return:
    """
    assert len(shop_id) == len('H2noKWCDigM0H9c1')
    shop_url = get_shop_url(shop_id)
    # Todo 这个接口需要登录，以后再说


def get_basic_review(shop_id):
    """
    获取评分、人均，评论数
    @param shop_id:
    @return:
    """
    assert len(shop_id) == len('H2noKWCDigM0H9c1')
    shop_url = get_shop_url(shop_id)
    url = 'http://www.dianping.com/ajax/json/shopDynamic/allReview?' \
          'shopId=' + str(shop_id) + \
          '&cityId=19' \
          '&shopType=10' \
          '&tcv=' + str(spider_config.TCV) + \
          '&_token=' + str(get_token(shop_url)) + \
          '&uuid=' + str(spider_config.UUID) + \
          '&platform=1' \
          '&partner=150' \
          '&optimusCode=10' \
          '&originUrl=' + shop_url

    r = requests_util.get_request_for_interface(url)
    r_json = json.loads(requests_util.replace_json_text(r.text, get_font_msg()))

    if r_json['code'] == 200:
        # 获取评论的标签以及每个标签的个数
        summaries = []
        if r_json['summarys'] is None:
            pass
        else:
            for summary in r_json['summarys']:
                summaries.append({
                    '描述': summary['summaryString'],
                    '个数': summary['summaryCount']
                })

        # 获取评论数量信息
        all_review_count = r_json['reviewCountAll']
        review_with_pic_count = r_json['reviewCountPic']
        good_review_count = r_json['reviewCountGood']
        mid_review_count = r_json['reviewCountCommon']
        bad_review_count = r_json['reviewCountBad']

        # 获取all_review详情信息
        reviews = []
        for review in r_json['reviewAllDOList']:
            # 基础评论信息
            review_info = review['reviewDataVO']
            review_id = review_info['reviewData']['reviewId']
            review_star = review_info['reviewData']['star']
            review_body = BeautifulSoup(review_info['reviewData']['reviewBody'], 'lxml').text
            review_vote_count = review_info['reviewData']['voteCount']
            review_reply_count = review_info['reviewData']['replyCount']
            review_view_count = review_info['reviewData']['viewCount']

            # review_like_dish
            if review_info['reviewData']['extInfoList'] is not None:
                review_like_dish = review_info['reviewData']['extInfoList'][0]['values']
            else:
                review_like_dish = []

            review_avg_price = review_info['reviewData']['avgPrice']
            review_publish_time = review_info['addTimeVO']
            # review_merchant_reply
            review_merchant_reply = review_info['followNoteString']

            # 用户review_pic_list
            if review['picList'] is not None:
                review_pic_list = []
                for each_pic in review['picList']:
                    review_pic_list.append(each_pic['bigPicture'])
            else:
                review_pic_list = []

            # 获取用户相关信息
            review_username = review['user']['userNickName']
            user_id = review['user']['userId']

            each_review = {
                'shop_id': shop_id,
                '评论id': review_id,
                'user_id': user_id,
                'review_username': review_username,
                'review_total_score': review_star,
                'review_score_detail': {},
                'review_text': review_body,
                '点赞个数': review_vote_count,
                '回复个数': review_reply_count,
                '浏览次数': review_view_count,
                'mean_price': review_avg_price,
                'review_like_dish': review_like_dish,
                'review_publish_time': review_publish_time,
                'review_merchant_reply': review_merchant_reply,
                'review_pic_list': review_pic_list,
            }
            reviews.append(each_review)

        # recommend
        dish_tag_list = r_json['dishTagStrList']

        return {
            'shop_id': shop_id,
            'summaries': summaries,
            'review_number': all_review_count,
            'good_review_count': good_review_count,
            'mid_review_count': mid_review_count,
            'bad_review_count': bad_review_count,
            'review_with_pic_count': review_with_pic_count,
            'all_review': reviews,
            'recommend': dish_tag_list,
        }
    else:
        logger.warning('json响应码异常，尝试更改提pr，或者提issue')
