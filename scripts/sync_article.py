# -*- coding: utf-8 -*-


import sys
import os

# 引入父目录来引入其他模块
SITE_ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.extend([os.path.abspath(os.path.join(SITE_ROOT, '../')),
                 os.path.abspath(os.path.join(SITE_ROOT, '../../')),
                 ])
os.environ['DJANGO_SETTINGS_MODULE'] = 'www.settings'

import datetime
import re
import time
import requests
from pyquery import PyQuery as pq
from pprint import pprint
from www.article.models import Article


def _replace_html_tag(text):
    tag_s = re.compile('<[^\/]+?>')
    tag_e = re.compile('</\w+?>')
    text = tag_s.sub('', text)
    text = tag_e.sub(' ', text)
    return text


def sync_article_head_1():

    start_time = time.time()
    url = "http://www.weiyangx.com/"
    resp = requests.get(url)
    text = resp.text
    # print text.encode("utf8")

    jq = pq(text)
    imgs = jq('#kopa_widget_articles_carousel-7 li img')
    for img in imgs:
        img_src = pq(img).attr("src")
        href = pq(img).next().attr("href")
        article = pq(requests.get(href).text)
        title = article("header:eq(1) h4 a").html().strip()
        content = article("#dslc-content").html()
        try:
            Article.objects.create(title=title, content=content, from_url=href, img=img_src, article_type=0)
        except Exception, e:
            print e

    end_time = time.time()
    print (u"耗时：%s秒" % int(end_time - start_time)).encode("utf8")


def sync_article_head():
    sync_article_head_1()


if __name__ == '__main__':
    sync_article_head()
