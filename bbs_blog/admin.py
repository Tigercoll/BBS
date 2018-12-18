from django.contrib import admin

# Register your models here.

from bbs_blog.models import *


admin.site.register(UserInfo)
admin.site.register(BlogIndex)
admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Article)
admin.site.register(ArticleDetail)
admin.site.register(ArticleFavour)
admin.site.register(Comment)
