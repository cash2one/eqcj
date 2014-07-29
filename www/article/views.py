# -*- coding: utf-8 -*-

import urllib
from django.contrib import auth
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template import RequestContext
from django.shortcuts import render_to_response

from common import utils, page
from www.article import interface

atb = interface.ArticleBase()


def home(request, template_name='article/article_home.html'):
    articles_with_img = atb.get_articles_with_img()[:8]

    return render_to_response(template_name, locals(), context_instance=RequestContext(request))


def article_detail(request, article_id=None, template_name='article/article_detail.html'):
    article = atb.get_article_by_id(article_id=article_id)
    # if not article:
    #     raise Http404

    return render_to_response(template_name, locals(), context_instance=RequestContext(request))


def article_list(request, article_type=None, template_name='article/article_list.html'):
    article_type = "t%s" % article_type
    article_type = atb.get_article_type_by_domain(article_type)
    if not article_type:
        raise Http404

    return render_to_response(template_name, locals(), context_instance=RequestContext(request))


def test500(request):
    raise Exception, u'test500 for send error email'
