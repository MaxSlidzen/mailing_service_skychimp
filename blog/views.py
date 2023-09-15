from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

from blog.forms import ArticleForm
from blog.models import Article
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse, reverse_lazy


class ArticleListView(ListView):
    model = Article
    extra_context = {
        'title': 'Блог'
    }


class ArticleDetailView(DetailView):
    model = Article
    extra_context = {
        'title': 'Статья',
    }

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.views_count += 1
        self.object.save()
        return self.object


class ArticleCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Article
    form_class = ArticleForm

    success_url = reverse_lazy('blog:article_list')
    extra_context = {
        'title': 'Создание статьи',
    }
    permission_required = 'blog.add_article'


class ArticleUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Article
    form_class = ArticleForm

    extra_context = {
        'title': 'Редактирование статьи',
    }
    permission_required = 'blog.change_article'

    def get_success_url(self):
        return reverse('blog:article_detail', args=[self.kwargs.get('pk'), self.kwargs.get('slug')])


class ArticleDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Article
    success_url = reverse_lazy('blog:article_list')
    extra_context = {
        'title': 'Удаление статьи',
    }
    permission_required = 'blog.delete_article'
