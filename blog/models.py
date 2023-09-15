from django.db import models

from users.models import NULLABLE


class Article(models.Model):
    title = models.CharField(max_length=250, verbose_name='заголовок')
    content = models.TextField(verbose_name='содержание')
    image = models.ImageField(upload_to='articles/', verbose_name='превью', **NULLABLE)
    published_at = models.DateTimeField(auto_now_add=True, verbose_name='дата публикации')
    views_count = models.PositiveIntegerField(default=0, verbose_name='количество просмотров')

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'статья'
        verbose_name_plural = 'статьи'
        ordering = ('published_at',)
