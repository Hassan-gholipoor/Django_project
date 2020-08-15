from django.contrib import admin
from .models import Article, Category


# change admin header

admin.site.site_header = 'وبلاگ'


def make_published(modeladmin, request, queryset):
    rows_updated = queryset.update(status='p')
    if rows_updated == 1:
        message_bit = 'منتشر شد'
    else:
        message_bit = 'منتشر شدند'
    modeladmin.message_user(request, f'{rows_updated} مقاله {message_bit}')


make_published.short_description = 'انتشار مقالات انتخاب شده'


def make_draft(modeladmin, request, queryset):
    rows_updated = queryset.update(status='d')
    if rows_updated == 1:
        message_bit = 'پیشنویس شد'
    else:
        message_bit = 'پیش نویس شدند'
    modeladmin.message_user(request, f'{rows_updated} مقاله {message_bit}')


make_draft.short_description = 'پیش نویس مقالات انتخاب شده'


# Register your models here.


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('position', 'title', 'slug', 'parent', 'status')
    list_filter = (['status'])
    search_fields = ('title', 'slug')
    prepopulated_fields = {
        'slug': ('title',)
    }


admin.site.register(Category, CategoryAdmin)


class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'thumbnail_tag', 'slug', 'jpublish', 'status', 'category_to_str')
    list_filter = ('status', 'publish')
    search_fields = ('title', 'description')
    prepopulated_fields = {
        'slug': ('title',)
    }
    ordering = ['status', '-publish']
    actions = [make_published, make_draft]


admin.site.register(Article, ArticleAdmin)
