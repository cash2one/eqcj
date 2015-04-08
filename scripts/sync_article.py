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
import random
from pyquery import PyQuery as pq
from pprint import pprint
from www.article.models import Article

headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:29.0) Gecko/20100101 Firefox/29.0"}


def _replace_html_tag(text):
    tag_s = re.compile('<.+?>')
    tag_e = re.compile('</\w+?>')
    text = tag_s.sub('', text)
    text = tag_e.sub(' ', text)
    return text


def sync_article_head_1():
    """
    @note: 未央网采集
    """
    start_time = time.time()
    url = "http://www.weiyangx.com/"
    resp = requests.get(url, headers=headers, timeout=30)
    text = resp.text

    jq = pq(text)
    imgs = jq('#kopa_widget_articles_carousel-7 li img')
    count = 0
    now = datetime.datetime.now()
    for img in imgs:
        img_src = pq(img).attr("src")
        href = pq(img).parent().parent().attr("href")
        article = pq(requests.get(href, headers=headers, timeout=30).text)
        title = article("header:eq(1) h4 a").html().strip()
        content = article(".elements-box").children().eq(0).html()
        create_time = now - datetime.timedelta(seconds=random.randint(0, 3600 * 3))
        try:
            Article.objects.create(title=title, content=content, from_url=href, img=img_src, article_type=0, create_time=create_time)
        except Exception, e:
            print e
            break
        count += 1
        if count > 3:
            break

    end_time = time.time()
    print (u"未央网采集完成，耗时：%s秒" % int(end_time - start_time)).encode("utf8")


def sync_article_head_2():
    """
    @note: 犀牛网采集
    """
    main_url = "http://www.xinews.com.cn"
    start_time = time.time()
    url = main_url + "/action/home/"
    resp = requests.get(url, headers=headers, timeout=30)
    text = resp.text

    jq = pq(text)
    imgs = jq('.nlist .con img')
    count = 0
    now = datetime.datetime.now()
    for img in imgs:
        img_src = main_url + pq(img).attr("src")
        href = main_url + pq(img).parent().attr("href")

        article = pq(requests.get(href, headers=headers, timeout=30).text)
        title = article(".artiTle h2").html().strip()
        content = article("#frameContent").html()
        create_time = now - datetime.timedelta(seconds=random.randint(0, 3600 * 3))

        try:
            Article.objects.create(title=title, content=content, from_url=href, img=img_src, article_type=0, create_time=create_time)
        except Exception, e:
            print e
            break
        count += 1
        if count > 3:
            break

    end_time = time.time()
    print (u"犀牛网采集完成，耗时：%s秒" % int(end_time - start_time)).encode("utf8")


def sync_article_body_0():
    """
    @note: 国内财经采集
    """
    main_url = "http://www.cb.com.cn"
    start_time = time.time()
    for i in range(1, 10):
        url = main_url + "/economy/%s.html" % i
        resp = requests.get(url, headers=headers)
        text = resp.text

        jq = pq(text)
        ahrefs = jq('.cblb_list_r h2 a')
        break_flag = False

        for ahref in ahrefs:
            href = pq(ahref).attr("href")
            if "http" in href:
                continue
            href = main_url + href
            resp = requests.get(href, headers=headers)
            if resp.status_code != 200:
                continue
            resp.encoding = "utf8"
            article = pq(resp.text)
            title = article(".t30_g").html().strip()
            content = article("#Article").html()
            create_time = article(".art_nav>h4").html().strip()
            create_time = re.compile('(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})').findall(create_time)[0]
            create_time = datetime.datetime.strptime(create_time, '%Y-%m-%d %H:%M:%S')

            try:
                Article.objects.create(title=title, content=content, from_url=href, article_type=0, create_time=create_time)
            except Exception, e:
                print e
                break_flag = True
                break
        if break_flag:
            break

            # time.sleep(1)
        if i % 10 == 0:
            print "%s ok" % i

    end_time = time.time()
    print (u"国内采集完成，耗时：%s秒" % int(end_time - start_time)).encode("utf8")


