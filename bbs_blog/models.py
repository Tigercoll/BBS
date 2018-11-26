from django.db import models

# Create your models here.


from django.contrib.auth.models import User


class UserInfo(User):
    """用户表"""

    avatar = models.ImageField(upload_to="static/avatars/", default="static/avatars/default.png", verbose_name="头像")
    create_time = models.DateTimeField(auto_now_add=True)


class BlogIndex(models.Model):
    """用户个人博客"""

