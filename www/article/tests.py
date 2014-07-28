# -*- coding: utf-8 -*-

import os
import sys

SITE_ROOT = os.path.dirname(os.path.abspath(__file__))
# 引入父目录来引入其他模块
sys.path.extend([os.path.abspath(os.path.join(SITE_ROOT, '../')),
                 os.path.abspath(os.path.join(SITE_ROOT, '../../')),
                 ])
os.environ['DJANGO_SETTINGS_MODULE'] = 'www.settings'


user_id = user = 'f762a6f5d2b711e39a09685b35d0bf16'


def main():
    from www.article import interface

    atb = interface.ArticleBase()
    atb.add_article(u"百度搜索“出海”巴西并非临时起意，事前已做好渠道铺垫", u"asdfasdfasdfads", from_url="http://www.a.com")


if __name__ == '__main__':
    main()
