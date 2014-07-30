# -*- coding: utf-8 -*-

# import datetime

# from common import cache, debug, utils
from www.misc import consts
from www.article.models import Article


dict_err = {
    10100: u'',
}
dict_err.update(consts.G_DICT_ERROR)


class ArticleBase(object):

    def get_article_type_by_domain(self, key):
        article_type_list = consts.ARTICLE_TYPE_LIST
        for article_type in article_type_list:
            if article_type[0] == key:
                return article_type

    def get_article_type_by_id(self, article_type_id):
        article_type_list = consts.ARTICLE_TYPE_LIST
        for article_type in article_type_list:
            if article_type[2] == article_type_id:
                return article_type

    def get_article_by_id(self, article_id, state=None):
        try:
            ps = dict(id=article_id)
            if state is not None:
                ps.update(dict(state=state))
            return Article.objects.get(**ps)
        except Article.DoesNotExist:
            return None

    def get_next_article(self, article):
        articles = Article.objects.filter(create_time__lt=article.create_time, article_type=article.article_type)
        if articles:
            return articles[0]

    def get_pre_article(self, article):
        articles = Article.objects.filter(create_time__gt=article.create_time, article_type=article.article_type).order_by("create_time")
        if articles:
            return articles[0]

    def get_related_articles(self, article):
        return Article.objects.filter(create_time__lt=article.create_time, article_type=article.article_type)[:3]

    def get_all_articles(self, state=True):
        objs = Article.objects.all()
        if state is not None:
            objs = objs.filter(state=state)

        return objs

    def get_articles_with_img(self):
        return Article.objects.exclude(img=None)

    def get_articles_by_article_type(self, article_type):
        return Article.objects.filter(article_type=article_type)

    def add_article(self, title, content, from_url, img=None):
        if not (title and content):
            return 99800, dict_err.get(99800)

        article = Article.objects.create(title=title, content=content, from_url=from_url, img=img)

        return 0, article
