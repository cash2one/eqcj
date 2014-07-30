# -*- coding: utf-8 -*-

from django.contrib import admin

from www.article.models import Article, FriendlyLink


class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'content', 'article_type', 'from_url', 'img', 'sort_num', 'state', 'create_time')


class FriendlyLinkAdmin(admin.ModelAdmin):
    list_display = ('img', 'des', 'link_type', 'sort_num', 'state', 'create_time')


admin.site.register(Article, ArticleAdmin)
admin.site.register(FriendlyLink, FriendlyLinkAdmin)
