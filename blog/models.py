from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser


class UserInfo(AbstractUser):
    phone = models.CharField(max_length=32, null=True, verbose_name='用户手机号')
    icon = models.FileField(upload_to='icon/', default='icon/default.png', null=True, verbose_name='用户头像')
    blog = models.OneToOneField(to='Blog', on_delete=models.CASCADE, null=True)


class Blog(models.Model):
    title = models.CharField(max_length=32, null=True, verbose_name='主标题')
    site_title = models.CharField(max_length=32, null=True, verbose_name='副标题')
    site_style = models.CharField(max_length=64, null=True, verbose_name='站点样式')


class Tag(models.Model):
    name = models.CharField(max_length=32, verbose_name='标签名', null=True)
    blog = models.ForeignKey(to='Blog', on_delete=models.CASCADE)


class Classify(models.Model):
    name = models.CharField(max_length=32, verbose_name='分类名')
    blog = models.ForeignKey(to='Blog', on_delete=models.CASCADE)


class Article(models.Model):
    title = models.CharField(max_length=32, verbose_name='文章标题')
    desc = models.CharField(max_length=255, verbose_name='文章摘要')
    content = models.TextField(verbose_name='文章内容')
    create_time = models.DateTimeField(auto_now_add=True)
    classify = models.ForeignKey(to='Classify', on_delete=models.CASCADE)
    tag = models.ManyToManyField(to='Tag')
    blog = models.ForeignKey(to='Blog', on_delete=models.CASCADE)


class UpAndDown(models.Model):
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='点赞点踩时间')
    user = models.ForeignKey(to='UserInfo', on_delete=models.CASCADE)
    article = models.ForeignKey(to='Article', on_delete=models.CASCADE)
    is_up = models.BooleanField(verbose_name='是否点赞')


class Comment(models.Model):
    content = models.CharField(max_length=64, verbose_name='评论内容')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='评论时间')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(to='UserInfo', on_delete=models.CASCADE, null=True)
    article = models.ForeignKey(to='Article', on_delete=models.CASCADE, null=True)

