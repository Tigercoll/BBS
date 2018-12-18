from django import template

from bbs_blog.models import *

from django.db.models import Count

register = template.Library()



def get_left_menu(username):
    user = UserInfo.objects.filter(username=username).first()
    article_list = Article.objects.filter(author=user)
    return article_list
@register.simple_tag
def get_category_list(username):
    article_list=get_left_menu(username)
    category_list = article_list.values('category__name').annotate(
        count=Count('category__name')).values('category__name', 'count')
    return category_list

@register.simple_tag
def get_tag_list(username):
    article_list = get_left_menu(username)
    tag_list = article_list.values('tag__name').annotate(count=Count('tag__name')).values('tag__name', 'count')
    return tag_list

@register.simple_tag
def get_archive_list(username):
    article_list = get_left_menu(username)
    archive_list = []
    archive = article_list.dates('create_time', 'month', order='DESC')
    for i in archive:
        archive_count = article_list.filter(create_time__year=i.year, create_time__month=i.month).count()
        archive_list.append([i, archive_count])
    return archive_list
