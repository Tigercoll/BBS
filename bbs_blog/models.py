from django.db import models

# Create your models here.


from django.contrib.auth.models import AbstractUser


class UserInfo(AbstractUser):
    """用户表"""
    nid = models.AutoField(primary_key=True)
    avatar = models.ImageField(upload_to="static/avatars/", default="static/avatars/default.png", verbose_name="头像")
    create_time = models.DateTimeField(auto_now_add=True,verbose_name='创建时间')
    blog = models.OneToOneField(to='BlogIndex',to_field='nid',on_delete=models.CASCADE,verbose_name='个人博客',blank=True,null=True)

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = '用户表'
        verbose_name_plural = verbose_name


class BlogIndex(models.Model):
    """用户个人博客主页"""
    nid = models.AutoField(primary_key=True)
    blog_title = models.CharField(max_length=64,verbose_name='博客标题')
    site = models.CharField(max_length=32, unique=True,verbose_name='个人博客后缀')

    def __str__(self):
        return self.blog_title

    class Meta:
        verbose_name = '用户个人博客主页'
        verbose_name_plural = verbose_name


class Category(models.Model):
    """分类"""
    nid = models.AutoField(primary_key=True)
    name = models.CharField(max_length=64,verbose_name='分类名称')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "文章分类"
        verbose_name_plural = verbose_name


class Tag(models.Model):
    """
    标签
    """
    nid = models.AutoField(primary_key=True)
    name = models.CharField(max_length=64,verbose_name='标签')


    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "标签"
        verbose_name_plural = verbose_name

class Article2Tag(models.Model):
    """文章和标签的多对多关系表"""
    nid = models.AutoField(primary_key=True)
    article = models.ForeignKey(to="Article", to_field="nid",on_delete=models.CASCADE)
    tag = models.ForeignKey(to="Tag", to_field="nid",on_delete=models.CASCADE)


class Article(models.Model):
    """
    文章
    """
    nid = models.AutoField(primary_key=True)
    title = models.CharField(max_length=64,verbose_name='文章的标题')
    desc = models.CharField(max_length=128,verbose_name='文章简介')
    create_time = models.DateTimeField(auto_now_add=True,verbose_name='创建时间')
    comment_count = models.IntegerField(verbose_name='评论数')
    favour_count =models.IntegerField(verbose_name='点赞数')
    author = models.ForeignKey(to='UserInfo',to_field='nid',on_delete=models.CASCADE,verbose_name='作者')
    tag = models.ManyToManyField(to=Tag,
        through="Article2Tag",
        through_fields=("article", "tag"),verbose_name='文章标签')
    category = models.ForeignKey(to=Category,on_delete=models.CASCADE,verbose_name='文章分类')




    def __str__(self):
        return self.title

    class Meta:
        verbose_name = '文章'
        verbose_name_plural = verbose_name


class ArticleDetail(models.Model):
    """
    文章详情表
    """
    nid = models.AutoField(primary_key=True)
    content = models.TextField(verbose_name='文章内容')
    article = models.OneToOneField(to="Article", to_field="nid",on_delete=models.CASCADE)

    class Meta:
        verbose_name = "文章详情"
        verbose_name_plural = verbose_name

class ArticleFavour(models.Model):
    """
    点赞表
    """
    nid = models.AutoField(primary_key=True)
    user = models.ForeignKey(to="UserInfo", on_delete=models.CASCADE)
    article = models.ForeignKey(to="Article", on_delete=models.CASCADE)
    is_up = models.BooleanField(default=True)

    class Meta:
        unique_together = (("article", "user"),)
        verbose_name = "文章点赞"
        verbose_name_plural = verbose_name


class Comment(models.Model):
    """
    评论表
    """
    nid = models.AutoField(primary_key=True)
    article = models.ForeignKey(to="Article", to_field="nid",on_delete=models.CASCADE)
    comment_user = models.ForeignKey(to="UserInfo", to_field="nid",on_delete=models.CASCADE)
    content = models.CharField(max_length=255,verbose_name='评论内容')  # 评论内容
    create_time = models.DateTimeField(auto_now_add=True)
    parent_comment = models.ForeignKey("self", blank=True,on_delete=models.CASCADE)  # blank=True 在django admin里面可以不填

    def __str__(self):
        return self.content

    class Meta:
        verbose_name = "评论"
        verbose_name_plural = verbose_name
