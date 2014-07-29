# -*- coding: utf-8 -*-

from django.db import models
import datetime


class Article(models.Model):
    # article_type_choices = ((0, u"国内财经"), (0, u"国际财经"), (0, u"公司要闻"), (0, u"证券要闻"))
    title = models.CharField(max_length=128)
    content = models.TextField()

    article_type = models.IntegerField()
    from_url = models.CharField(max_length=128, unique=True)
    img = models.CharField(max_length=128, null=True)
    sort_num = models.IntegerField(default=0, db_index=True)
    state = models.BooleanField(default=True, db_index=True)
    create_time = models.DateTimeField(default=datetime.datetime.now)

    class Meta:
        ordering = ["-sort_num", "-create_time"]

    def get_url(self):
        return '/article/%s' % self.id

    def get_article_type(self):
        from www.article.interface import ArticleBase
        return ArticleBase().get_article_type_by_id(self.article_type)

    def get_summary(self):
        """
        @attention: 通过内容获取摘要
        """
        from common import utils
        return utils.get_summary_from_html_by_sub(self.content).strip()


class FriendlyLink(models.Model):
    link_type_choices = ((0, u'首页链接'), (1, u'内页链接'))

    name = models.CharField(max_length=32)
    href = models.CharField(max_length=128)
    img = models.CharField(max_length=64, null=True)
    des = models.CharField(max_length=128, null=True)
    link_type = models.IntegerField(default=0, choices=link_type_choices)
    sort_num = models.IntegerField(default=0, db_index=True)
    state = models.BooleanField(default=True, db_index=True)

    class Meta:
        unique_together = [("name", 'link_type'), ]
        ordering = ["-sort_num", "id"]
