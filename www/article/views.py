# -*- coding: utf-8 -*-

import urllib
from django.contrib import auth
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template import RequestContext
from django.shortcuts import render_to_response

from common import utils, page
from www.misc import consts
from www.article import interface

atb = interface.ArticleBase()


def home(request, template_name='article/article_home.html'):
    import copy

    articles_with_img = atb.get_articles_with_img()[:8]
    article_type_list = copy.deepcopy(consts.ARTICLE_TYPE_LIST)
    for at in article_type_list:
        articles = atb.get_articles_by_article_type(at[2])[:5]
        article_type_list[at[2]].append(articles)

    return render_to_response(template_name, locals(), context_instance=RequestContext(request))


def article_detail(request, article_id=None, template_name='article/article_detail.html'):
    article = atb.get_article_by_id(article_id=article_id)
    if not article:
        raise Http404

    return render_to_response(template_name, locals(), context_instance=RequestContext(request))


def article_list(request, article_type=None, page_num=1, template_name='article/article_list.html'):
    article_type = "t%s" % article_type
    article_type = atb.get_article_type_by_domain(article_type)
    if not article_type:
        raise Http404

    articles = atb.get_articles_by_article_type(article_type[2])
    page_num = int(page_num)
    page_objs = page.Cpt(articles, count=20, page=page_num).info
    articles = page_objs[0]
    page_params = (page_objs[1], page_objs[4])

    return render_to_response(template_name, locals(), context_instance=RequestContext(request))


def test500(request):
    raise Exception, u'test500 for send error email'
