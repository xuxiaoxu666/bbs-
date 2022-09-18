from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser


class UserInfo(AbstractUser):
    phone = models.CharField(max_length=32, null=True, verbose_name='用户手机号')
    icon = models.FileField(upload_to='icon/', default='icon/default.png', null=True, verbose_name='用户头像')
    blog = models.OneToOneField(to='Blog', on_delete=models.CASCADE, null=True)

    class Meta:
        verbose_name_plural = '用户表'

    def __str__(self):
        return self.username


class Blog(models.Model):
    title = models.CharField(max_length=32, null=True, verbose_name='主标题')
    site_title = models.CharField(max_length=32, null=True, verbose_name='副标题')
    site_style = models.CharField(max_length=64, null=True, verbose_name='站点样式')

    class Meta:
        verbose_name_plural = '博客表'

    def __str__(self):
        return self.title


class Tag(models.Model):
    name = models.CharField(max_length=32, verbose_name='标签名', null=True)
    blog = models.ForeignKey(to='Blog', on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = '标签表'

    def __str__(self):
        return self.name


class Classify(models.Model):
    name = models.CharField(max_length=32, verbose_name='分类名')
    blog = models.ForeignKey(to='Blog', on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = '分类表'

    def __str__(self):
        return self.name


class Article(models.Model):
    title = models.CharField(max_length=32, verbose_name='文章标题')
    desc = models.CharField(max_length=255, verbose_name='文章摘要')
    content = models.TextField(verbose_name='文章内容')
    create_time = models.DateTimeField(auto_now_add=True)
    classify = models.ForeignKey(to='Classify', on_delete=models.CASCADE, verbose_name='分类')
    tag = models.ManyToManyField(to='Tag', verbose_name='标签')
    blog = models.ForeignKey(to='Blog', on_delete=models.CASCADE, verbose_name='博客')

    class Meta:
        verbose_name_plural = '文章表'

    def __str__(self):
        try:
            return f'文章名:{self.title}, 博客:{self.blog.title}'
        except:
            return self.title


class UpAndDown(models.Model):
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='点赞点踩时间')
    user = models.ForeignKey(to='UserInfo', on_delete=models.CASCADE)
    article = models.ForeignKey(to='Article', on_delete=models.CASCADE)
    is_up = models.BooleanField(verbose_name='是否点赞')

    class Meta:
        verbose_name_plural = '点赞表'

    # def __str__(self):
    #     return f''


class Comment(models.Model):
    content = models.CharField(max_length=64, verbose_name='评论内容')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='评论时间')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(to='UserInfo', on_delete=models.CASCADE, null=True)
    article = models.ForeignKey(to='Article', on_delete=models.CASCADE, null=True)

    class Meta:
        verbose_name_plural = '评论表'

    # def __str__(self):
    #     return f''
