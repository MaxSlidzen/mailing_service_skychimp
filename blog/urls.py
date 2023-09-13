from django.urls import path
from django.views.decorators.cache import cache_page

from blog.apps import BlogConfig
from blog.views import ArticleListView, ArticleDetailView, ArticleCreateView, ArticleUpdateView, ArticleDeleteView

app_name = BlogConfig.name

urlpatterns = [
    path('', cache_page(60)(ArticleListView.as_view()), name='article_list'),
    path('article_<int:pk>/view/', cache_page(60)(ArticleDetailView.as_view()), name='article_detail'),
    path('create/', ArticleCreateView.as_view(), name='article_create'),
    path('article_<int:pk>/update/', ArticleUpdateView.as_view(), name='article_update'),
    path('article_<int:pk>/delete/', ArticleDeleteView.as_view(), name='article_delete'),
]
