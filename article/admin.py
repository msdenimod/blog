from django.contrib import admin
from django.utils.safestring import mark_safe
from mptt.admin import MPTTModelAdmin

from .models import Category, Article, Comment


@admin.register(Category)
class CategoryAdmin(MPTTModelAdmin):
    list_display = ('id', 'name', 'parent', 'slug')
    list_display_links = ('name',)
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'get_image', 'author', 'created_date')
    list_display_links = ('title',)
    search_fields = ('title', 'text')
    prepopulated_fields = {'url': ('title',)}
    readonly_fields = ("get_image",)

    def get_image(self, obj):
        if obj.image:
            return mark_safe(f'<img src={obj.image.url} width="50" height="60">')
        else:
            return ''

    get_image.short_description = "Изображение"


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'text', 'author', 'created_date')
    list_display_links = ('text',)
    search_fields = ('text',)


admin.site.site_title = 'Админка'
admin.site.site_header = 'Админка'
