from django import forms

from .models import Article, Comment


class ArticleForm(forms.ModelForm):
    """Форма добавления статьи"""
    class Meta:
        model = Article
        fields = ('category', 'image', 'title', 'text')


class CommentForm(forms.ModelForm):
    """Форма добавления комментария"""
    class Meta:
        model = Comment
        fields = ('text',)
