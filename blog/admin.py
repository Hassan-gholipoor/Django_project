from django.contrib import admin
from .models import Article, Category
# Register your models here.


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('position', 'title', 'slug', 'parent', 'status')
    list_filter = (['status'])
    search_fields = ('title', 'slug')
    prepopulated_fields = {'slug': ('title', )}


admin.site.register(Category, CategoryAdmin)


class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'thumbnail_tag', 'slug', 'jpublish', 'author', 'status', 'is_special', 'category_to_str')
    list_filter = ('publish', 'status','author')
    search_fields = ('title', 'description')
    prepopulated_fields = {'slug': ('title', )}
    ordering = ('status', '-publish')

    def make_published(self, request, queryset):
        rows_updated = queryset.update(status='p')
        if rows_updated == 1:
            message_bit = '1 story was'
        else:
            message_bit = f'{rows_updated} stories were'
        self.message_user(request, f'{message_bit} successfully marked as published')
    make_published.short_description = 'انتشار مقالات انتخاب شده'

    def make_draft(self, request, queryset):
        rows_updated = queryset.update(status='d')
        if rows_updated == 1:
            message_bit = '1 story was'
        else:
            message_bit = f'{rows_updated} stories were'
        self.message_user(request, f'{message_bit} successfully marked as draft')
    make_draft.short_description = 'پیش نویس مقالات انتخاب شده'

    actions = [make_published, make_draft]


admin.site.register(Article, ArticleAdmin)
