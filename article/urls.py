from django.urls import path
from . import views

urlpatterns = [
    path('', views.ArticleList.as_view(), name='article_list'),
    path('article/search/', views.ArticleSearchList.as_view(), name='article_search'),
    path('article/new/', views.ArticleNew.as_view(), name='article_new'),
    path('article/draft/', views.ArticleDraftList.as_view(), name='article_draft_list'),
    path('article/<slug>/', views.ArticleDetail.as_view(), name='article_detail'),
    path('article/<pk>/publish', views.ArticlePublish.as_view(), name='article_publish'),
    path('article/<pk>/unpublish', views.ArticleUnPublish.as_view(), name='article_un_publish'),
    path('article/<pk>/comment/', views.add_comment_to_article, name='add_comment_to_article'),
    path('article/<pk>/edit', views.ArticleEdit.as_view(), name='article_edit'),
    path('article/<pk>/remove', views.article_remove, name='article_remove'),
    path('comment/<pk>/approve/', views.comment_approve, name='comment_approve'),
    path('comment/<pk>/remove/', views.comment_remove, name='comment_remove'),
    path('<slug:slug>/', views.ArticleList.as_view(), name='article_category'),
]
