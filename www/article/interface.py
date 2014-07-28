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

    def get_article_by_id(self, article_id, state=None):
        try:
            ps = dict(id=article_id)
            if state is not None:
                ps.update(dict(state=state))
            return Article.objects.get(**ps)
        except Article.DoesNotExist:
            return None

    def get_all_articles(self, state=True):
        objs = Article.objects.all()
        if state is not None:
            objs = objs.filter(state=state)

        return objs

    def get_article_by_title(self, title):
        return self.get_all_articles(state=None).filter(title__contains=title)

    def add_article(self, title, content, from_url, img=None):
        if not (title and content):
            return 99800, dict_err.get(99800)

        article = Article.objects.create(title=title, content=content, from_url=from_url, img=img)

        return 0, article
