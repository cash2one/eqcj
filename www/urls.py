# -*- coding: utf-8 -*-

from django.conf.urls import patterns, include, url
from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
                       url(r'^$', 'www.article.views.home'),
                       url(r'^t(?P<article_type>\w+)$', 'www.article.views.article_list'),
                       url(r'^t(?P<article_type>\w+)/(?P<page_num>\d+)$', 'www.article.views.article_list'),
                       url(r'^article/', include('www.article.urls')),

                       url(r'^500$', 'www.article.views.test500'),
                       url(r'^(?P<txt_file_name>\w+)\.txt$', 'www.misc.views.txt_view'),

                       url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT, 'show_indexes': False}),
                       url(r'^admin/', include(admin.site.urls)),
                       )