def sync_article_body_1():
    """
    @note: 国际财经采集
    """
    main_url = "http://www.nbd.com.cn"
    start_time = time.time()
    for i in range(1, 10):
        url = main_url + "/columns/48/page/%s" % i
        resp = requests.get(url, headers=headers, timeout=30)
        text = resp.text

        jq = pq(text)
        ahrefs = jq('.main .articleMaterial_title a')
        break_flag = False

        for ahref in ahrefs:
            href = pq(ahref).attr("href")
            resp = requests.get(href, headers=headers, timeout=30)
            if resp.status_code != 200:
                continue
            resp.encoding = "utf8"
            article = pq(resp.text)
            title = article(".articleTitle").html().strip()
            content = article("#articleContent").html()

            create_time = article(".articleTime span:eq(0)").html().strip()
            create_time = datetime.datetime.strptime(create_time.encode("utf8"), '%Y-%m-%d %H:%M')

            # print title.encode("utf8")
            # print content.encode("utf8")
            # print create_time

            try:
                Article.objects.create(title=title, content=content, from_url=href, article_type=1, create_time=create_time)
            except Exception, e:
                print e
                break_flag = True
                break
        if break_flag:
            break

        if i % 10 == 0:
            print "%s ok" % i

    end_time = time.time()
    print (u"国际财经采集完成，耗时：%s秒" % int(end_time - start_time)).encode("utf8")


def sync_article_body_2():
    """
    @note: 公司要闻采集
    """
    main_url = "http://finance.ifeng.com"
    start_time = time.time()
    for i in range(1, 10):
        url = main_url + "/cmppdyn/26/33/%s/dynlist.html" % i

        resp = requests.get(url, headers=headers, timeout=30)
        text = resp.text

        jq = pq(text)
        ahrefs = jq('#list01 h3>a')
        break_flag = False

        for ahref in ahrefs:
            href = pq(ahref).attr("href")
            resp = requests.get(href, headers=headers, timeout=30)
            if resp.status_code != 200:
                continue
            resp.encoding = "utf8"
            # print resp.text.encode("utf8")
            article = pq(resp.text)
            if "404" in article("title").html():
                continue
            title = article("#artical>h1:eq(0)").html().strip()
            content = ""
            ps = article("#main_content p")
            for p in ps:
                content += u"<p>%s</p>" % _replace_html_tag(pq(p).html() or "")
            create_time = article("#artical_sth span:eq(0)").html().strip()
            create_time = datetime.datetime.strptime(create_time.encode("utf8"), '%Y年%m月%d日 %H:%M')

            try:
                Article.objects.create(title=title, content=content, from_url=href, article_type=2, create_time=create_time)
            except Exception, e:
                print e
                break_flag = True
                break
        if break_flag:
            break

        if i % 10 == 0:
            print "%s ok" % i

    end_time = time.time()
    print (u"公司要闻采集完成，耗时：%s秒" % int(end_time - start_time)).encode("utf8")


def sync_article_body_3():
    """
    @note: 证券要闻采集
    """
    main_url = "http://cailianpress.lanjinger.com"
    start_time = time.time()
    for i in range(1, 10):
        url = main_url + "/list-3-1.html?p=%s" % i
        resp = requests.get(url, headers=headers, timeout=30)
        text = resp.text

        jq = pq(text)
        ahrefs = jq('.i_truelist li>a:eq(0)')
        break_flag = False

        for ahref in ahrefs:
            href = main_url + pq(ahref).attr("href")
            if "?p=1" in href:
                continue
            resp = requests.get(href, headers=headers, timeout=30)
            if resp.status_code != 200:
                continue
            resp.encoding = "utf8"
            article = pq(resp.text)
            title = article(".d_title>h1:eq(0)").html().strip()
            content = article(".d_content").html().split('<div class="d_copy">')[0]

            create_time = article(".d_xian span:eq(1)").html().strip()
            create_time = datetime.datetime.strptime(create_time.encode("utf8"), '%Y-%m-%d %H:%M')

            try:
                Article.objects.create(title=title, content=content, from_url=href, article_type=3, create_time=create_time)
            except Exception, e:
                print e
                break_flag = True
                break
        if break_flag:
            break

        if i % 10 == 0:
            print "%s ok" % i

    end_time = time.time()
    print (u"证券要闻采集完成，耗时：%s秒" % int(end_time - start_time)).encode("utf8")


def sync_article_head():
    sync_article_head_1()
    sync_article_head_2()


def sync_article_body():
    sync_article_body_0()
    sync_article_body_1()
    sync_article_body_2()
    sync_article_body_3()


if __name__ == '__main__':
    sync_article_head()
    sync_article_body()

    
