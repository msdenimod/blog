from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, View
from django.template.defaultfilters import slugify
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from unidecode import unidecode
from django.shortcuts import redirect
from django.utils import timezone
from .models import Article, Category, Comment
from .forms import ArticleForm, CommentForm
from django.contrib.auth.mixins import LoginRequiredMixin


class ArticleList(ListView):
    """Список статей"""
    model = Article

    def get_queryset(self):
        try:
            slug = self.kwargs['slug']
        except:
            slug = False

        if slug:
            category = get_object_or_404(Category, slug=slug.strip())

            if category.parent:
                return Article.objects.filter(published_date__lte=timezone.now(), category=category).order_by('published_date')
            else:
                categories = category.children.all()
                return Article.objects.filter(published_date__lte=timezone.now(), category__in=categories).order_by('published_date')
        else:
            return Article.objects.filter(published_date__lte=timezone.now()).order_by('published_date')


class ArticleDetail(DetailView):
    """Страница статьи"""
    model = Article
    slug_field = 'url'


class ArticleSearchList(ListView):
    """Поиск статей"""
    model = Article

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        q = self.request.GET.get('q')
        context['q'] = q
        return context

    def get_queryset(self):
        q = self.request.GET.get('q')
        return Article.objects.filter(Q(published_date__lte=timezone.now()), Q(title__icontains=q) | Q(text__icontains=q)).order_by('published_date')


class ArticleNew(LoginRequiredMixin, View):
    """Добавление новой статьи"""

    def get(self, request):
        form = ArticleForm()

        return render(request, 'article/article_edit.html', {'form': form})

    def post(self, request):
        form = ArticleForm(request.POST)

        if form.is_valid():
            article = form.save(commit=False)
            article.author = request.user
            article.save()
            slug = f'{article.title}-{article.pk}'
            article.url = slugify(unidecode(slug))
            article.save()

        return redirect('article_detail', slug=article.url)


class ArticleDraftList(LoginRequiredMixin, ListView):
    """Список черновиков"""
    model = Article
    queryset = Article.objects.filter(published_date__isnull=True).order_by('created_date')


class ArticlePublish(LoginRequiredMixin, View):
    """"Публикация статьи"""
    def get(self, request, pk):
        article = get_object_or_404(Article, pk=pk)
        article.publish()
        return redirect('article_detail', slug=article.url)


class ArticleUnPublish(LoginRequiredMixin, View):
    """"Снятие с публикации статьи"""
    def get(self, request, pk):
        article = get_object_or_404(Article, pk=pk)
        article.un_publish()
        return redirect('article_detail', slug=article.url)


class ArticleEdit(LoginRequiredMixin, View):
    """Редактировать статью"""

    def get(self, request, pk):
        article = get_object_or_404(Article, pk=pk)
        form = ArticleForm(instance=article)

        return render(request, 'article/article_edit.html', {'form': form})

    def post(self, request, pk):
        article = get_object_or_404(Article, pk=pk)
        form = ArticleForm(request.POST or None, instance=article)

        if form.is_valid():
            article = form.save(commit=False)
            slug = f'{article.title}-{article.pk}'
            article.url = slugify(unidecode(slug))
            article.save()

        return redirect('article_detail', slug=article.url)


@login_required
def article_remove(request, pk):
    article = get_object_or_404(Article, pk=pk)
    article.delete()
    return redirect('article_list')


@login_required
def add_comment_to_article(request, pk):
    article = get_object_or_404(Article, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.article = article
            comment.author = request.user
            comment.save()
            return redirect('article_detail', pk=article.pk)
    else:
        form = CommentForm()
    return render(request, 'article/add_comment_to_article.html', {'form': form})


@login_required
def comment_approve(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve()
    return redirect('article_detail', pk=comment.article.pk)


@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.delete()
    return redirect('article_detail', pk=comment.article.pk)
