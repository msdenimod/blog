# Generated by Django 3.1.3 on 2020-11-19 17:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0002_article_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='category',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='articles_category', to='article.category', verbose_name='Категория'),
            preserve_default=False,
        ),
    ]
