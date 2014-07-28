# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url
# from django.conf import settings

urlpatterns = patterns('www.article.views',
                       url(r'^$', 'home'),
                       url(r'list$', 'article_list'),
                       url(r'(?P<article_id>\d+)$', 'article_detail'),
                       )
