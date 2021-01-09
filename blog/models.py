from django.db import models
from django.utils import timezone
from account.models import User
from django.utils.html import format_html
from extensions.utils import jalali_converter


# managers
class ArticleManager(models.Manager):
    def published(self):
        return self.filter(status='p')


class CategoryManager(models.Manager):
    def active(self):
        return self.filter(status=True)


# Create your models here.


class Category(models.Model):
    parent = models.ForeignKey('self', default=None, blank=True, null=True, on_delete=models.SET_NULL, related_name='children', verbose_name='زیردسته')
    title = models.CharField(max_length=200, verbose_name='عنوان')
    slug = models.SlugField(max_length=100, unique=True, verbose_name='ادرس')
    status = models.BooleanField(default=True, verbose_name='ایا نمایش داده شود')
    position = models.IntegerField(verbose_name='پوزیشن')

    class Meta:
        verbose_name = 'دسته بندی'
        verbose_name_plural = 'دسته بندی ها'
        ordering = ['parent__id', '-position']

    def __str__(self):
        return self.title

    objects = CategoryManager()


class Article(models.Model):
    STATUS_CHOICE = (
        ('p', 'منتشرشده'),
        ('d', 'پیش تویس'),
        ('i', 'بررسی'),
        ('b', 'برگشت داده شده'),
    )
    author = models.ForeignKey(User, null=True, default=None, blank=True, on_delete=models.SET_NULL, verbose_name='نویسنده', related_name='articles')
    title = models.CharField(max_length=200, verbose_name='عنوان')
    slug = models.SlugField(max_length=100, unique=True, verbose_name='ادرس')
    category = models.ManyToManyField(Category, verbose_name='دسته بندی', related_name='articles')
    description = models.TextField(verbose_name='توضیحات')
    thumbnail = models.ImageField(upload_to='images', verbose_name='تصویر')
    publish = models.DateTimeField(default=timezone.now, verbose_name='تاریخ انتشار')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_special = models.BooleanField(default=False, verbose_name='مقاله ویژه')
    status = models.CharField(max_length=1, choices=STATUS_CHOICE, verbose_name='وضعیت')

    def __str__(self):
        return self.title

    def jpublish(self):
        return jalali_converter(self.publish)
    jpublish.short_description = 'تاریخ انتشار'

    class Meta:
        verbose_name = 'مقاله'
        verbose_name_plural = 'مقالات'
        ordering = ['-publish']

    def category_to_str(self):
        return ' ,'.join([category.title for category in self.category_published()])
    category_to_str.short_description = 'دسته بندی'

    def category_published(self):
        return self.category.filter(status=True)

    def thumbnail_tag(self):
        return format_html(f'<img width=80 src="{self.thumbnail.url}"/>')
    thumbnail_tag.short_description = 'تصویر'

    objects = ArticleManager()