from django.contrib import admin
from mptt.admin import MPTTModelAdmin

from .models import Category, Article


@admin.register(Category)
class CategoryAdmin(MPTTModelAdmin):
    list_display = ('id', 'name', 'parent', 'slug')
    list_display_links = ('name',)
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'author', 'created_date')
    list_display_links = ('title',)
    search_fields = ('title', 'text')
    prepopulated_fields = {'url': ('title',)}

