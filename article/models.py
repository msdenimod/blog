from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils import timezone
from mptt.models import MPTTModel, TreeForeignKey
from ckeditor.fields import RichTextField


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
        return reverse('article_category', kwargs={"slug": self.slug})

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Article(models.Model):
    author = models.ForeignKey(User, verbose_name='Автор', related_name='articles_author', on_delete=models.CASCADE)
    category = models.ForeignKey(Category, verbose_name='Категория', related_name='articles_category', on_delete=models.CASCADE)
    image = models.ImageField("Привью статьи", upload_to="article/preview", null=True, blank=True)
    title = models.CharField('Название', max_length=255)
    text = RichTextField('Текст статьи')
    created_date = models.DateTimeField('Дата создания', auto_now_add=True)
    update_date = models.DateTimeField('Дата редактирования', auto_now=True)
    published_date = models.DateTimeField(blank=True, null=True)
    url = models.SlugField(max_length=255, unique=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def un_publish(self):
        self.published_date = None
        self.save()

    def approved_comments(self):
        return self.comments.filter(approved_comment=True)

    def __str__(self):
        return self.title
        
    def get_absolute_url(self):
        return reverse('article_detail', kwargs={"slug": self.url})

    def get_article_publish_url(self):
        return reverse('article_publish', kwargs={"pk": self.pk})

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'


class Comment(models.Model):
    article = models.ForeignKey(Article, verbose_name='Статья', on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, verbose_name='Автор', related_name='comment_author', on_delete=models.CASCADE)
    text = models.TextField('Текст комментария')
    created_date = models.DateTimeField('Дата создания', auto_now_add=True)
    approved_comment = models.BooleanField('Модерация', default=False)

    def approve(self):
        self.approved_comment = True
        self.save()

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
