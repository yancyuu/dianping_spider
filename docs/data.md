# Sniper

## 数据规约：

由于数据对齐的原因，有一些字段名字可能会轻微变化。

### search：

![iamge](../imgs/show7.jpg)

![iamge](../imgs/show9.jpg)

    {
                'shop_id': -,
                'shop_name': -,
                'review_number': -,
                'mean_price': -,
                'tag1': -,
                'tag2': -,
                'shop_address': -,
                'detail_url': -,
                'image_path': -,
                'comment_list': -,
                'recommend': *,
                'star_point': -,
                'shop_phone': -,
                'other_info': #,
                'coupon_info': *,
    }

###  review

![iamge](../imgs/show8.jpg)

    {
           'shop_id': -,
           'summaries': -,
           'review_number': -,
           'good_review_count': -,
           'mid_review_count': -,
           'bad_review_count': -,
           'review_with_pic_count': -,
           'all_review': [
                          {
                            'shop_id': -,
                            '评论id': -,
                            'user_id': -,
                            'review_username': -,
                            'review_score_detail': [接口为单评分，网页为多评分],
                            'review_text': -,
                            '点赞个数': *,
                            '回复个数': *,
                            '浏览次数': *,
                            'mean_price': -,
                            'review_like_dish': -,
                            'review_publish_time': -,
                            'review_merchant_reply': -,
                            'review_pic_list': -,
                          }
                    ],
    }
    
    
    
由于采用了多种爬取方式，有些数据对于其它爬取方式并不可见，因此采用最大集的数据规约。

带*的为接口特有，带#的为网页特有，-则为都有。

