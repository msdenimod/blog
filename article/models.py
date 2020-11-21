from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils import timezone
from mptt.models import MPTTModel, TreeForeignKey


class Category(MPTTModel):
    name = models.CharField('Название', max_length=255)
    parent = TreeForeignKey(
        'self',
        verbose_name='Родитель',
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='children'
    )
    slug = models.SlugField(max_length=160, unique=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category', kwargs={"slug": self.slug})

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Article(models.Model):
    author = models.ForeignKey(User, verbose_name='Автор', related_name='articles_author', on_delete=models.CASCADE)
    category = models.ForeignKey(Category, verbose_name='Категория', related_name='articles_category', on_delete=models.CASCADE)
    title = models.CharField('Название', max_length=255)
    text = models.TextField()
    created_date = models.DateTimeField('Дата создания', auto_now_add=True)
    update_date = models.DateTimeField('Дата редактирования', auto_now=True)
    published_date = models.DateTimeField(blank=True, null=True)
    url = models.SlugField(max_length=255, unique=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title
        
    def get_absolute_url(self):
        return reverse('article_detail', kwargs={"slug": self.url})

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'
